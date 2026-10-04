# [[512,128,13]] with integer overlap identity

J=3, L=8, P=32. Maximum binary check weight 10; maximum canonical basis weights 26/26. Symbol/binary girths 6/4.

`construction.json` gives every polynomial entry of both GF4 check matrices, both canonical seed families, the disjoint pivot/free-column partition, and the determinant inverses. `matrices.npz` specifies every entry of the four final binary matrices. `distance/` records exhaustive lower coverage through weight 12 and a separately verified weight-13 nontrivial logical operator. Run `python scripts/verify_all.py` from the repository root for binary CSS, rank, kernel, and canonical checks.
