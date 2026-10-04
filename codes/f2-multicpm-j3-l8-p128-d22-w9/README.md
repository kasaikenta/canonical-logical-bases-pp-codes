# Binary multi-CPM example: `[[1024,256,22]]`

This directory gives the complete explicit example associated with the binary
multi-CPM--PP extension.  The paper retains the general construction and its
weight bounds; this page records the instance-specific formulas, matrices,
canonical basis, and exact-distance evidence.

## Formal family

Work in

```text
A = GF(2)[U,U^{-1},T]/(T^2-1),  U* = U^{-1},  T* = T.
```

The two formal QC checks are

```text
H_X = [ U^-6+1       1               1                 1       1          1          1           1
        1            U^3+T U^5       U                 T U^-3  U^14       T U^8      T U^-13     T U^2
        1            U^11            T U^10+T U^13     U^-3    U^8        T U^29     U^5         U^15 ]

H_Z = [ 1            U^14            T U^19            1+U^6   U^14       T U^19     U^5         U^5
        1            T U^-3          T U^8             T U^-3 U^6+T U^8 U^15       1           U^15
        1            U^3             U^-13             U^-3    1          U^3+U^6    U^-13       U^-3 ].
```

The PP parent is obtained by deleting `U^-6`, `T U^5`, and `T U^10`
from X blocks `(0,0)`, `(1,1)`, and `(2,2)`, and deleting `U^6` from Z
blocks `(0,3)`, `(1,4)`, and `(2,5)`.  Indices start at zero.  Its pair
partitions are

```text
M1 = {03,14,25,67}    M2 = {06,13,24,57}
M3 = {04,15,26,37}    M4 = {01,24,36,57}
M5 = {07,15,26,34}

[ M1 M2 M3 ]
[ M3 M1 M4 ]
[ M2 M5 M1 ].
```

Here `ab` denotes the unordered pair `{a,b}`.  Substitution verifies both the
PP parent identities and the multi-CPM addition condition.

## Pivots and canonical normalization

Choose

```text
A = (1,2,7),   B = (4,5,6),   I = (0,3).
```

The selected determinants are

```text
Delta_X  = U^16 + T U^16 + T U^20 = T U^20 F,
Delta_Z  = T U^12 + U^16 + T U^16,
Delta_Z* = T U^-12 F,
F        = 1 + (1+T)U^-4,   F^2 = 1,
g        = Delta_Z* Delta_X = U^8.
```

Because `(1+T)^2=0`, `F` is its own inverse.  Both pivot minors are units,
and the Gram normalization is a pure cyclic shift after each even-`P`
specialization `U=z^h`, `T=z^(P/2)`.  The two free-column seed types have
formal weights `(30,33)` on the X side and `(33,30)` on the Z side.  These
values use cancellations in the explicit determinants.

The machine-readable version of this construction, including the formal
`H_X`, `H_Z`, `L_X`, and `L_Z` entries, is in
[`construction.json`](construction.json).

## Fixed specialization

For `P=128` and `h=1`:

| quantity | value |
|---|---:|
| parameters | `[[1024,256,22]]` |
| check size | `384 x 1024` on each side |
| check rank | 384 on each side |
| maximum row weight | 9 |
| girth | 6 on each side |
| column weights | 640 columns of weight 3; 384 of weight 4 |
| canonical pairs | 256 |
| basis weights | 128 pairs of `(30,33)` and 128 of `(33,30)` |
| matched-pair support intersection | one physical qubit |

The authoritative final matrices are in [`matrices.npz`](matrices.npz).
Their dimensions and SHA-256 hashes are recorded in
[`metadata.json`](metadata.json).

## Exact distance

The fixed specialization has `d_X=d_Z=22`.  The archived exhaustive searches
exclude every nontrivial logical operator of weight at most 21, and the
weight-22 witness has zero syndrome and lies outside the relevant stabilizer
space.  All eight QC block roots are covered; root zero is split into its eight
first branches.  The checked X/Z exchange transfers the lower bound to the
opposite side.

The exact-distance summary is [`distance/exact_distance.json`](distance/exact_distance.json),
the upper witness is [`distance/upper_witness22.json`](distance/upper_witness22.json),
and the archived coverage records are in [`distance/`](distance/).  This
distance claim applies to this fixed `P=128`, `h=1` specialization.

## Verification

From the repository root, run

```bash
python3 scripts/verify_all.py
```

This checks the matrix hashes, CSS commutation, both logical kernel
conditions, canonical pairing, ranks, and weight summaries over `GF(2)`.
