# [[768,192,18]]: symbol and binary girth 6

The GF(4) CPM--PP construction has J=3, L=8, P=48, binary check weights 8/9, and binary column weights 3/4. The complete canonical bases have maximum binary weights 28/28 and maximum integer support intersections 1/2 for equal/unequal logical indices.

`matrices.npz` stores HX, HZ, LX, LZ. All eight Matrix Market files additionally give the binary and quaternary matrices. `construction.json` contains the circulant exponents, pair partitions, coefficient positions, pivot sets, pairing polynomial, and complete polynomial seeds. Matrix Market coordinates are one-based; GF(4) values 2 and 3 denote omega and omega+1.

The reported exact binary quantum distance is 18: both saved exclusion searches cover weights through 17, and at least one independently checked nontrivial binary logical has weight 18. The side-specific intervals are recorded in `summary.json`. The independent three-Mac replay completed all 16 physical-bit roots on each CSS side through weight d-1. Its inputs, 32 root records, and certificate are in `distance/three_mac_recheck/`; the original records are preserved separately.

Run `python3 scripts/verify_all.py` from the repository root for the final binary matrix audit. See [the replay documentation](../../docs/girth6-codes.md) for the independent distance reexecution.
