"""Run both complete state enumeration and safety checks. Provide an official TLC jar."""
import argparse,subprocess,json,re,hashlib,pathlib
p=argparse.ArgumentParser();p.add_argument('jar');args=p.parse_args()
root=pathlib.Path(__file__).resolve().parent; jar=pathlib.Path(args.jar).resolve()
rows=[]
for epoch in [1,2,3,5,7]:
 for mode in ['local_ack','volatile_receipt','regressive_policy','session_bypass','protected']:
  name=f'{mode}_e{epoch}_count';cfg=root/(name+'.cfg')
  cfg.write_text(f'CONSTANT Mode = "{mode}"\nCONSTANT MaxEpoch = {epoch}\nSPECIFICATION Spec\nINVARIANT TypeOK\nCHECK_DEADLOCK FALSE\n')
  cmd=['java','-Xmx512m','-cp',str(jar),'tlc2.TLC','-workers','1','-cleanup','-config',cfg.name,'FirewallEpochs.tla']
  r=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=90)
  log=r.stdout+r.stderr;(root/'evidence'/f'{name}.log').write_text(log)
  m=re.search(r'([\d,]+) states generated, ([\d,]+) distinct states found',log)
  if r.returncode or not m:raise RuntimeError(log)
  rows.append(dict(mode=mode,max_epoch=epoch,generated=int(m[1].replace(',','')),distinct=int(m[2].replace(',',''))))
  print(name,rows[-1]['distinct'],flush=True)
for mode in ['local_ack','volatile_receipt','regressive_policy','session_bypass','protected']:
 name=f'{mode}_e7_safety';cfg=root/(name+'.cfg')
 cfg.write_text(f'CONSTANT Mode = "{mode}"\nCONSTANT MaxEpoch = 7\nSPECIFICATION Spec\nINVARIANTS TypeOK Safe ProtectedOrder\nCHECK_DEADLOCK FALSE\n')
 r=subprocess.run(['java','-Xmx512m','-cp',str(jar),'tlc2.TLC','-workers','1','-cleanup','-config',cfg.name,'FirewallEpochs.tla'],cwd=root,capture_output=True,text=True,timeout=90)
 log=r.stdout+r.stderr;(root/'evidence'/f'{name}.log').write_text(log)
 expected=('Model checking completed. No error has been found.' in log) if mode=='protected' else ('Invariant Safe is violated.' in log)
 if not expected:raise RuntimeError(log)
 print(name,'expected result',flush=True)
python=json.loads((root/'evidence/python_results.json').read_text())['results']
for t,py in zip(rows,python):
 assert (t['mode'],t['max_epoch'])==(py['mode'],py['max_epoch'])
 assert t['distinct']==py['reachable_states'],(t,py)
(root/'evidence/tlc_summary.json').write_text(json.dumps({'jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'results':rows,'cross_check':'All 25 reachable-state counts match Python; all five epoch-7 safety outcomes match.'},indent=2))
print('All cross-checks passed.',flush=True)
