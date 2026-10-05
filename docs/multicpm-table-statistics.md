# Detailed statistics for the binary multi-CPM table

The paper shows column weights `3,4` and maximum canonical-basis weights
`33/33`. The counts below apply separately to X and Z.

| P | Columns of weight 3 | Columns of weight 4 | Basis vectors of weight 30 | Basis vectors of weight 33 |
|---:|---:|---:|---:|---:|
| 56 | 280 | 168 | 56 | 56 |
| 66 | 330 | 198 | 66 | 66 |
| 72 | 360 | 216 | 72 | 72 |
| 128 | 640 | 384 | 128 | 128 |

All check rows have weight 9; each side has `3P` rows. Each complete
canonical basis has `2P` rows.

The full numerical report is [multicpm-table-statistics.json](multicpm-table-statistics.json).
It includes all weight histograms, matrix hashes, both check and basis ranks,
CSS and kernel conditions, canonical pairing, binary girths, and maximum
integer support overlaps. The four matrix hashes for every specialization
match the archived matrices used for the paper.

The [formal family](../codes/f2-multicpm-j3-l8-p128-d22-w9/README.md)
is specialized with `U=z` and `T=z^(P/2)`. From the repository root, reproduce
the statistics and optionally export all four binary matrices for each P:

```bash
python3 scripts/describe_multicpm_table.py --json /tmp/multicpm-statistics.json --matrix-dir /tmp/multicpm-matrices
```

This command verifies the matrix identities and displayed weight statistics.
It does not rerun the exhaustive minimum-distance searches.
