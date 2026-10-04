"""Standalone binary verifier; requires Python 3.10+ and NumPy."""
from pathlib import Path
import hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
recipe=json.loads((HERE/'construction.json').read_text())
with np.load(HERE/'matrices.npz',allow_pickle=False) as f:
    mats={key:np.asarray(f[key],dtype=np.uint8) for key in ('HX','HZ','LX','LZ')}
with np.load(HERE.parent.parent/'matrices.npz',allow_pickle=False) as f:
    for key in ('HX','HZ'):assert np.array_equal(mats[key],f[key])
def bitrows(a):
    return [int.from_bytes(row.tobytes(),'little') for row in np.packbits(a,axis=1,bitorder='little')]
def rank(rows):
    piv={}
    for row in rows:
        while row:
            col=row.bit_length()-1
            if col in piv:row^=piv[col]
            else:piv[col]=row;break
    return len(piv)
for key,a in mats.items():
    assert np.all(a<=1)
    assert hashlib.sha256(a.tobytes()).hexdigest()==recipe['binary_matrix_sha256'][key]
    assert a.shape==((240,640) if key.startswith('H') else (160,640))
HX,HZ,LX,LZ=[bitrows(mats[key]) for key in ('HX','HZ','LX','LZ')]
assert rank(HX)==rank(HZ)==240 and rank(LX)==rank(LZ)==160
assert 640-rank(HX)-rank(HZ)==160
assert all((x&z).bit_count()%2==0 for x in HX for z in HZ)
assert all((x&z).bit_count()%2==0 for x in LX for z in HZ)
assert all((x&z).bit_count()%2==0 for x in HX for z in LZ)
assert all((x&z).bit_count()==int(i==j) for i,x in enumerate(LX) for j,z in enumerate(LZ))
assert max(row.bit_count() for row in HX+HZ)==9
assert max(row.bit_count() for row in LX)==max(row.bit_count() for row in LZ)==27
witness=json.loads((HERE.parent.parent/'distance/distance_result.json').read_text())['witness']
mask=sum(value<<(2*coordinate) for coordinate,value in witness['word'])
assert mask.bit_count()==11
assert all((mask&row).bit_count()%2==0 for row in HX)
assert any((mask&row).bit_count()%2 for row in LX)
print('Verified [[640,160,11]] basis variant: unchanged checks; complete canonical basis; integer overlap I_160; maximum weights 27/27.')
