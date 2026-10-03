from pathlib import Path
import tempfile,shutil,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def reindex(root):
    exclude={'PUBLIC_MANIFEST.json','SHA256SUMS.txt'}
    files=sorted(p for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in exclude)
    rec=[]
    for p in files:
        b=p.read_bytes(); rel=p.relative_to(root).as_posix(); rec.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    man={'schema':'UBUILDOS_PUBLIC_PROJECTION_MANIFEST_V1','projection_version':'1.0.1','frozen_product_sha256':'3a675b33d2733f99ca5e3c3a634dc9563354db576672d7409cb9730a7f83a330','population':len(rec),'files':rec}
    (root/'PUBLIC_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    (root/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in rec))
def case(name,edit,reindex_after=False):
    with tempfile.TemporaryDirectory() as d:
        dst=Path(d)/'p'; shutil.copytree(ROOT,dst)
        edit(dst)
        if reindex_after: reindex(dst)
        r=subprocess.run(['python3',str(dst/'tests/verify_public_projection.py')],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FALSE PASS '+name)
        print('DETECTED',name)
cases=[
 ('delete_index',lambda r:(r/'index.html').unlink(),False),
 ('modify_index',lambda r:(r/'index.html').write_text((r/'index.html').read_text()+'\nmutated'),False),
 ('delete_manifest',lambda r:(r/'PUBLIC_MANIFEST.json').unlink(),False),
 ('hidden_scoring_rehashed',lambda r:(r/'LINKEDIN_POST.md').write_text((r/'LINKEDIN_POST.md').read_text().replace('No hidden scoring.','Hidden scoring is allowed.')),True),
 ('remove_review_rehashed',lambda r:(r/'LINKEDIN_POST.md').write_text((r/'LINKEDIN_POST.md').read_text().replace('If evidence is missing, invalid, or contradictory, it goes to REVIEW.','Missing evidence may qualify automatically.')),True),
 ('lifecycle_overclaim_rehashed',lambda r:(r/'LIFECYCLE_STATUS.md').write_text((r/'LIFECYCLE_STATUS.md').read_text().replace('Terminal campaign closeout: NOT YET COMPLETE','Terminal campaign closeout: COMPLETE')),True),
 ('remove_live_label_rehashed',lambda r:(r/'LINKEDIN_POST.md').write_text((r/'LINKEDIN_POST.md').read_text().replace('Live build: ','Build: ')),True),
 ('projection_iqa_overclaim_rehashed',lambda r:(r/'LIFECYCLE_STATUS.md').write_text((r/'LIFECYCLE_STATUS.md').read_text().replace('Public-projection successor Fresh Independent IQA: NOT YET PERFORMED','Public-projection successor Fresh Independent IQA: PASS')),True),
 ('carousel_corruption_rehashed',lambda r:(r/'UBUILDOS_DAY11_LINKEDIN_CAROUSEL_v1.0.5.pdf').write_bytes(b'%PDF-1.4\n%%EOF\n'),True),
]
for x in cases: case(*x)
print('PUBLIC_MUTATION_PASS',len(cases))
