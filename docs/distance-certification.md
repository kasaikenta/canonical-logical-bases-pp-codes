# Exact-distance records

The catalog field `distance_status` distinguishes exact values from bounds.
Every entry in the paper table is marked `exact` only when both ingredients
are archived:

1. a nontrivial zero-syndrome representative of weight `d`; and
2. exhaustive exclusion of every nontrivial representative of weight below
   `d`, using the cyclic symmetry reduction described in the paper.

The compact records under `distance/` preserve the claimed value, search
coverage, witness location, and source hashes available for the corresponding
experiment.  Some historical searches produced large per-worker traces; those
traces are summarized rather than duplicated here.  The final matrices and
the compact certificates are keyed by stable code identifier and SHA-256
digest so that a separately archived full trace can be matched unambiguously.

Distance is a property of the fixed binary matrices in `matrices.npz`; a
family-level construction recipe does not by itself certify the distance of
all lift sizes.
