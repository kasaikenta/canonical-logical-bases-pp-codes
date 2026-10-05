# [[1024,256,20]] with complete canonical bases of maximum weight 25

J=3, L=8, P=64. Maximum binary check weight 10; column weights 3,4,5 on each side; ranks 384/384. Both symbol girths are 6 and both binary girths are 4. The complete logical bases have maximum weights 25/25 and integer overlap I_256.

The block-column partition is A=(5,6,7), B=(0,1,3), I=(2,4). The determinants are Delta_X=omega*z^43 and Delta_Z=omega*z^6, and the unnormalized pairing polynomial is g=omega^2*z^37. Individual determinant inverses normalize the free-column entries to 1. The cofactor reconstruction agrees entry by entry with the archived binary matrices.

`construction.json` gives all pair partitions, exponent and coefficient arrays, polynomial checks and canonical seeds, determinant inverses, and physical-bit pivot sets. `matrices.npz` losslessly supplies HX,HZ,LX,LZ.

Run `python reconstruct.py` in this directory to reproduce all four matrices. Run `python verify_distance.py` to check the stored root/branch coverage bookkeeping and the weight-20 witness. The distance archive records all 48 roots and every split branch through weight 19; its records refer to exhaustive runs of the archived `distance/distance_resume.cpp` (the exact source used for this run). Rechecking coverage and the witness uses these archived execution records rather than rerunning the complete exhaustive computation.

From the repository root, `python scripts/verify_all.py` also verifies binary CSS, kernel conditions, complete canonical pairing, ranks, weights, and matrix hashes.
