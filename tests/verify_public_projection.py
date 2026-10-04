from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parents[1]
def fail(x): raise SystemExit('FAIL: '+x)

m=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
if m.get('schema')!='UBUILDOS_PUBLIC_PROJECTION_MANIFEST_V1': fail('manifest schema')
if m.get('projection_version')!='1.0.2': fail('projection version')
records=m.get('files',[])
if m.get('population')!=len(records): fail('population')
seen=set()
for r in records:
    p=r['path']
    if p in seen: fail('duplicate '+p)
    seen.add(p)
    f=ROOT/p
    if not f.is_file(): fail('missing '+p)
    b=f.read_bytes()
    if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: fail('integrity '+p)
checks={}
for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
    if not line: continue
    h,p=line.split('  ',1); checks[p]=h
if len(checks)!=len(records): fail('checksum population')
for r in records:
    if checks.get(r['path'])!=r['sha256']: fail('checksum '+r['path'])

html=(ROOT/'index.html').read_text()
for ref in re.findall(r'(?:href|src)="([^"]+)"',html):
    if ref.startswith(('http:','https:','#')): continue
    if not (ROOT/ref).exists(): fail('broken local ref '+ref)

post=(ROOT/'LINKEDIN_POST.md').read_text()
for token in [
    'No hidden scoring.',
    'If evidence is missing, invalid, or contradictory, it goes to REVIEW.',
    'Live build: https://braiz-works.github.io/ubuildos-completion-receipt-012/',
    'Public repository: https://github.com/BRAIZ-Works/ubuildos-completion-receipt-012',
    'What it does NOT prove']:
    if token not in post: fail('linkedin semantic token: '+token)

life=(ROOT/'LIFECYCLE_STATUS.md').read_text()
for token in [
    'Public projection v1.0.1 — deployed predecessor',
    '685ad609e7c76a8a9de6ec61604ed96652a74d5ffa2f11ccc57fb5a08ec98952',
    'Repository deployment commit: `afb8c5e473df1d4cf027b9fe18ce56cf4b28c5e9`',
    'Public projection v1.0.2 — documentation-currentness successor',
    'Fresh Independent IQA: NOT YET PERFORMED',
    'terminal campaign closeout: NOT YET COMPLETE']:
    if token not in life: fail('lifecycle token: '+token)

readme=(ROOT/'README.md').read_text()
for token in [
    '# UBuildOS Prospect Qualification Pipeline™ — Day 11',
    'Live build: https://braiz-works.github.io/ubuildos-completion-receipt-012/',
    'Public repository: https://github.com/BRAIZ-Works/ubuildos-completion-receipt-012',
    '3a675b33d2733f99ca5e3c3a634dc9563354db576672d7409cb9730a7f83a330',
    '685ad609e7c76a8a9de6ec61604ed96652a74d5ffa2f11ccc57fb5a08ec98952',
    'afb8c5e473df1d4cf027b9fe18ce56cf4b28c5e9',
    'ee9162a13af043feb0d323631c3c157ad231489d3b5a931a82113608252c9c1e',
    'This `v1.0.2` package is a documentation-currentness successor only.']:
    if token not in readme: fail('readme currentness token: '+token)

carousel=ROOT/'UBUILDOS_DAY11_LINKEDIN_CAROUSEL_v1.0.5.pdf'
if not carousel.is_file(): fail('carousel successor missing')
if hashlib.sha256(carousel.read_bytes()).hexdigest()!='ee9162a13af043feb0d323631c3c157ad231489d3b5a931a82113608252c9c1e': fail('carousel identity')

qa=(ROOT/'evidence/CAROUSEL_SUCCESSOR_QA.md').read_text().lower()
for token in ['dominant empty-panel defect from v1.0.0','fresh independent iqa remains separate']:
    if token not in qa: fail('carousel qa token: '+token)

for p in [ROOT/'LIFECYCLE_STATUS.md',ROOT/'PUBLICATION_GATE.md',ROOT/'docs/VERIFICATION_SUMMARY.md',ROOT/'README.md']:
    t=p.read_text()
    forbidden=[
        'v1.0.2 Fresh Independent IQA: PASS',
        'v1.0.2 publication/deployment: COMPLETE',
        'Public projection v1.0.2 — deployed',
        'Terminal campaign closeout: COMPLETE']
    for token in forbidden:
        if token in t: fail('v1.0.2 overclaim '+p.name+': '+token)

print('PUBLIC_PROJECTION_VERIFY_PASS')
