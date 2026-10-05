#!/usr/bin/env python3
"""Reexecute saved binary girth-6 distance roots, preserving the original evidence."""
import argparse,concurrent.futures as cf,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--all',action='store_true');g.add_argument('--code',action='append');p.add_argument('--jobs',type=int,default=max(1,os.cpu_count() or 1));p.add_argument('--seconds',type=float,default=600);p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert a.jobs>=1 and a.seconds>0
 codes=[]
 for code in (ROOT/'codes').iterdir():
  mp=code/'metadata.json'
  if not mp.exists():continue
  meta=json.loads(mp.read_text())
  if 'three_mac_distance_recheck' in meta and (a.all or meta['id'] in a.code):codes.append((code,meta))
 assert codes and (a.all or len(codes)==len(set(a.code))), 'Unknown code ID'
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);assert out!=ROOT and not out.is_relative_to(ROOT/'codes'),'Use a separate output directory'
 source=ROOT/'scripts/physical_binary_distance.cpp';source_sha=sha(source);exe=out/'physical_binary_distance';subprocess.run(['c++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True);tasks=[]
 for code,meta in codes:
  certpath=code/meta['three_mac_distance_recheck'];cert=json.loads(certpath.read_text());r=certpath.parent;assert source_sha==cert['source_sha256']
  for side in ['X','Z']:
   ss=cert['sides'][side];inp=r/(side+'_input.txt');st=r/(side+'_stabilizers.txt');assert sha(inp)==ss['input_sha256'] and sha(st)==ss['stabilizer_sha256']
   for root in range(16):tasks.append({'code_id':meta['id'],'side':side,'root':root,'limit':meta['d']-1,'input':str(inp),'stabilizers':str(st),'input_sha256':ss['input_sha256'],'stabilizer_sha256':ss['stabilizer_sha256'],'source_sha256':source_sha})
 def run(t):
  dest=out/t['code_id'];dest.mkdir(exist_ok=True);name=t['side']+'_r'+str(t['root']).zfill(2);record=dest/(name+'.json');raw=dest/(name+'.raw.json')
  if record.exists():
   old=json.loads(record.read_text())
   if old.get('passed') and old.get('task')==t:return old
  started=time.time();x=subprocess.run([str(exe),t['input'],str(raw),str(t['limit']),str(a.seconds),t['stabilizers'],str(t['root']),str(t['root']+1)],capture_output=True,text=True);r=json.loads(raw.read_text()) if raw.exists() else {}
  passed=x.returncode==0 and r.get('complete_exclusion') and not r.get('found') and not r.get('timed_out') and r.get('bound')==t['limit'] and r.get('completed_roots')==r.get('total_roots')==1 and r.get('root_first')==t['root'] and r.get('root_last')==t['root']+1
  result={'task':t,'passed':bool(passed),'result':r,'returncode':x.returncode,'stderr':x.stderr,'started_at':started,'finished_at':time.time()};tmp=record.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');os.replace(tmp,record);return result
 results=[]
 with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
  for future in cf.as_completed([pool.submit(run,t) for t in tasks]):
   results.append(future.result())
   if len(results)%32==0 or len(results)==len(tasks):print(str(len(results))+'/'+str(len(tasks))+' roots, failures='+str(sum(not x['passed'] for x in results)),flush=True)
 report={'all_passed':all(x['passed'] for x in results),'total_roots':len(results),'source_sha256':source_sha,'codes':[meta['id'] for _,meta in codes],'note':'An incomplete or timed-out root never proves a distance lower bound. Verified weight-d witnesses are preserved in the original data.'};(out/'replay_summary.json').write_text(json.dumps(report,indent=2)+'\n');return 0 if report['all_passed'] else 1
if __name__=='__main__':sys.exit(main())
