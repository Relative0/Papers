"""Read current manuscript identities and resolve literal local TeX dependencies."""
from snapshot import ROOT,OUT,dump,sha
import json,re,pathlib
def main():
    results=[]
    for paper in json.loads((OUT/'paper_catalog.json').read_text(encoding='utf-8')):
        if not paper['source']:continue
        src=ROOT/paper['home']/paper['source']
        if src.suffix!='.tex':continue
        text=src.read_text(encoding='utf-8-sig',errors='replace')
        title=re.search(r'\\title(?:\[[^]]*\])?\{([\s\S]*?)(?=\\(?:author|date|begin\{document))',text)
        abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',text)
        checked=[];visited=set()
        def visit(p):
            if p in visited:return
            visited.add(p);t=p.read_text(encoding='utf-8-sig',errors='replace')
            t=re.sub(r'(?<!\\)%[^\n]*','',t)
            for command,raw in re.findall(r'\\(input|include|bibliography|addbibresource|includegraphics)(?:\[[^]]*\])?\{([^}]+)\}',t):
                for target in raw.split(',') if command=='bibliography' else [raw]:
                    if '\\' in target or '#' in target:continue
                    q=p.parent/target
                    options=[q] if q.suffix else [q.with_suffix(s) for s in (['.bib'] if command in ('bibliography','addbibresource') else ['.pdf','.png','.jpg'] if command=='includegraphics' else ['.tex'])]
                    found=next((x for x in options if x.is_file()),None)
                    checked.append({'source':p.relative_to(ROOT).as_posix(),'command':command,'reference':target,'resolved':found.relative_to(ROOT).as_posix() if found else None,'status':'PASS' if found else 'MISSING'})
                    if found and found.suffix=='.tex':visit(found)
        visit(src)
        results.append({'paper_id':paper['id'],'source':src.relative_to(ROOT).as_posix(),'sha256':sha(src),'title_source_excerpt':title[1].strip()[:1300] if title else None,'abstract':abstract[1].strip() if abstract else None,'dependencies':checked})
    dump('current_manuscript_evidence.json',results)
    print(json.dumps({'manuscript_sources':len(results),'literal_dependencies':sum(len(x['dependencies']) for x in results),'missing':[d for r in results for d in r['dependencies'] if d['status']=='MISSING']},indent=2))
if __name__=='__main__':main()
