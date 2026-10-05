# P128 canonical basis with integer overlap identity

J=3, L=8, P=128; n=2048, k=512. The binary distance is **d=20**, certified by excluding all nontrivial logicals through weight 19 and checking a weight 20 logical.

The complete canonical X/Z bases have maximum weights 27/27, maximum check weight 10, symbol girth 6/6 and binary girth 4/4. Their integer support-overlap matrix is I512. Check ranks are 768 on each side; each basis has rank 512.

`construction.json` gives M, both exponent and coefficient arrays, disjoint pivot sets A=(0,1,2), B=(4,5,6), free sets I=(3,7), both determinants, and all normalized polynomial logical seeds. `matrices.npz` stores the lossless final binary HX,HZ,LX,LZ. Metadata hashes identify the same matrices used for the exact-distance verification.

Stages 1 through 19 excluded nontrivial logicals on both CSS sides. The checked Z-type weight 20 operator supplies the matching upper bound. Input files and the public exact engine permit rerunning the 48 cyclic-symmetry roots through 19. Stage completion summaries are archived in `distance/`. The search uses ascending integer limits; no parity of the distance is assumed.
