# Exact-distance records

The catalog field `distance_status` distinguishes exact values from bounds.
Every entry in the paper table is marked `exact` only when both ingredients
are archived:

1. a nontrivial zero-syndrome representative of weight `d`; and
2. exhaustive exclusion of every nontrivial representative of weight below
   `d`, using the cyclic symmetry reduction described in the paper.

The compact records under `distance/` preserve the claimed value, search
coverage, witness location, and source hashes available for the corresponding
experiment.  Some historical searches produced large per-worker traces; those
traces are summarized rather than duplicated here.  The final matrices and
the compact certificates are keyed by stable code identifier and SHA-256
digest so that a separately archived full trace can be matched unambiguously.

Distance is a property of the fixed binary matrices in `matrices.npz`; a
family-level construction recipe does not by itself certify the distance of
all lift sizes.

## Re-running the added GF4 searches

The binary metric assigns costs 1, 1, and 2 to field values 1, 2, and 3.
`distance_X.txt` and `distance_Z.txt` encode the three incident GF4 checks
and binary logical-pairing labels for each symbol. Both input kernels and
all pairing labels of the 25 additions were independently compared with
the four stored binary matrices. Cyclic shifts reduce each side to 24 roots
for J=3, L=8.

Compile the engine with `c++ -O3 -std=c++17 scripts/distance_resume.cpp
-o /tmp/pp-distance`. For an input file INPUT, weight limit W, block index B
in 0,...,7, and nonzero field value A in 1,...,3, initialize a frontier with
`/tmp/pp-distance split INPUT W B A 1 FRONTIER` and resume it with
`/tmp/pp-distance run INPUT W FRONTIER SECONDS FRONTIER`. The 24 root scopes
per side must all complete at W=d-1. Incomplete frontiers preserve the exact
remaining scope and can be partitioned without overlap. A `found` result
provides a candidate upper witness; the archived binary witness check tests
zero syndrome and a nonzero pairing with the opposite complete logical basis.
For the exact-distance-18 instance, its evidence archive can be extracted into
a separate directory and checked using `python verify_exact18.py`.
