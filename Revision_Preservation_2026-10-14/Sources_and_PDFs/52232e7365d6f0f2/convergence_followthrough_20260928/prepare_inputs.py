"""Import immutable research packages with ZIP path checks and provenance."""
from pathlib import Path
import hashlib, json, shutil, stat, zipfile

ROOT = Path(__file__).resolve().parent
DOWNLOADS = Path(r'C:\Users\brian\Downloads')
PACKAGES = {
    'external_audit': 'ASTRA_Convergence_Audit_2026-09-28 (1).zip',
    'theory': 'QK_THEORY_MILESTONE_1_BUNDLE.zip',
    'baseline': 'CM_Computation_Baseline_Handoff_for_Convergence_Audit_2026-09-28.zip',
}

def main():
    records=[]
    for label,name in PACKAGES.items():
        src=DOWNLOADS/name
        dest=ROOT/'inputs'/label
        dest.mkdir(parents=True,exist_ok=False)
        archive=dest/'original.zip'
        shutil.copy2(src,archive)
        with zipfile.ZipFile(archive) as z:
            assert sum(i.file_size for i in z.infolist())<200_000_000
            for item in z.infolist():
                path=Path(item.filename)
                assert not path.is_absolute() and '..' not in path.parts and '\\' not in item.filename
                assert not stat.S_ISLNK(item.external_attr>>16)
                assert (dest/path).resolve().is_relative_to(dest.resolve())
            z.extractall(dest)
        records.append({'label':label,'source':str(src),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    (ROOT/'INPUT_PROVENANCE.json').write_text(json.dumps(records,indent=2))
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
