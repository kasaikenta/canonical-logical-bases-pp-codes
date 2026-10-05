"""Check archived exhaustive-search coverage bookkeeping and exact-distance witness."""
from pathlib import Path
import json,gzip,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
claim=json.loads((ROOT/'distance/distance-claim.json').read_text())
proof=json.loads(gzip.decompress((ROOT/'distance/stage19_certificate_audit.json.gz').read_bytes()))
cid=proof['candidate'];limit=claim['no_witness_through'];assert limit==19
active={f'{cid}_w{limit}_{side}_{b}_{a}' for side in ('X','Z') for b in range(8) for a in (1,2,3)}
processed=set();counts={}
for record in proof['terminal_and_split_records']:
 ident=record['id'];assert ident in active and ident not in processed
 processed.add(ident);active.remove(ident);status=record['status'];assert status in ('complete','queued','split');counts[status]=counts.get(status,0)+1
 for child in record['children']:
  if child.startswith(f'{cid}_w{limit+1}_'):assert status=='complete';continue
  assert child.startswith(f'{cid}_w{limit}_') and child not in active and child not in processed;active.add(child)
assert not active and counts==proof['root_tree_coverage_audit']['result_counts']
assert proof['certificate']['no_witness_through']==19 and proof['certificate']['roots']==48
for side in ('X','Z'):assert hashlib.sha256((ROOT/f'distance/distance_{side}.txt').read_bytes()).hexdigest()==claim['input_sha256'][side]
a=np.load(ROOT/'matrices.npz');w=claim['witness'];word=np.zeros(a['HX'].shape[1],dtype=np.uint16);seen=set()
for coord,val in w['word']:
 assert coord not in seen and val in (1,2,3);seen.add(coord);word[2*coord]=val&1;word[2*coord+1]=(val>>1)&1
check,opposite=('HZ','LZ') if w['side']=='X' else ('HX','LX')
assert int(word.sum())==20 and not np.any((a[check].astype(np.uint16)@word)%2) and np.any((a[opposite].astype(np.uint16)@word)%2)
assert claim['lower_bound']==claim['upper_bound']==claim['distance']==20
print('PASS: archived coverage has 48 completed roots, no unfinished branches through 19; verified nontrivial binary witness of weight 20')
