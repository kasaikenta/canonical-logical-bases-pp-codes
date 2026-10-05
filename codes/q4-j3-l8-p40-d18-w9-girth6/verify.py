#!/usr/bin/env python3
"""Standalone structural/witness verifier for an extracted individual code ZIP."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,permutations
import hashlib,json
P=Path(__file__).resolve().parent
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))

def load(name):return json.loads((P/name).read_text())
def bits(w):
    while w:
        b=w&-w;yield b.bit_length()-1;w^=b
def read(name):
    with (P/name).open() as f:
        assert f.readline().strip()=='%%MatrixMarket matrix coordinate integer general'
        lines=(s for s in f if s.strip() and not s.startswith('%'))
        nr,nc,nnz=map(int,next(lines).split());rows=[{} for _ in range(nr)]
        for s in lines:
            i,j,c=map(int,s.split());assert 1<=i<=nr and 1<=j<=nc and j-1 not in rows[i-1];rows[i-1][j-1]=c
        assert sum(map(len,rows))==nnz;return rows,nc
def expand(rows):
    out=[{} for _ in range(2*len(rows))]
    for i,row in enumerate(rows):
        for j,c in row.items():
            for b,a in enumerate((1,2)):
                v=MUL[c][a]
                for t in (0,1):
                    if v>>t&1:out[2*i+t][2*j+b]=1
    return out
def words(rows):return [sum(1<<j for j in row) for row in rows]
def rank(rows):
    piv={}
    for w in rows:
        while w:
            b=w.bit_length()-1
            if b not in piv:piv[b]=w;break
            w^=piv[b]
    return len(piv)
def pair(xs,zs,identity=False):
    for i,x in enumerate(xs):
        for j,z in enumerate(zs):assert (x&z).bit_count()%2==int(identity and i==j)
def graph(rows,n):
    cols=[[] for _ in range(n)];edges=defaultdict(list)
    for i,row in enumerate(rows):
        for j in row:cols[j].append(i)
    for j,col in enumerate(cols):
        for a,b in combinations(col,2):edges[a,b].append(j)
    assert all(len(v)==1 for v in edges.values()),'binary or symbol C4 present'
    neighbors=[{} for _ in rows]
    for (a,b),vs in edges.items():neighbors[a][b]=neighbors[b][a]=vs[0]
    has6=False
    for a in range(len(rows)):
        for b in neighbors[a]:
            if b<=a:continue
            for c in neighbors[a].keys()&neighbors[b].keys():
                if c>b and len({neighbors[a][b],neighbors[b][c],neighbors[c][a]})==3:has6=True;break
            if has6:break
        if has6:break
    assert has6
    hist=lambda xs:{str(x):y for x,y in sorted(Counter(xs).items())}
    return dict(row_weight_histogram=hist(map(len,rows)),column_weight_histogram=hist(map(len,cols)),girth=6)
def input_text(h,dual,n,N):
    es=[[] for _ in range(n)];ds=[0]*(2*n)
    for i,row in enumerate(h):
        for j,c in row.items():es[j].append((i,c))
    for i,w in enumerate(dual):
        for j in bits(w):ds[j]|=1<<i
    blocks=(len(dual)+63)//64;out=[f'{n} {len(h)} {len(dual)} {N}']
    out+=[' '.join(str(v) for e in sorted(x) for v in e) for x in es]
    for j in range(n):
        for w in (ds[2*j],ds[2*j+1],ds[2*j]^ds[2*j+1]):out.append(' '.join(str(w>>(64*b)&((1<<64)-1)) for b in range(blocks)))
    return '\n'.join(out)+'\n'
def main():
    summary=load('summary.json');construction=load('construction.json');N=summary['N'];n=summary['n'];k=summary['k'];d=summary['d']
    shifts=[construction['Hx_shifts'],construction['Hz_shifts']];fr=construction['canonical']
    assert (n,k)==(16*N,4*N);hs=[];hb=[];lb=[]
    for side in 'xz':
        h,nc=read(f'H{side}_symbol.mtx');b,nb=read(f'H{side}_binary.mtx');l,nl=read(f'L{side}_symbol.mtx');bl,nbl=read(f'L{side}_binary.mtx')
        assert nc==nl==8*N and nb==nbl==n and b==expand(h)
        s='xz'.index(side)
        expected_h=[{c*N+(t-shifts[s][i][c])%N:(2 if c==4*s+i else 1) for c in range(8)} for i in range(3) for t in range(N)]
        assert h==expected_h
        expected_l=[{c*N+(t+e)%N:a for c,poly in enumerate(seed) for e,a in poly} for seed in fr[side.upper()] for t in range(N)]
        assert l==expected_l
        hs.append(h);hb.append(words(b));lb.append(words(bl));assert rank(hb[-1])==6*N and len(lb[-1])==k
        expected=[sum(MUL[c][a]<<(2*j) for j,c in row.items()) for seed in range(2) for a in (1,2) for row in l[seed*N:(seed+1)*N]]
        assert expected==lb[-1]
        for label,rows,size in [('symbol',h,nc),('binary',b,nb)]:
            g=graph(rows,size)
            for key,v in g.items():assert v==summary['graphs'][side][label][key]
    pair(*hb);pair(lb[0],hb[1]);pair(lb[1],hb[0]);pair(*lb,True)
    coeff=lambda s,i,c:2 if c==4*s+i else 1
    for i in range(3):
        for j in range(3):
            pairs=construction['matching'][i][j];assert sorted(c for p in pairs for c in p)==list(range(8))
            for a,b in pairs:
                assert (shifts[0][i][a]-shifts[1][j][a]-shifts[0][i][b]+shifts[1][j][b])%N==0
                assert MUL[coeff(0,i,a)][coeff(1,j,a)]==MUL[coeff(0,i,b)][coeff(1,j,b)]
    def determinant(s,cols):
        out={}
        for perm in permutations(cols):
            e=sum(shifts[s][i][perm[i]] for i in range(3))%N;a=1
            for i in range(3):a=MUL[a][coeff(s,i,perm[i])]
            out[e]=out.get(e,0)^a
        return {e:a for e,a in out.items() if a}
    dx=determinant(0,fr['A']);dz=determinant(1,fr['B']);gram={}
    for e,a in dz.items():
        for f,b in dx.items():
            t=(f-e)%N;gram[t]=gram.get(t,0)^MUL[a][b]
    assert sorted([e,a] for e,a in gram.items() if a)==fr['Gram']
    assert max(w.bit_count() for rows in lb for w in rows)==summary['canonical_Wmax']
    detectors=lb
    if summary.get('distance_detector_basis_transfer'):
        detectors=[]
        for s,side in enumerate('xz'):
            rows,size=read(f'distance/L{side}_audit_detectors.mtx');assert size==n and len(rows)==k
            detectors.append(words(rows))
            assert rank(hb[s]+detectors[s])==rank(hb[s]+lb[s])==rank(hb[s]+detectors[s]+lb[s])==10*N
        pair(detectors[0],hb[1]);pair(detectors[1],hb[0]);pair(*detectors,True)
    lower=[];upper=[]
    for s,side in enumerate('XZ'):
        claim=summary['distance'][side];lo=load(claim['exclusion_file']);hi=load(claim['upper_file'])
        root_count=16 if lo.get('engine')=='physical_binary_bit_branching_v1' else 24
        assert lo['complete_exclusion'] and not lo['timed_out'] and lo['completed_roots']==lo['total_roots']==root_count
        if lo.get('partition_files'):
            parts=[load('distance/'+name) for name in lo['partition_files']]
            assert sorted((r['root_first'],r['root_last']) for r in parts)==[(i,i+1) for i in range(root_count)]
            assert all(r['complete_exclusion'] and not r['timed_out'] and r['bound']==lo['bound'] for r in parts)
        lower.append(lo['bound']+1);w=sum(1<<j for j in hi['binary_support']);upper.append(w.bit_count());assert w.bit_count()==hi['binary_weight']
        pair([w],hb[1-s]);assert rank(hb[s]+[w])==6*N+1
        assert (P/f'distance/{side}_input.txt').read_text()==input_text(hs[1-s],detectors[1-s],8*N,N)
    assert min(lower)>=d and min(upper)==d
    for name,sha in load('manifest.json').items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha
    print(f'PASS [[{n},{k},{d}]]: matrices, CSS, ranks, complete conjugate basis, weights, both girths, witnesses, inputs, exclusion coverage, hashes')
    print('Exclusion-log consistency checked. This invocation does not rerun exhaustive distance searches.')
if __name__=='__main__':main()
