#!/usr/bin/env python3
"""Verify every binary CSS code and canonical logical basis in the catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def rows_as_ints(a: np.ndarray) -> list[int]:
    packed = np.packbits(np.asarray(a, dtype=np.uint8), axis=1, bitorder="little")
    return [int.from_bytes(row.tobytes(), "little") for row in packed]


def gf2_rank(a: np.ndarray) -> int:
    rows = rows_as_ints(a)
    pivots: dict[int, int] = {}
    for value in rows:
        x = value
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)


def orthogonal(a: np.ndarray, b: np.ndarray) -> bool:
    rb = rows_as_ints(b)
    return all((x & y).bit_count() % 2 == 0 for x in rows_as_ints(a) for y in rb)


def canonical(lx: np.ndarray, lz: np.ndarray) -> bool:
    rz = rows_as_ints(lz)
    for i, x in enumerate(rows_as_ints(lx)):
        for j, z in enumerate(rz):
            if ((x & z).bit_count() & 1) != (i == j):
                return False
    return True


def sha256_matrix(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.uint8).tobytes()).hexdigest()


def distribution(values: np.ndarray) -> dict[str, int]:
    unique, counts = np.unique(values, return_counts=True)
    return {str(int(x)): int(n) for x, n in zip(unique, counts)}


def verify(code_dir: Path) -> dict:
    meta = json.loads((code_dir / "metadata.json").read_text())
    with np.load(code_dir / "matrices.npz", allow_pickle=False) as archive:
        matrices = {name: np.asarray(archive[name], dtype=np.uint8) for name in ("HX", "HZ", "LX", "LZ")}
    hx, hz, lx, lz = (matrices[name] for name in ("HX", "HZ", "LX", "LZ"))
    n, k = int(meta["n"]), int(meta["k"])
    expected_check_rank = (n - k) // 2
    checks = {
        "binary_entries": all(np.all((a == 0) | (a == 1)) for a in matrices.values()),
        "shapes": hx.shape[1] == hz.shape[1] == lx.shape[1] == lz.shape[1] == n and lx.shape[0] == lz.shape[0] == k,
        "css": orthogonal(hx, hz),
        "hz_lx": orthogonal(hz, lx),
        "hx_lz": orthogonal(hx, lz),
        "canonical": canonical(lx, lz),
        "rank_hx": gf2_rank(hx) == expected_check_rank,
        "rank_hz": gf2_rank(hz) == expected_check_rank,
        "rank_lx": gf2_rank(lx) == k,
        "rank_lz": gf2_rank(lz) == k,
        "hashes": all(sha256_matrix(matrices[name]) == meta["matrix_sha256"][name] for name in matrices),
        "max_check_row_weight": max(int(hx.sum(1).max()), int(hz.sum(1).max())) == int(meta["max_check_row_weight"]),
        "max_basis_weight_x": int(lx.sum(1).max()) == int(meta["max_basis_weight_x"]),
        "max_basis_weight_z": int(lz.sum(1).max()) == int(meta["max_basis_weight_z"]),
    }
    return {
        "id": meta["id"],
        "passed": all(checks.values()),
        "checks": checks,
        "computed": {
            "rank_HX": gf2_rank(hx),
            "rank_HZ": gf2_rank(hz),
            "check_row_weights_HX": distribution(hx.sum(1)),
            "check_row_weights_HZ": distribution(hz.sum(1)),
            "check_column_weights_HX": distribution(hx.sum(0)),
            "check_column_weights_HZ": distribution(hz.sum(0)),
            "basis_weights_LX": distribution(lx.sum(1)),
            "basis_weights_LZ": distribution(lz.sum(1)),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="write a machine-readable report")
    args = parser.parse_args()
    results = [verify(path) for path in sorted((ROOT / "codes").iterdir()) if (path / "metadata.json").exists()]
    report = {"all_passed": all(item["passed"] for item in results), "codes": results}
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    for item in results:
        print(f"{'PASS' if item['passed'] else 'FAIL'}  {item['id']}")
    print(f"{sum(item['passed'] for item in results)}/{len(results)} codes passed")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
