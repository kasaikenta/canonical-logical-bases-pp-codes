# Canonical logical bases from pair-partition codes

This repository is the reproducibility companion to **Low-Weight Canonical
Logical Bases from Pair-Partition Codes** by Koki Okada and Kenta Kasai.  It
contains the final binary check matrices and complete canonical logical bases
for the codes reported in the paper and additional fully documented examples.

## Contents

- `catalog/codes.csv` and `catalog/codes.json`: one row per archived code.
- `codes/<code-id>/matrices.npz`: `HX`, `HZ`, `LX`, and `LZ` as binary NumPy
  arrays.  These matrices are the authoritative, lossless code descriptions.
- `codes/<code-id>/metadata.json`: parameters, weights, girths, Gram data,
  source recipe status, exact-distance status, and matrix hashes.
- `codes/<code-id>/construction.json`: polynomial/QC construction data when
  archived in structured form.
- `codes/<code-id>/distance/`: compact exact-distance certificate records and
  witnesses when available.
- `scripts/verify_all.py`: independently checks dimensions, ranks, CSS
  commutation, logical kernel conditions, and canonical pairing over GF(2).

The binary multi-CPM example moved out of the paper appendix is documented in
[`codes/f2-multicpm-j3-l8-p128-d22-w9/README.md`](codes/f2-multicpm-j3-l8-p128-d22-w9/README.md).
That page gives the formal family, PP parent, pair partitions, pivot minors,
canonical normalization, fixed specialization, and exact-distance records.
An alternate complete basis for the quaternary `[[640,160,11]]` code is in
[`codes/q4-j3-l8-p40-d11-w9/basis_variants/systematic-overlap10/README.md`](codes/q4-j3-l8-p40-d11-w9/basis_variants/systematic-overlap10/README.md).
It has maximum representative weights 27/27 and integer support overlap I_160,
with the same checks and exact distance as the original weight-25/25 basis.
Its standalone verifier checks the unchanged checks, completeness, and integer
support-overlap identity.

Three additional connected quaternary CPM--PP codes have exact distance 13,
maximum binary check weight 10, and complete canonical bases of maximum
weights 26/26 with integer support overlap equal to an identity matrix:
[`[[384,96,13]]`](codes/q4-j3-l8-p24-d13-w10/README.md),
[`[[512,128,13]]`](codes/q4-j3-l8-p32-d13-w10/README.md), and
[`[[640,160,13]]`](codes/q4-j3-l8-p40-d13-w10/README.md).
Their symbol girths are 6/6 and binary girths 4/4. Each directory contains
all polynomial data, final matrices, and compact exact-distance records.

The catalog also contains the verified `P=52` instance and the dependent
four-block-row presentations listed in the paper's appendix table.

The compressed matrices are sufficient to reconstruct every displayed CSS
code and its canonical basis without relying on private documents.  Structured
construction files additionally reproduce the polynomial/QC route used to
obtain the matrices.

## Quick verification

Python 3.10 or later and NumPy are sufficient.

```bash
python3 scripts/verify_all.py
```

The verifier checks, for every entry,

```text
HX HZ^T = 0,
HZ LX^T = 0,
HX LZ^T = 0,
LX LZ^T = I,
rank(HX) = rank(HZ) = (n-k)/2,
rank(LX) = rank(LZ) = k.
```

It also checks the matrix SHA-256 digests and the row/column-weight summaries
recorded in `metadata.json`.

## File convention

All products in the verifier are over GF(2).  Rows of `LX` and `LZ` are paired
in the same order.  Thus row `i` of `LX` anticommutes with row `i` of `LZ` and
commutes with every other row of the opposite basis.

See [docs/format.md](docs/format.md) for the complete schema and
[docs/distance-certification.md](docs/distance-certification.md) for the scope
of the archived exact-distance records.

## Citation

Please cite the paper and the archived release identified in `CITATION.cff`.

## License

Code is released under the MIT License.  Numerical data are released under
CC0-1.0; see `DATA-LICENSE`.
