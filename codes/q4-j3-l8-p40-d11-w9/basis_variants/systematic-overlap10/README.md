# Complete support-separated canonical basis

This is an alternate basis for the same [[640,160,11]] CSS code as ../../matrices.npz.
Maximum binary check weight: 9; symbol and binary girth: 6/6.
Maximum canonical-basis row weights: 27/27. Each side has 40 rows of weight 25,
80 of weight 26, and 40 of weight 27.

The full integer support-overlap matrix is I_160: each paired X/Z representative
shares exactly one physical qubit; representatives of different logical qubits
have disjoint supports. All 160 logical qubits are covered.

Construction: A=(0,1,2), B=(4,5,6), I=(3,7). Multiply each X cofactor seed by
Delta_Z^-1 and each Z cofactor seed by Delta_X^-1 before companion expansion.
The shared free-column coefficients then equal one. The full polynomial recipe
and all four binary matrices are provided here. GF(4) elements 2 and 3 mean
omega and omega^2; omega^2+omega+1=0. A cyclic monomial z^e is expanded with
entry ((t+e) mod P,t)=1. The companion matrix of omega is [[0,1],[1,1]].
Logical rows are transposes of the expanded cofactor columns.

Check matrices are byte-identical to the parent code. The exact distance 11
uses the parent's distance records; changing the complete logical basis leaves
the code and its distance unchanged. The original lower-weight basis remains
available in the parent matrix archive for comparison.

Run `python3 verify.py` from this directory to verify hashes, ranks, CSS,
logical kernel conditions, and the integer overlap identity.
