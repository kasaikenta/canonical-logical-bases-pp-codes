# Data format

Each code directory contains two required files.

`matrices.npz` stores four two-dimensional arrays with entries in `{0,1}`:

- `HX`: X-check matrix;
- `HZ`: Z-check matrix;
- `LX`: X-logical representatives;
- `LZ`: Z-logical representatives.

`metadata.json` records the stable code identifier, family, block parameters,
`[[n,k,d]]`, symbol/binary girths, check weights, check ranks, maximum logical
basis weights, Gram polynomial when applicable, exact-distance status, and
SHA-256 digests.  A digest is computed from the matrix's C-contiguous `uint8`
byte representation.

If present, `construction.json` gives the QC/polynomial inputs used before
binary expansion.  The exact fields depend on the family: the quaternary
single-CPM construction records exponent and coefficient arrays, pivot/free
column sets, and Gram data; the binary multi-CPM construction records its
sparse polynomial blocks and specialization.  The binary matrices remain the
authoritative common representation across families.

Weight histograms map the weight to its count, separately for each matrix.
For example, `check_column_weights_HX` describes the column counts of HX and
`basis_weights_LX` describes the row counts of LX. The complete histograms
for all four binary multi-CPM table instances are in
[multicpm-table-statistics.json](multicpm-table-statistics.json), with
[reading and reproduction instructions](multicpm-table-statistics.md).
