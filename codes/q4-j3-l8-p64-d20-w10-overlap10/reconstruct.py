"""Reproduce the archived GF(4) cofactor construction and all binary matrices."""
from pathlib import Path
import json,itertools,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
RHO=(np.zeros((2,2),dtype=np.uint8),np.eye(2,dtype=np.uint8),np.array([[0,1],[1,1]],dtype=np.uint8),np.array([[1,1],[1,0]],dtype=np.uint8))
c=json.loads((ROOT/'construction.json').read_text());P=int(c['P']);L=int(c['L'])
def add(*items):
 out={}
 for item in items:
  for e,a in item.items():out[e]=out.get(e,0)^a
 return {e:a for e,a in out.items() if a}
def mul(a,b):
 out={}
 for e,x in a.items():
  for f,y in b.items():
   pos=(e+f)%P;out[pos]=out.get(pos,0)^MUL[x][y]
 return {e:x for e,x in out.items() if x}
def prod(items):
 out={0:1}
 for item in items:out=mul(out,item)
 return out
def det(H,cols):return add(*(prod([H[i][cols[t[i]]] for i in range(len(H))]) for t in itertools.permutations(range(len(cols)))))
def inv_monomial(a):
 assert len(a)==1
 e,x=next(iter(a.items()));return {(-e)%P:(0,1,3,2)[x]}
def seeds(H,cols,free):
 d=det(H,cols);inv=inv_monomial(d);out=[]
 for a in free:
  v=[{} for _ in range(L)];v[a]=d
  for t,b in enumerate(cols):cc=list(cols);cc[t]=a;v[b]=det(H,cc)
  out.append([mul(p,inv) for p in v])
 return out
HX4=[[{int(c['E'][i][j]):int(c['CX'][i][j])} for j in range(L)] for i in range(c['J'])]
HZ4=[[{int(c['D'][i][j]):int(c['CZ'][i][j])} for j in range(L)] for i in range(c['J'])]
A,B,I=c['A'],c['B'],c['I'];X=seeds(HZ4,B,I);Z=seeds(HX4,A,I)
def check_rows(H):
 out=np.zeros((len(H)*2*P,L*2*P),dtype=np.uint8)
 for i,row in enumerate(H):
  for j,p in enumerate(row):
   for e,a in p.items():
    for t in range(P):out[2*(i*P+t):2*(i*P+t)+2,2*(j*P+(t-e)%P):2*(j*P+(t-e)%P)+2]^=RHO[a]
 return out
def logical_rows(V):
 out=np.zeros((len(V)*2*P,L*2*P),dtype=np.uint8)
 for i,v in enumerate(V):
  for j,p in enumerate(v):
   for e,a in p.items():
    for t in range(P):out[2*(i*P+t):2*(i*P+t)+2,2*(j*P+(t+e)%P):2*(j*P+(t+e)%P)+2]^=RHO[a].T
 return out
mat={'HX':check_rows(HX4),'HZ':check_rows(HZ4),'LX':logical_rows(X),'LZ':logical_rows(Z)}
archive=np.load(ROOT/'matrices.npz');meta=json.loads((ROOT/'metadata.json').read_text())
for name,a in mat.items():
 assert np.array_equal(a,archive[name]),name
 assert hashlib.sha256(a.tobytes()).hexdigest()==meta['matrix_sha256'][name]
print('PASS: all four matrices reproduced entry by entry from E,D,CX,CZ and A,B,I')
