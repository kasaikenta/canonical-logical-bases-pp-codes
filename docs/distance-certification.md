# Exact-distance records

The catalog field `distance_status` distinguishes claimed exact values from
bounds. Exact distance requires both ingredients:

1. a nontrivial zero-syndrome representative of weight `d`; and
2. exhaustive exclusion of every nontrivial representative of weight below
   `d`, using the cyclic symmetry reduction described in the paper.

The compact records under `distance/` preserve the search coverage, witnesses,
and source hashes available for each experiment. Record coverage differs by
entry: a `distance-claim.json` status alone is not a distance certificate.
Saved execution records can be checked without repeating the exhaustive search;
they are computational evidence from the archived engine, not a formal proof
trace checked by an independent proof assistant.

## Completed records added in v1.0.10

The release repairs the incomplete public export for the six original small
examples, seven check-weight-nine examples, the `[[2048,512,24]]` example, and
the five L=10 examples with `(P,d)=(31,14),(37,13),(37,15),(41,13),(53,16)`. Their
`distance/completed_certificate.json` files identify the actual four matrices,
search inputs, archived engine source, upper witnesses and completed lower scope.
They supersede older partial records, which are explicitly marked as such.

Run from the repository root:

```bash
python3 scripts/verify_completed_distances.py --regenerate-partitions
```

This checks all 19 added evidence archives. It reconstructs every input check and
logical-pairing label from `matrices.npz`, checks cyclic automorphisms and any
X/Z exchange permutation, verifies actual nontrivial binary upper witnesses,
and checks saved completion evidence. For split searches, it compiles the saved
C++17 source in a temporary directory and regenerates every split frontier.
The P=128 instance covers 24 roots and 28,701 completed final prefixes through
weight 23. The L=10 records contain aggregate counts for 30 roots per side;
for P=53, saved follow-up records identify roots `(0,1)` and `(0,2)` on each side.
The original enumeration wrapper and actual follow-up schedule are archived.
The aggregate P=53 record does not retain the identities of its 28 completed
roots. Thus identifying the follow-ups as the two remaining roots depends on
the historical schedule, rather than an independently verifiable list of all
completed root identities. The validator reports this evidence level explicitly.

The historical unsplit L=10 records do not embed a per-run executable digest.
Their provenance comes from the archived source, executable records, saved
execution wrappers and input reconstruction. The exported certificates state
this limitation. Hashes recorded during archival must not be interpreted as
retroactive per-run signatures.

Without `--regenerate-partitions`, the command performs matrix, witness and
saved-record checks without compiling C++. Neither mode reexecutes the costly
leaf exclusions. A full rerun uses the archived engines and input files, and
must finish every required root at `d-1` without finding a logical operator.

The separately archived 22 girth-6 rechecks can be checked with
`python3 scripts/verify_girth6_rechecks.py`; their 704 physical-bit roots were
independently reexecuted before v1.0.9. The P=64 distance-20 overlap-identity
entry has its own `verify_distance.py` for the saved coverage and upper witness.

The [Table 1 evidence inventory](distance-evidence-inventory.json) maps every
current manuscript row to its archived evidence level. In addition to the
historical L=10 aggregate counts, the P=128 distance-20 overlap-identity entry
retains aggregate stage-completion records rather than every branch identity.
The inventory distinguishes these records from individually identified root
records and regenerable branch partitions.

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
