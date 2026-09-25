import pathlib, hashlib, json, csv, re, zipfile, io, collections
from pypdf import PdfReader
ROOT=pathlib.Path(r'C:\Users\brian\Documents\Math Latex etc\Papers for Publication')
OUT=pathlib.Path(__file__).parent
TEXT=OUT/'text'; TEXT.mkdir(exist_ok=True)
rows=[]; errors=[]; archives=[]; seen={}; profiles=[]; manifests=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def extract(b, suffix):
    if suffix=='.pdf':
        p=PdfReader(io.BytesIO(b)); return '\n'.join(f'\n[PAGE {i+1}]\n'+(x.extract_text() or '') for i,x in enumerate(p.pages)),len(p.pages)
    return b.decode('utf-8-sig',errors='replace'),None
def profile(path,b,h):
    suffix=pathlib.PurePosixPath(path).suffix.lower()
    if suffix not in {'.pdf','.tex','.md','.txt','.py','.json','.csv','.bib','.log','.sh','.ps1','.yaml','.yml'}: return
    if h in seen: return
    seen[h]=path
    try:
        text,pages=extract(b,suffix)
        (TEXT/(h+'.txt')).write_text(text,encoding='utf-8')
        headings=[{'line':i+1,'text':l[:500]} for i,l in enumerate(text.splitlines()) if re.search(r'^(#{1,6} |\\(?:sub)*section|\\title|\\begin\{(?:theorem|lemma|proposition|corollary|abstract)|.*(?:Theorem|Proposition|Lemma)\s+\d)',l)]
        profiles.append({'path':path,'sha256':h,'pages':pages,'start':text[:1800],'headings':headings,'chars':len(text)})
    except Exception as e: errors.append({'path':path,'error':str(e)})
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or '.git' in p.relative_to(ROOT).parts: continue
    rel=p.relative_to(ROOT).as_posix()
    if p.name.startswith('.env') or p.suffix.lower() in {'.key','.sqlite','.db'}: raise RuntimeError('Sensitive file encountered: '+rel)
    b=p.read_bytes(); h=sha(b); rows.append({'path':rel,'bytes':len(b),'sha256':h,'folder':rel.split('/')[0]})
    profile(rel,b,h)
    if p.name=='SOURCE_MANIFEST_SHA256.csv':
        entries=list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')))); issues=[]
        for e in entries:
            q=p.parent/e['RelativePath']; actual=sha(q.read_bytes()) if q.is_file() else None
            if actual!=e['SHA256'].lower(): issues.append({'path':e['RelativePath'],'expected':e['SHA256'],'actual':actual})
        manifests.append({'path':rel,'entries':len(entries),'issues':issues})
    if p.suffix.lower()=='.zip':
        with zipfile.ZipFile(p) as z:
            for info in z.infolist():
                if info.is_dir(): continue
                b2=z.read(info); h2=sha(b2); v=rel+'!/'+info.filename
                archives.append({'archive':rel,'member':info.filename,'bytes':len(b2),'sha256':h2})
                profile(v,b2,h2)
for name,obj in [('inventory_before',rows),('profiles',profiles),('archive_members',archives),('manifest_checks_before',manifests),('extraction_errors',errors)]:
    (OUT/(name+'.json')).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'distinct_hashes':len(set(x['sha256'] for x in rows)),'unique_texts':len(profiles),'archive_members':len(archives),'extraction_errors':errors,'manifest_issues':[(x['path'],len(x['issues'])) for x in manifests],'folders':dict(collections.Counter(x['folder'] for x in rows))},indent=2))
