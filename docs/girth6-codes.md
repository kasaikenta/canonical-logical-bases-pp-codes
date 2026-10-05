# GF(4) CPM--PP codes with binary girth 6

These 22 fixed constructions have J=3, L=8, rate 1/4, symbol girths 6/6, binary girths 6/6, maximum binary check-row weight 9, and binary column weights 3/4. All distances refer to physical binary qubits. The maximum support intersections distinguish equal and unequal logical indices; canonicality requires parity, and does not require an integer intersection of one.

| P | [[n,k,d]] | Max. basis weight X/Z | Max. overlap equal/unequal |
|---:|---|---:|---:|
| 13 | [`[[208,52,10]]`](../codes/q4-j3-l8-p13-d10-w9-girth6/README.md) | 24/24 | 1/2 |
| 15 | [`[[240,60,11]]`](../codes/q4-j3-l8-p15-d11-w9-girth6/README.md) | 35/35 | 1/2 |
| 16 | [`[[256,64,11]]`](../codes/q4-j3-l8-p16-d11-w9-girth6/README.md) | 28/28 | 3/4 |
| 16 | [`[[256,64,12]]`](../codes/q4-j3-l8-p16-d12-w9-girth6/README.md) | 27/27 | 1/2 |
| 18 | [`[[288,72,10]]`](../codes/q4-j3-l8-p18-d10-w9-girth6/README.md) | 22/22 | 1/2 |
| 18 | [`[[288,72,12]]`](../codes/q4-j3-l8-p18-d12-w9-girth6/README.md) | 22/22 | 1/2 |
| 20 | [`[[320,80,11]]`](../codes/q4-j3-l8-p20-d11-w9-girth6/README.md) | 26/26 | 1/2 |
| 20 | [`[[320,80,13]]`](../codes/q4-j3-l8-p20-d13-w9-girth6/README.md) | 33/33 | 1/4 |
| 22 | [`[[352,88,11]]`](../codes/q4-j3-l8-p22-d11-w9-girth6/README.md) | 24/24 | 1/2 |
| 22 | [`[[352,88,13]]`](../codes/q4-j3-l8-p22-d13-w9-girth6/README.md) | 24/24 | 1/2 |
| 22 | [`[[352,88,14]]`](../codes/q4-j3-l8-p22-d14-w9-girth6/README.md) | 26/26 | 1/2 |
| 26 | [`[[416,104,15]]`](../codes/q4-j3-l8-p26-d15-w9-girth6/README.md) | 28/28 | 1/2 |
| 28 | [`[[448,112,15]]`](../codes/q4-j3-l8-p28-d15-w9-girth6/README.md) | 27/27 | 1/2 |
| 28 | [`[[448,112,16]]`](../codes/q4-j3-l8-p28-d16-w9-girth6/README.md) | 27/27 | 1/2 |
| 30 | [`[[480,120,14]]`](../codes/q4-j3-l8-p30-d14-w9-girth6/README.md) | 24/24 | 1/2 |
| 36 | [`[[576,144,17]]`](../codes/q4-j3-l8-p36-d17-w9-girth6/README.md) | 32/32 | 1/4 |
| 40 | [`[[640,160,18]]`](../codes/q4-j3-l8-p40-d18-w9-girth6/README.md) | 29/29 | 1/6 |
| 40 | [`[[640,160,19]]`](../codes/q4-j3-l8-p40-d19-w9-girth6/README.md) | 32/32 | 1/6 |
| 44 | [`[[704,176,20]]`](../codes/q4-j3-l8-p44-d20-w9-girth6/README.md) | 32/32 | 1/6 |
| 48 | [`[[768,192,18]]`](../codes/q4-j3-l8-p48-d18-w9-girth6/README.md) | 28/28 | 1/2 |
| 48 | [`[[768,192,19]]`](../codes/q4-j3-l8-p48-d19-w9-girth6/README.md) | 33/33 | 1/4 |
| 64 | [`[[1024,256,20]]`](../codes/q4-j3-l8-p64-d20-w9-girth6/README.md) | 32/32 | 1/6 |

## Fixed data and independent verification

Each directory includes the CPM exponents, GF(4) coefficient placement, pair partitions, pivot sets, pairing polynomial, canonical polynomial seeds, eight Matrix Market files, and the four final binary matrices in `matrices.npz`. An invertible nonmonomial pairing polynomial is displayed as `unit` in the paper table; its full coefficients are saved in `construction.json`.

The original records and the new replay are kept separate. All 22 exact quantum distances were independently reexecuted on three Macs, completing all 16 physical-bit symmetry roots on each CSS side: 704 roots in total, with no timeout, failure, or duplicate ownership. The replay inspected 8672238859 search nodes. Each completed exclusion through d-1, together with a checked weight-d nontrivial logical operator, establishes the stated exact distance. Individual X and Z distances can differ; their original intervals are recorded in `summary.json`.

The replay inputs were reconstructed directly from the supplied matrices. The historical distance detector for the P=40,d=18 instance uses a different complete basis; its quotient completeness was checked, and the new replay uses the currently supplied opposite basis. Both check spaces were explicitly checked invariant under the cyclic coordinate shift before symmetry reduction. A root is completed only when its full subtree has finished.

Audit matrices, rebuilt inputs, root coverage, witnesses, and source/matrix hashes:

```sh
python3 scripts/verify_all.py
python3 scripts/verify_girth6_rechecks.py
```

Reexecute the distance exclusion for one code in a separate output directory:

```sh
python3 scripts/replay_girth6_distance.py \
  --code q4-j3-l8-p64-d20-w9-girth6 --jobs 8 --seconds 600 \
  --output /tmp/pp-girth6-distance-replay
```

Use `--all` instead of `--code` for all 22 instances. Existing completed roots in the same output directory are reused only when their scope and input/source hashes match. A timeout is reported as incomplete and never treated as a distance proof. The original evidence files are never overwritten.

The C++17 engine is in `scripts/physical_binary_distance.cpp`. It branches on physical binary bits, applies only sound parity, packing, and stabilizer-coset minimality pruning, and uses a complete opposite logical basis to recognize nontriviality. Cyclic symmetry reduces the root set to two physical-bit roots per base column, 16 per side. Unlike symbol branching, this represents coefficient omega+1 by selecting both physical bits. The supporting full-scope records are in each `distance/three_mac_recheck/` directory.
