#!/usr/bin/env python3
"""Reconstruct the four multi-CPM table instances and report weight counts.

Uses the archived formal family at U=z, T=z^(P/2). This command verifies
matrix identities and table statistics; it does not rerun distance proofs.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import verify_all as verify

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / 'codes/f2-multicpm-j3-l8-p128-d22-w9/construction.json'
INSTANCES = ((56, 18), (66, 19), (72, 20), (128, 22))


def expand(blocks, P):
    matrix = np.zeros((len(blocks) * P, len(blocks[0]) * P), dtype=np.uint8)
    indices = np.arange(P)
    for i, row in enumerate(blocks):
        for j, polynomial in enumerate(row):
            for u, t in polynomial:
                shift = (u + t * (P // 2)) % P
                matrix[i * P + indices, j * P + (indices - shift) % P] ^= 1
    return matrix


def girth(matrix):
    # A repeated check-pair gives a four-cycle; otherwise a triangle with
    # three different shared variable nodes gives a six-cycle.
    edges, neighbors = {}, [set() for _ in range(matrix.shape[0])]
    for column in range(matrix.shape[1]):
        rows = np.flatnonzero(matrix[:, column]).tolist()
        for a, i in enumerate(rows):
            for j in rows[a + 1:]:
                if (i, j) in edges:
                    return 4
                edges[i, j] = column
                neighbors[i].add(j)
                neighbors[j].add(i)
    for (i, j), column in edges.items():
        for k in neighbors[i] & neighbors[j]:
            if k > j and len({column, edges[i, k], edges[j, k]}) == 3:
                return 6
    return None


def describe(P, distance, formal):
    matrices = {name: expand(formal[key], P)
                for name, key in [('HX', 'X'), ('HZ', 'Z'), ('LX', 'LX'), ('LZ', 'LZ')]}
    hx, hz, lx, lz = (matrices[name] for name in ('HX', 'HZ', 'LX', 'LZ'))
    checks = {
        'CSS': verify.orthogonal(hx, hz),
        'X_kernel': verify.orthogonal(hz, lx),
        'Z_kernel': verify.orthogonal(hx, lz),
        'canonical': verify.canonical(lx, lz),
        'check_rank': verify.gf2_rank(hx) == verify.gf2_rank(hz) == 3 * P,
        'basis_rank': verify.gf2_rank(lx) == verify.gf2_rank(lz) == 2 * P,
    }
    assert all(checks.values()), (P, checks)
    overlaps = lx.astype(np.uint16) @ lz.astype(np.uint16).T
    unmatched = overlaps.copy()
    np.fill_diagonal(unmatched, 0)
    assert int(np.diag(overlaps).max()) == 1 and int(unmatched.max()) == 2
    assert girth(hx) == girth(hz) == 6
    record = {
        'J': 3, 'L': 8, 'P': P, 'h': 1, 'parameters_reported_in_paper': [8 * P, 2 * P, distance],
        'distance_verification_in_this_command': False,
        'checks': checks, 'girth_X_Z': [6, 6], 'maximum_overlap': [1, 2],
        'matrix_sha256': {name: verify.sha256_matrix(m) for name, m in matrices.items()},
        'check_row_weights_HX': verify.distribution(hx.sum(1)),
        'check_row_weights_HZ': verify.distribution(hz.sum(1)),
        'check_column_weights_HX': verify.distribution(hx.sum(0)),
        'check_column_weights_HZ': verify.distribution(hz.sum(0)),
        'basis_weights_LX': verify.distribution(lx.sum(1)),
        'basis_weights_LZ': verify.distribution(lz.sum(1)),
    }
    assert record['check_column_weights_HX'] == record['check_column_weights_HZ'] == {'3': 5 * P, '4': 3 * P}
    assert record['basis_weights_LX'] == record['basis_weights_LZ'] == {'30': P, '33': P}
    if P == 128:
        original = json.loads((FORMAL.parent / 'metadata.json').read_text())
        assert record['matrix_sha256'] == original['matrix_sha256']
    return record, matrices


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    parser.add_argument('--matrix-dir', type=Path, help='optionally write all four reconstructed matrices per P')
    args = parser.parse_args()
    formal = json.loads(FORMAL.read_text())
    records = []
    for P, distance in INSTANCES:
        record, matrices = describe(P, distance, formal)
        records.append(record)
        if args.matrix_dir:
            args.matrix_dir.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(args.matrix_dir / f'P{P}.npz', **matrices)
    report = {'source_formal_family': str(FORMAL.relative_to(ROOT)), 'specialization': 'U=z, T=z^(P/2)',
              'distance_note': 'Distances reproduce the paper labels. This script verifies the matrices and weight distributions, not exhaustive distance certificates.',
              'instances': records}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
