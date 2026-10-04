# [[768,192,11]] with integer overlap identity

J=3, L=8, P=48. Maximum binary check weight 9; maximum canonical basis weights 27/27. Symbol/binary girths 6/6.

`construction.json` gives every polynomial entry of both GF4 check matrices, both canonical seed families, the disjoint pivot/free-column partition, and the determinant inverses. `matrices.npz` specifies every entry of the four final binary matrices. `distance/` records exhaustive lower coverage through weight 10 and a separately verified weight-11 nontrivial logical operator. Run `python scripts/verify_all.py` from the repository root for binary CSS, rank, kernel, and canonical checks.
