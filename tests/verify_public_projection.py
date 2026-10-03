from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def fail(x): raise SystemExit('FAIL: '+x)
m=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
if m.get('schema')!='UBUILDOS_PUBLIC_PROJECTION_MANIFEST_V1': fail('manifest schema')
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
required=[
    'No hidden scoring.',
    'If evidence is missing, invalid, or contradictory, it goes to REVIEW.',
    'Live build: https://braiz-works.github.io/ubuildos-completion-receipt-012/',
    'Public repository: https://github.com/BRAIZ-Works/ubuildos-completion-receipt-012',
    'What it does NOT prove'
]
for token in required:
    if token not in post: fail('linkedin semantic token: '+token)
life=(ROOT/'LIFECYCLE_STATUS.md').read_text()
for token in ['Fresh Independent IQA: PASS','Owner accepted: YES','Frozen: YES','Public repository: NOT YET PUBLISHED','Terminal campaign closeout: NOT YET COMPLETE']:
    if token not in life: fail('lifecycle token: '+token)
readme=(ROOT/'README.md').read_text()
if '3a675b33d2733f99ca5e3c3a634dc9563354db576672d7409cb9730a7f83a330' not in readme: fail('frozen identity')
print('PUBLIC_PROJECTION_VERIFY_PASS')
