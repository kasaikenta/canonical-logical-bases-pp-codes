#!/usr/bin/env python3
"""Resume exact distance exclusions from the supplied C++17 search source."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,subprocess,time
P=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=600);ap.add_argument('--jobs',type=int,default=3);ap.add_argument('--roots',type=int,nargs='+');ap.add_argument('--bound',type=int);a=ap.parse_args()
    summary=json.loads((P/'summary.json').read_text());bound=summary['d']-1 if a.bound is None else a.bound
    root_count=16 if (P/'physical_search.cpp').exists() else 24
    roots=list(range(root_count)) if a.roots is None else sorted(set(a.roots));assert roots and all(0<=r<root_count for r in roots)
    source=P/('physical_search.cpp' if root_count==16 else 'partitioned_search.cpp');exe=P/'partitioned_search';subprocess.run(['c++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True)
    start=time.time()
    def run(side,root):
        p=P/f'recheck_{root_count}roots_{side}_bound{bound}_root{root}.json'
        if p.exists():
            r=json.loads(p.read_text())
            if r['bound']==bound and r['root_first']==root and r['root_last']==root+1 and (r['found'] or r['complete_exclusion']):return side,root,r
        subprocess.run([str(exe),str(P/f'distance/{side}_input.txt'),str(p),str(bound),str(a.seconds),str(P/f'distance/{side}_stabilizers.txt'),str(root),str(root+1)],check=True,stdout=subprocess.DEVNULL)
        return side,root,json.loads(p.read_text())
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        ff=[pool.submit(run,side,root) for root in roots for side in 'XZ']
        for f in concurrent.futures.as_completed(ff):
            side,root,r=f.result();results.append(dict(side=side,root=root,**r));print(side,root,r['complete_exclusion'],r['found'],r['timed_out'],flush=True)
    full=roots==list(range(root_count)) and len(results)==2*root_count and all(r['complete_exclusion'] and not r['timed_out'] and r['completed_roots']==r['total_roots']==1 for r in results)
    record=dict(bound=bound,complete_both_sides_exclusion=full,quantum_distance_lower_bound=bound+1 if full else None,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),wall_seconds=time.time()-start,results=results,scope='Only the complete root set on both sides give a quantum distance lower bound. A timeout or partial root set gives none.')
    (P/'distance_recheck.json').write_text(json.dumps(record,indent=2)+'\n');print('Complete both sides:',full,flush=True)
if __name__=='__main__':main()
