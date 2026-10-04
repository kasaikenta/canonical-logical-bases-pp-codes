# GF(4) CPM--PP [[640,160,13]] with integer support overlap I

J=3, L=8, P=40. Maximum binary check-row weight 10; GF4 symbol girth 6/6;
binary Tanner girth 4/4; binary column weights 3,4,6. The complete canonical
bases have maximum row weights 26/26 and integer support overlap I_160.
Each side has 40 rows of weight 24, 40 of weight 25, and 80 of weight 26.

This code keeps the exponent arrays of q4-j3-l8-p40-d11-w9 and changes the
GF4 column coefficients. Multiply each H_X column by lambda_j and each H_Z
column by lambda_j^-1. The scalars and optional check-row scalars are recorded
in construction.json. This preserves symbol supports and CSS commutation.
The physical binary checks change, so the distance is certified afresh.

Choose A=(0,1,2), B=(4,5,6), I=(3,7), form the cofactor columns, and divide
X seeds by Delta_Z and Z seeds by Delta_X. All cyclic polynomial coefficients
are given in construction.json; GF4 values 2 and 3 mean omega and omega^2.
Expand z^e with entry ((t+e) mod P,t)=1. Expand omega by [[0,1],[1,1]],
and transpose the expanded seed columns to obtain logical rows.

Binary CSS, kernel identities, completeness, ranks and integer support-overlap
identity were independently checked. Exact minimum distance 13 uses exhaustive
exclusion through weight 12 on both sides and a verified weight-13 witness.
See distance/ for compact records. Run the repository-wide scripts/verify_all.py
for matrix hashes, ranks, kernel conditions, and canonical pairing.

This is an additional search result; it has not yet been added to the paper table.
