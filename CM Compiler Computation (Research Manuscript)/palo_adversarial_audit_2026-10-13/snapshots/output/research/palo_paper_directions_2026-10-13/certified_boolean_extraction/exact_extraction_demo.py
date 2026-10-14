"""Small exact research demonstrator; Python >=3.10, standard library only.

Certifies F=D+A*x+B*y+C*x*y over a joint rational coefficient/magnitude box.
The corner theorem applies because the expanded score is multi-affine in
(D,A,B,C,a,b). It does NOT apply to general networks or arbitrary polynomials.
Output goes beside this script, never into source manuscript folders.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from pathlib import Path
from copy import deepcopy
import json
import hashlib

AXES = ("D", "A", "B", "C", "a", "b")
FRAME = ((1, 1), (1, 0), (0, 1), (0, 0))
MODEL = "D+A*x+B*y+C*x*y; joint-box; strict-zero-threshold; v1"


def box(D=0, A=1, B=1, C=1, a=Q(1, 2), b=Q(1, 2)):
    values = (D, A, B, C, a, b)
    return {k: tuple(map(Q, v if isinstance(v, tuple) else (v, v)))
            for k, v in zip(AXES, values)}


def serial_box(bounds):
    return {k: list(map(str, bounds[k])) for k in AXES}


def score_expanded(z, alpha):
    D, A, B, C, a, b = z
    ex, ey = (2 * alpha[0] - 1), (2 * alpha[1] - 1)
    return D + ex*A*a + ey*B*b + ex*ey*C*a*b


def score_original(z, alpha):
    D, A, B, C, a, b = z
    x, y = (2*alpha[0]-1)*a, (2*alpha[1]-1)*b
    return D + A*x + B*y + C*x*y


def vertices(bounds):
    return list(product(*(sorted(set(bounds[k])) for k in AXES)))


def extract(bounds, family=MODEL):
    if family != MODEL:
        return {"status": "UNKNOWN", "reason": "unsupported model family"}
    if any(bounds[k][0] > bounds[k][1] for k in AXES):
        return {"status": "UNREACHABLE", "reason": "empty joint box"}
    if bounds["a"][0] <= 0 or bounds["b"][0] <= 0:
        return {"status": "UNKNOWN", "reason": "signed magnitude frame requires positivity"}
    vs = vertices(bounds)
    rows, bits = [], []
    for alpha in FRAME:
        vals = [score_expanded(z, alpha) for z in vs]
        lo, hi = min(vals), max(vals)
        positive, negative, tie = hi > 0, lo < 0, lo <= 0 <= hi
        signs = (["-"] if negative else []) + (["0"] if tie else []) + (["+"] if positive else [])
        rows.append({"alpha": list(alpha), "min": str(lo), "max": str(hi),
                     "min_vertex": list(map(str, vs[vals.index(lo)])),
                     "max_vertex": list(map(str, vs[vals.index(hi)])),
                     "attained_signs": signs,
                     "status": "MIXED" if positive and negative else
                               "TIE_PRESENT" if tie else "STRICT"})
        bits.append(1 if lo > 0 else 0 if hi < 0 else None)
    exact = all(b is not None for b in bits)
    result = {"status": "EXACT" if exact else "NONEXACT", "model": MODEL,
              "frame": [list(a) for a in FRAME], "bounds": serial_box(bounds),
              "range_proof": "multi-affine box interpolation", "rows": rows,
              "vertex_evaluations": 4*len(vs), "truth_vector": bits if exact else None}
    result["contract_sha256"] = hashlib.sha256(
        json.dumps({k:result[k] for k in ("model", "frame", "bounds")}, sort_keys=True).encode()).hexdigest()
    return result


def replay(cert, expected_bounds):
    """Check a certificate against a caller-supplied contract, using direct F.

    Bounds are checked on ALL box vertices. The universal inference relies on
    the multi-affine interpolation theorem, not on finite random testing.
    This is an exact arithmetic checker, not a proof assistant.
    """
    if cert.get("model") != MODEL or cert.get("frame") != [list(a) for a in FRAME]:
        return False
    if cert.get("bounds") != serial_box(expected_bounds):
        return False
    if cert.get("range_proof") != "multi-affine box interpolation":
        return False
    digest = hashlib.sha256(json.dumps(
        {k:cert[k] for k in ("model", "frame", "bounds")}, sort_keys=True).encode()).hexdigest()
    if cert.get("contract_sha256") != digest:
        return False
    inferred = []
    for alpha, row in zip(FRAME, cert["rows"]):
        if row["alpha"] != list(alpha):
            return False
        vals = [score_original(z, alpha) for z in vertices(expected_bounds)]
        lo, hi = min(vals), max(vals)
        if (Q(row["min"]), Q(row["max"])) != (lo, hi):
            return False
        for kind, val in (("min", lo), ("max", hi)):
            witness = tuple(map(Q, row[kind+"_vertex"]))
            if any(not expected_bounds[k][0] <= v <= expected_bounds[k][1]
                   for k, v in zip(AXES, witness)):
                return False
            if score_original(witness, alpha) != val:
                return False
        signs = (["-"] if lo < 0 else []) + (["0"] if lo <= 0 <= hi else []) + (["+"] if hi > 0 else [])
        status = "MIXED" if lo < 0 < hi else "TIE_PRESENT" if lo <= 0 <= hi else "STRICT"
        if row["attained_signs"] != signs or row["status"] != status:
            return False
        inferred.append(1 if lo > 0 else 0 if hi < 0 else None)
    if len(cert["rows"]) != 4:
        return False
    exact = all(b is not None for b in inferred)
    return cert["status"] == ("EXACT" if exact else "NONEXACT") and cert["truth_vector"] == (inferred if exact else None)


def interpolate(bounds, z, alpha):
    active = [k for k in range(6) if bounds[AXES[k]][0] != bounds[AXES[k]][1]]
    total = Q(0)
    for corner in vertices(bounds):
        w = Q(1)
        for i in active:
            lo, hi = bounds[AXES[i]]
            t = (z[i]-lo)/(hi-lo)
            w *= t if corner[i] == hi else 1-t
        total += w * score_original(corner, alpha)
    return total


def interval_baseline(bounds, alpha):
    """Natural interval arithmetic, without dependency refinement."""
    def mul(x,y):
        vals=[a*b for a in x for b in y]
        return min(vals),max(vals)
    def add(x,y):return x[0]+y[0],x[1]+y[1]
    ex,ey=2*alpha[0]-1,2*alpha[1]-1
    x=mul((Q(ex),Q(ex)),bounds["a"])
    y=mul((Q(ey),Q(ey)),bounds["b"])
    return add(add(add(bounds["D"],mul(bounds["A"],x)),mul(bounds["B"],y)),
               mul(bounds["C"],mul(x,y)))


def run():
    checks = {}
    def check(group, condition):
        assert condition, group
        checks[group] = checks.get(group, 0)+1

    examples = {
        "and_input_region": box(a=(Q(2,5),Q(3,5)), b=(Q(2,5),Q(3,5))),
        "joint_input_parameter_region": box(D=(Q(-1,100),Q(1,100)),
            A=(Q(99,100),Q(101,100)), B=(Q(99,100),Q(101,100)),
            C=(Q(99,100),Q(101,100)), a=(Q(2,5),Q(3,5)), b=(Q(2,5),Q(3,5))),
        "mixed_region": box(a=(Q(1,2),Q(2)), b=Q(1,2)),
        "boundary_point": box(a=1,b=Q(1,2)),
        "empty_box": box(a=(2,1)),
    }
    artifacts = {name:extract(bounds) for name,bounds in examples.items()}
    baselines=[]
    for name in ("and_input_region","joint_input_parameter_region"):
        intervals=[interval_baseline(examples[name],alpha) for alpha in FRAME]
        baseline_exact=all(lo>0 or hi<0 for lo,hi in intervals)
        baselines.append({"case":name,"natural_interval_ranges":[list(map(str,r)) for r in intervals],
                          "natural_interval_status":"EXACT" if baseline_exact else "UNKNOWN",
                          "corner_certificate_status":artifacts[name]["status"]})
        check("interval_comparison",not baseline_exact and artifacts[name]["status"]=="EXACT")
    for name,bounds in examples.items():
        cert = artifacts[name]
        if cert["status"] in ("EXACT", "NONEXACT"):
            check("certificate_replay", replay(cert,bounds))
    check("typed_statuses",artifacts["and_input_region"]["truth_vector"]==[1,0,0,0])
    check("typed_statuses",artifacts["joint_input_parameter_region"]["status"]=="EXACT")
    check("typed_statuses",artifacts["mixed_region"]["rows"][1]["status"]=="MIXED")
    check("typed_statuses",artifacts["boundary_point"]["rows"][1]["attained_signs"]==["0"])
    check("typed_statuses",artifacts["empty_box"]["status"]=="UNREACHABLE")
    check("typed_statuses",extract(box(),family="arbitrary neural network")["status"]=="UNKNOWN")
    for field in ("frame", "bounds", "min", "truth_vector"):
        tampered=deepcopy(artifacts["and_input_region"])
        if field=="frame": tampered[field].reverse()
        elif field=="bounds": tampered[field]["a"][0]="1/100"
        elif field=="min":tampered["rows"][1][field]="1"
        else:tampered[field]=[1,1,1,1]
        check("tamper_rejection",not replay(tampered,examples["and_input_region"]))

    # Test actual interpolation with simultaneous uncertain coefficients/inputs.
    bounds=examples["joint_input_parameter_region"]
    choices=[[lo,(lo+hi)/2,hi] for lo,hi in (bounds[k] for k in AXES)]
    for z in product(*choices):
        for alpha in FRAME:
            v=score_original(z,alpha)
            check("interpolation_identity",v==interpolate(bounds,z,alpha))

    # All 16 tables arise at +/-1 via the inverse Walsh/Hadamard map.
    all_tables=[]
    for bits in product((0,1),repeat=4):
        values=[Q(2*b-1) for b in bits]
        D=sum(values)/4
        A=sum(v*(2*a[0]-1) for v,a in zip(values,FRAME))/4
        B=sum(v*(2*a[1]-1) for v,a in zip(values,FRAME))/4
        C=sum(v*(2*a[0]-1)*(2*a[1]-1) for v,a in zip(values,FRAME))/4
        # Perturb all coefficients by 1/20; +/-1 inputs remain singletons.
        coeffs=[(v-Q(1,20),v+Q(1,20)) for v in (D,A,B,C)]
        bounds=box(*coeffs,a=1,b=1)
        cert=extract(bounds)
        check("sixteen_parameter_certificates",cert["truth_vector"]==list(bits))
        check("sixteen_parameter_certificates",replay(cert,bounds))
        all_tables.append({"truth_vector":list(bits),"coefficients":list(map(str,(D,A,B,C))),
                           "parameter_box_halfwidth":"1/20","margin":"4/5"})

    # Reproduce original four-label point dispatcher, with exact trichotomy.
    for a,b in product([Q(i,4) for i in range(1,25)],repeat=2):
        cert=extract(box(a=a,b=b))
        hs=[a-b-a*b,-a+b-a*b,-a-b+a*b]
        if 0 in hs:
            check("original_point_dispatch",cert["status"]=="NONEXACT")
        else:
            bitpair=(int(hs[0]*hs[2]<0),int(hs[1]*hs[2]<0))
            decoded={(0,0):[1,0,0,0],(1,0):[1,1,0,0],
                     (0,1):[1,0,1,0],(1,1):[1,0,0,1]}[bitpair]
            check("original_point_dispatch",cert["truth_vector"]==decoded)

    # Saturated stars: inspect symbolic sign patterns, not a universal lower-bound test.
    stars=[]
    for k in range(1,5):
        q=2**k-1
        codes=[tuple((j>>i)&1 for i in range(k)) for j in range(q+1)]
        row_loads=[sum(c[i] for c in codes) for i in range(k)]
        check("star_codes",all(w==2**(k-1) for w in row_loads))
        for leaf in range(q+1):
            hs=[Q(1) if leaf==j else Q(-1) for j in range(1,q+1)]
            signature=[]
            for i in range(k):
                selected=[hs[j-1] for j in range(1,q+1) if codes[j][i]]
                h=Q((-1)**(len(selected)+1))
                for v in selected:h*=v
                signature.append(int(h>0))
            check("star_codes",tuple(signature)==codes[leaf])
        stars.append({"labels":q+1,"minimum_bits":k,"quadratic_boundary_degree_required":2**k})
    # Seven disjoint radius-one discs, degree-two irreducible boundaries.
    for leaf in range(8):
        u,v=(Q(4*leaf),Q(0)) if leaf else (Q(0),Q(0))
        signs=[int(1-(u-4*j)**2-v*v>0) for j in range(1,8)]
        check("seven_disc_witnesses",signs==[int(j==leaf) for j in range(1,8)])
    weights=(1,2,3)
    optimum=min(max(sum(w for w,c in zip(p,(1,2,3)) if c&(1<<i)) for i in range(2))
                for p in permutations(weights))
    check("weighted_star",optimum==4)

    # Endpoint equality is not persistence. Constant-in-input polynomial family.
    trajectory=[]
    for t in (Q(0),Q(1,2),Q(1),Q(3,2),Q(2)):
        D=(t-Q(1,2))*(t-Q(3,2))
        cert=extract(box(D=D,A=0,B=0,C=0,a=1,b=1))
        trajectory.append({"t":str(t),"D":str(D),"status":cert["status"],"truth_vector":cert["truth_vector"]})
    check("trajectory_counterexample",trajectory[0]["truth_vector"]==trajectory[-1]["truth_vector"])
    check("trajectory_counterexample",trajectory[2]["truth_vector"]!=trajectory[0]["truth_vector"])
    # A non-multi-affine score has positive endpoints and a negative interior.
    g=lambda t:(t-Q(1,2))**2-Q(1,100)
    check("corner_only_unsound_outside_family",g(Q(0))>0 and g(Q(1))>0 and g(Q(1,2))<0)
    # Disconnected cells can contain both signs and no tie: {-1,+1}, g(x)=x.
    check("disconnected_image_counterexample",set(map(lambda t:(t>0)-(t<0),[-1,1]))=={-1,1})
    results={"status":"PASS","assertions_by_group":checks,"total_assertions":sum(checks.values()),
             "examples":artifacts,"interval_baselines":baselines,
             "sixteen_tables":all_tables,"star_code_checks":stars,
             "weighted_three_leaf_optimum":optimum,"trajectory":trajectory,
             "limitations":["No neural training or PALO integration",
                "No SMT, general polynomial, constrained-region or floating-point backend",
                "Corner checks support a classical multi-affine theorem; no general sampling certificate",
                "Star lower bounds are mathematical arguments in the dossier, not established by enumeration",
                "No runtime speedup or novelty claim"]}
    (Path(__file__).parent/'demo_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps({"status":"PASS","total_assertions":sum(checks.values()),"groups":checks}))


if __name__=="__main__":
    run()
