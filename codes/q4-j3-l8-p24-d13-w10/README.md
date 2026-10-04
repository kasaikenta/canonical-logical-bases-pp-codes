# GF(4) CPM--PP [[384,96,13]] with integer support overlap I

J=3, L=8, P=24. The full exponent arrays, quaternary coefficients,
reciprocal column scalings, check-row scalings, pivot sets, determinant
inverses, and normalized polynomial logical seeds are in construction.json.
GF(4) values 1,2,3 mean 1, omega, omega^2, with omega^2+omega+1=0.
The polynomial exponents are reduced modulo P. Apply the repository's
companion convention to reconstruct matrices.npz from these data.

The disjoint pivots are A=(0,1,2), B=(4,5,6), I=(3,7).
Individual determinant normalization sets the free blocks to identities.
The complete binary logical basis has maximum weights 26/26 and integer
X/Z support-intersection matrix I_96. The symbol girths are 6/6 and
binary girths 4/4. The maximum binary check-row weight is 10.

The exact CSS distance 13 is certified by all 48 connected-search roots
completed through weight 12 on both sides and an independently checked
X-type weight-13 logical operator. See distance/ for the inputs and compact
certificate. Run scripts/verify_all.py for binary matrix validation.
This connected candidate is included in both paper tables.
