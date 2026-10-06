#!/usr/bin/env python3
"""Verify completed distance records against the actual binary matrices.

This checks saved search completion, input reconstruction, upper witnesses,
and cyclic/side-exchange symmetries. --regenerate-partitions additionally
compiles the archived C++ engines and regenerates every archived branch split;
it does not rerun the expensive leaf exclusions.
"""
from pathlib import Path
import argparse, gzip, hashlib, json, subprocess, tempfile
import numpy as np
from verify_all import verify, rows_as_ints

ROOT=Path(__file__).resolve().parents[1]
RHO=(np.zeros((2,2),np.uint8),np.eye(2,dtype=np.uint8),
     np.array([[0,1],[1,1]],np.uint8),np.array([[1,1],[1,0]],np.uint8))
def read(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def input_matches(path,side,matrices,P):
    lines=path.read_text().splitlines();ns,ms,K,lift=map(int,lines[0].split())
    H=matrices['HZ' if side=='X' else 'HX'];O=matrices['LZ' if side=='X' else 'LX']
    assert (2*ms,2*ns)==H.shape and lift==P and K==(O.shape[0]+63)//64
    assert len(lines)==ns+1
    rebuilt=np.zeros_like(H)
    for v,line in enumerate(lines[1:]):
        row=list(map(int,line.split()));assert len(row)==6+3*K
        seen=set()
        for j in range(3):
            c,a=row[2*j:2*j+2];assert 0<=c<ms and a in (1,2,3) and c not in seen;seen.add(c)
            rebuilt[2*c:2*c+2,2*v:2*v+2]=RHO[a]
        for a in (1,2,3):
            values=(O[:,2*v]*(a&1))^(O[:,2*v+1]*((a>>1)&1))
            expected=int.from_bytes(np.packbits(values,bitorder='little').tobytes(),'little')
            actual=sum(row[6+(a-1)*K+j]<<(64*j) for j in range(K));assert actual==expected
    assert np.array_equal(rebuilt,H)

def check_state(text,n):
    a=list(map(int,text.split()));cost,count=a[:2];pos=2;vals={}
    for _ in range(count):
        v,x=a[pos:pos+2];pos+=2;assert 0<=v<n and x in (1,2,3) and v not in vals;vals[v]=x
    bans=a[pos+1:];assert a[pos]==len(bans) and len(set(bans))==len(bans)
    assert all(0<=v<n and v not in vals for v in bans)
    assert cost==sum(2 if x==3 else 1 for x in vals.values())

def run_split(exe,inp,lim,root=None,state=None,n=None,depth=4):
    with tempfile.TemporaryDirectory(prefix='pp-split-') as td:
        td=Path(td);output=td/'frontier'
        if root is not None:cmd=[str(exe),'split',str(inp),str(lim),str(root[0]),str(root[1]),str(depth),str(output)]
        else:
            initial=td/'initial';initial.write_text(f'{n} 1\n{state}\n')
            cmd=[str(exe),'resplit',str(inp),str(lim),str(initial),str(depth),str(output)]
        result=json.loads(subprocess.check_output(cmd,text=True,timeout=120));assert not result['found']
        lines=output.read_text().splitlines();nn,count=map(int,lines[0].split());assert count==len(lines)-1
        return result,lines[1:]

def check_records(code,regenerate,compiled,tmp):
    cert=read(code/'distance/completed_certificate.json');meta=read(code/'metadata.json');D=code/'distance'
    assert cert['code_id']==meta['id'] and cert['distance']==meta['d'] and cert['limit']==meta['d']-1
    assert cert['matrix_sha256']==meta['matrix_sha256'] and verify(code)['passed']
    a=dict(np.load(code/'matrices.npz',allow_pickle=False));P=meta['P'];L=meta['L'];limit=cert['limit']
    for name,h in cert['evidence_files_sha256'].items():assert digest(D/name)==h,(meta['id'],name)
    engine=ROOT/cert['engine']['file'];assert digest(engine)==cert['engine']['sha256']
    for side,h in cert['input_sha256'].items():
        inp=D/f'distance_{side}.txt';assert digest(inp)==h;input_matches(inp,side,a,P)
    # Every cyclic root reduction must preserve both physical check spaces.
    shift=[2*(j*P+(t+1)%P)+b for j in range(L) for t in range(P) for b in range(2)]
    for key in ('HX','HZ'):assert set(rows_as_ints(a[key][:,shift]))==set(rows_as_ints(a[key]))
    if cert['sides']==['X']:
        perm=cert['xz_permutation'];assert sorted(perm)==list(range(meta['n']))
        assert all(perm[perm[i]]==i for i in range(meta['n']))
        assert set(rows_as_ints(a['HX'][:,perm]))==set(rows_as_ints(a['HZ']))
    else:assert cert['sides']==['X','Z']
    for u in cert['upper_witnesses']:
        support=u['binary_support'];assert len(support)==len(set(support))==u['weight']==cert['distance']
        assert all(0<=i<meta['n'] for i in support)
        vec=np.zeros(meta['n'],np.uint8);vec[support]=1
        H,O=('HZ','LZ') if u['side']=='X' else ('HX','LX')
        assert not np.any(a[H]@vec%2) and np.any(a[O]@vec%2)
    assert cert['upper_witnesses']
    if cert['kind']=='root_records':
        data=read(D/cert['lower_records']);seen=set()
        for record in data['records']:
            side,block,value=record['scope'];v=record['result']
            assert (side,block,value) not in seen;seen.add((side,block,value))
            assert v['limit']==limit and v['complete'] and not v['found'] and v['frontier_size']==0
            assert v['input_sha256']==cert['input_sha256'][side] and v['side']==side
        assert seen=={(side,b,value) for side in ('X','Z') for b in range(L) for value in (1,2,3)}
        return {'id':meta['id'],'distance':cert['distance'],'root_scopes':len(seen),'partition_regenerated':False}
    if cert['kind']=='whole_roots':
        lower=read(D/cert['lower_records']);total=3*L
        wrapper=cert['enumeration_wrapper'];assert digest(ROOT/wrapper['file'])==wrapper['sha256']
        schedule=None
        if cert.get('hard_root_schedule'):
            schedule=[s.split() for s in(D/cert['hard_root_schedule']).read_text().splitlines()]
        for side in ('X','Z'):
            history=lower['aggregate_record']['data']['sides'][side]['history']
            item=next(x for x in history if x['limit']==limit)
            assert not item['found_roots'] and not item.get('errors',[])
            follow=[x for x in lower['whole_root_followup_records'] if x['side_from_saved_task_schedule']==side]
            scopes=[]
            for f in follow:
                v=f['data'];assert v['limit']==limit and v['complete'] and not v['found'];scopes.append((v['block'],v['a']))
            assert len(scopes)==len(set(scopes)) and item['complete_roots']+len(scopes)==total
            if follow:
                scheduled={(int(b),int(value)) for case,s,lim,b,value in schedule if case==cert['historical_case_label'] and s==side and int(lim)==limit}
                assert set(scopes)==scheduled=={(0,1),(0,2)} and item['complete_roots']==total-2
        return {'id':meta['id'],'distance':cert['distance'],'root_scopes':2*total,'partition_regenerated':False,
                'coverage_evidence':'aggregate counts plus scheduled follow-ups' if schedule else 'all-root aggregate counts',
                'identity_level_coverage_independently_verified':False,
                'provenance':cert['root_coverage_provenance']}
    data=json.loads(gzip.decompress((D/cert['coverage']).read_bytes()));jobs={j['id']:j for j in data['jobs']};results={r['id']:r for r in data['results']}
    assert len(jobs)==len(data['jobs']) and len(results)==len(data['results']) and set(jobs)==set(results)
    for key,j in jobs.items():
        r=results[key];check_state(j['state'],j['n'])
        assert r['status']=='complete' and r['complete'] and not r['found'] and r['frontier_size']==0
        assert (r['limit'],r['block'],r['a'])==(limit,j['block'],j['a']) and j['limit']==limit
    exe=None
    if regenerate:
        key=cert['engine']['sha256']
        if key not in compiled:
            exe=tmp/key;subprocess.run(['c++','-O3','-std=c++17',str(engine),'-o',str(exe)],check=True,timeout=120);compiled[key]=exe
        exe=compiled[key]
    inp=D/'distance_X.txt';roots=set();seen=set();splits=0
    if cert['kind']=='legacy_split':
        for r in data['prior_roots']:
            root=(r['block'],r['a']);assert root not in roots and r['limit']==limit and r['complete'] and not r['found'];roots.add(root)
        for p in data['parents']:
            root=(p['block'],p['a']);assert root not in roots;roots.add(root);ids=p['child_ids']
            assert p['limit']==limit and len(ids)==len(set(ids))==p['count'] and not seen.intersection(ids);seen.update(ids)
            assert all((jobs[i]['block'],jobs[i]['a'])==root for i in ids)
            if regenerate:
                r,states=run_split(exe,inp,limit,root=root);assert states==[jobs[i]['state'] for i in ids] and r['nodes']==p['split_nodes'];splits+=1
        assert seen==set(jobs)
    else:
        assert cert['kind']=='refined_split';original=sorted(data['original_jobs'],key=lambda j:j['id']);ref={r['original_id']:r for r in data['refinements']}
        assert len(ref)==len(data['refinements'])==len(original) and set(ref)=={j['id'] for j in original}
        rootnodes={}
        for b in range(L):
            for value in (1,2,3):
                root=(b,value);roots.add(root)
                if regenerate:
                    r,states=run_split(exe,inp,limit,root=root);assert states==[j['state'] for j in original if(j['block'],j['a'])==root];rootnodes[root]=r['nodes'];splits+=1
        for j in original:
            r=ref[j['id']];ids=r['children'];assert not seen.intersection(ids);seen.update(ids)
            assert all(jobs[i]['original_prefix_id']==j['id'] and (jobs[i]['block'],jobs[i]['a'])==(j['block'],j['a']) for i in ids)
            if regenerate and r['resplit_nodes']:
                got,states=run_split(exe,inp,limit,state=j['state'],n=j['n'],depth=5);assert got['nodes']==r['resplit_nodes'];splits+=1
            else:states=[j['state']] if not r['resplit_nodes'] else None
            if states is not None:assert states==[jobs[i]['state'] for i in ids]
            if regenerate:rootnodes[j['block'],j['a']]+=r['resplit_nodes']
        assert seen==set(jobs)
        assert len(data['parents'])==3*L
        for p in data['parents']:
            root=(p['block'],p['a']);assert root in roots and set(p['children'])=={i for i,j in jobs.items() if(j['block'],j['a'])==root}
            if regenerate:assert rootnodes[root]==p['split_nodes']
    assert roots=={(b,value) for b in range(L) for value in (1,2,3)}
    return {'id':meta['id'],'distance':cert['distance'],'root_scopes':len(roots),'completed_leaves':len(jobs),'regenerated_splits':splits,'partition_regenerated':regenerate}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code');p.add_argument('--regenerate-partitions',action='store_true');p.add_argument('--json',type=Path);args=p.parse_args()
    codes=[ROOT/'codes'/args.code] if args.code else sorted(x.parent.parent for x in(ROOT/'codes').glob('*/distance/completed_certificate.json'))
    with tempfile.TemporaryDirectory(prefix='pp-distance-audit-') as td:
        compiled={};results=[check_records(c,args.regenerate_partitions,compiled,Path(td)) for c in codes]
    for r in results:print('PASS',r['id'],'d='+str(r['distance']))
    report={'all_passed':True,'scope':'saved-record verification, not exhaustive leaf reexecution','codes':results}
    if args.json:args.json.write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(results)}/{len(codes)} completed distance archives verified')
if __name__=='__main__':main()
