#!/usr/bin/env python3
"""Audit the 22 independent distance rechecks against their actual binary matrices."""
import hashlib,json
from pathlib import Path
import numpy as np
from verify_all import verify,sha256_matrix
ROOT=Path(__file__).resolve().parents[1]
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit(code):
 meta=json.loads((code/'metadata.json').read_text());certpath=code/meta['three_mac_distance_recheck'];c=json.loads(certpath.read_text());r=certpath.parent
 assert verify(code)['passed'];m=dict(np.load(code/'matrices.npz',allow_pickle=False));n,k,d=meta['n'],meta['k'],meta['d'];assert c['exact_quantum_distance']==d
 assert c['matrix_sha256']==meta['matrix_sha256'];assert sha(ROOT/c['source_file'])==c['source_sha256']
 checked=[]
 for side,H,op,stab in [('X','HZ','LZ','HX'),('Z','HX','LX','HZ')]:
  inp=r/(side+'_input.txt');st=r/(side+'_stabilizers.txt');data=list(map(int,inp.read_text().split()));ns,ms,kk,P=data[:4];assert (ns,ms,kk,P)==(n//2,m[H].shape[0]//2,k,meta['P'])
  edge=data[4:4+6*ns];binary=np.zeros_like(m[H])
  for v in range(ns):
   for j in range(3):
    row,coeff=edge[6*v+2*j:6*v+2*j+2];assert 0<=row<ms and 1<=coeff<=3
    for a in range(2):
     z=MUL[coeff][1<<a]
     for b in range(2):binary[2*row+b,2*v+a]^=(z>>b)&1
  assert np.array_equal(binary,m[H])
  labels=data[4+6*ns:];nb=(k+63)//64;assert len(labels)==3*ns*nb
  for v in range(ns):
   for a in (1,2,3):
    vals=(m[op][:,2*v]*(a&1))^(m[op][:,2*v+1]*((a>>1)&1));raw=np.packbits(vals,bitorder='little').tobytes();raw+=bytes((-len(raw))%8)
    expected=[int.from_bytes(raw[q:q+8],'little') for q in range(0,len(raw),8)];assert labels[(3*v+a-1)*nb:(3*v+a)*nb]==expected
  tok=list(map(int,st.read_text().split()));nr,nn=tok[:2];assert (nr,nn)==m[stab].shape;idx=2
  for row in m[stab]:
   w=tok[idx];idx+=1;assert tok[idx:idx+w]==list(np.flatnonzero(row));idx+=w
  assert idx==len(tok)
  # Cyclic QC automorphism must preserve both check spaces before reducing roots.
  perm=[2*(j*P+(t+1)%P)+b for j in range(8) for t in range(P) for b in range(2)]
  def words(a):return {np.packbits(x,bitorder='little').tobytes() for x in a}
  for h in ['HX','HZ']:assert words(m[h][:,perm])==words(m[h])
  ss=c['sides'][side];assert ss['limit']==d-1 and ss['lower_bound']==d and ss['completed_roots']==16 and sha(inp)==ss['input_sha256'] and sha(st)==ss['stabilizer_sha256']
  for root in range(16):
   x=json.loads((r/(side+'_r'+str(root).zfill(2)+'.json')).read_text());t=x['task'];a=x['result'];assert x['passed'] and x['returncode']==0 and x['source_sha256']==c['source_sha256'];assert t['code_id']==meta['id'] and t['side']==side and t['root']==root and t['limit']==d-1
   assert t['input_sha256']==ss['input_sha256'] and t['stabilizer_sha256']==ss['stabilizer_sha256'];assert a['complete_exclusion'] and not a['timed_out'] and not a['found'];assert (a['root_first'],a['root_last'],a['completed_roots'],a['total_roots'],a['full_total_roots'],a['bound'])==(root,root+1,1,1,16,d-1);checked.append((side,root))
 upper=[]
 for side,H,op in [('X','HZ','LZ'),('Z','HX','LX')]:
  x=json.loads((code/'distance'/(side+'_upper_word.json')).read_text());b=np.zeros(n,np.uint8);b[x['binary_support']]=1;assert int(b.sum())==x['binary_weight'];assert not np.any((m[H]@b)&1) and np.any((m[op]@b)&1);upper.append(int(b.sum()))
 assert len(set(checked))==32 and min(upper)==d
 return {'id':meta['id'],'passed':True,'exact_distance':d,'complete_roots':32,'input_matches_current_basis':True}
if __name__=='__main__':
 codes=[p for p in (ROOT/'codes').iterdir() if (p/'metadata.json').exists() and 'three_mac_distance_recheck' in json.loads((p/'metadata.json').read_text())]
 results=[audit(p) for p in sorted(codes)];assert len(results)==22
 for x in results:print('PASS',x['id'],'d='+str(x['exact_distance']))
 print('22/22 exact-distance rechecks audited; 704 disjoint roots.')
