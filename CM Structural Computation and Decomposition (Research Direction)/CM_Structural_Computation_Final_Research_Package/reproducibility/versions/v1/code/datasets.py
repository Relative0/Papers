"""Pinned EPFL ctrl BLIF plus explicitly synthetic positive/negative controls."""
from pathlib import Path
import hashlib, random, json

CTRL_SHA = '59b209caf863b2c6a9739777ae0a60a37cc4480c2e0d72fcbfcdddeb9a49be08'

class Blif:
    def __init__(self, path):
        blob = Path(path).read_bytes()
        if hashlib.sha256(blob).hexdigest() != CTRL_SHA:
            raise ValueError('Pinned source checksum mismatch')
        text = blob.decode().replace('\\\n',' ')
        self.nodes = {}
        current = None
        for line in text.splitlines():
            words = line.strip().split()
            if not words or words[0].startswith('#'): continue
            if words[0] == '.inputs': self.inputs = words[1:]
            elif words[0] == '.outputs': self.outputs = words[1:]
            elif words[0] == '.names':
                current = words[-1]
                self.nodes[current] = (tuple(words[1:-1]), [])
            elif not words[0].startswith('.'):
                deps, cubes = self.nodes[current]
                if not deps:
                    cubes.append(('', int(words[0])))
                else:
                    if len(words) != 2 or len(words[0]) != len(deps):
                        raise ValueError('unsupported cover syntax')
                    cubes.append((words[0], int(words[1])))
        for deps, cubes in self.nodes.values():
            if len({b for _,b in cubes}) > 1: raise ValueError('mixed on/off cover')
    def support(self, name):
        if name in self.inputs: return {name}
        deps, _ = self.nodes[name]
        out = set()
        for v in deps: out |= self.support(v)
        return out
    def scalar(self, root, env):
        memo = dict(env)
        def ev(name):
            if name in memo: return memo[name]
            deps, cubes = self.nodes[name]
            values = [ev(x) for x in deps]
            pol = cubes[0][1] if cubes else 1
            match = any(all(c=='-' or int(c)==v for c,v in zip(pattern, values)) for pattern,_ in cubes)
            memo[name] = pol if match else 1-pol
            return memo[name]
        return ev(root)
    def truth(self, root):
        # Two evaluation routes: scalar recursion and packed cube algebra.
        names = tuple(v for v in self.inputs if v in self.support(root))
        n, bits = len(names), 0
        for a in range(1 << n):
            env = {v:(a >> (n-j-1))&1 for j,v in enumerate(names)}
            bits |= self.scalar(root, env) << a
        full = (1 << (1 << n))-1
        memo = {v: sum(((a >> (n-j-1))&1)<<a for a in range(1 << n)) for j,v in enumerate(names)}
        def packed(name):
            if name in memo: return memo[name]
            deps,cubes = self.nodes[name]
            args = [packed(v) for v in deps]
            cover = 0
            for pattern,pol in cubes:
                term = full
                for c,a in zip(pattern,args):
                    if c != '-': term &= a if c == '1' else a^full
                cover |= term
            pol = cubes[0][1] if cubes else 1
            memo[name] = cover if pol else cover^full
            return memo[name]
        assert bits == packed(root)
        return {'id':'epfl_ctrl:'+root, 'origin':'external_ctrl', 'n':n,
                'scope_names':names, 'truth_hex':hex(bits), 'source_sha256':CTRL_SHA}


def build_dataset(root: Path):
    ctrl = Blif(root/'data'/'ctrl_size_2023.blif')
    data = [ctrl.truth(name) for name in ctrl.outputs]
    for n in (4,8,12):
        for family in ('parity','inner_product','product_of_xors','random'):
            rng = random.Random(2026092600+n)
            bits = 0
            for a in range(1 << n):
                values = [(a >> (n-j-1))&1 for j in range(n)]
                if family=='parity': v=sum(values)&1
                elif family=='inner_product': v=sum(values[j]*values[n//2+j] for j in range(n//2))&1
                elif family=='product_of_xors':
                    v=1
                    for j in range(0,n,2): v *= values[j]^values[j+1]
                else: v=rng.getrandbits(1)
                bits |= v << a
            data.append({'id':f'synthetic:{family}:{n}','origin':'synthetic_'+family,
                         'n':n, 'scope_names':list(range(n)), 'truth_hex':hex(bits)})
    return data

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    data=build_dataset(root)
    blob=json.dumps(data,indent=2,sort_keys=True).encode()+b'\n'
    (root/'data'/'cases.json').write_bytes(blob)
    print(json.dumps({'cases':len(data),'external':sum(x['origin']=='external_ctrl' for x in data),
                      'sha256':hashlib.sha256(blob).hexdigest()},indent=2))
