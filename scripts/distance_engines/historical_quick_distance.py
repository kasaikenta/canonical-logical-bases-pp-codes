#!/usr/bin/env python3
"""Screen exact companion distance up to a chosen limit using all QC roots."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
from pathlib import Path


def run_root(binary, source, limit, block, value, seconds):
    proc = subprocess.run([str(binary), str(source), str(limit), str(block),
                           str(value), str(seconds)], capture_output=True, text=True)
    if proc.returncode:
        return {"error": proc.stderr, "stdout": proc.stdout,
                "returncode": proc.returncode, "complete": False, "found": False}
    return json.loads(proc.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case", type=Path)
    ap.add_argument("--binary", type=Path, required=True)
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--max", type=int, default=24)
    ap.add_argument("--min", type=int, default=1)
    ap.add_argument("--seconds", type=float, default=5)
    ap.add_argument("--workers", type=int, default=40)
    args = ap.parse_args()
    result = {"sides": {}}
    for side in ("X", "Z"):
        source = args.case / f"distance_{side}.txt"
        history = []
        exact = None
        for limit in range(args.min, args.max + 1):
            roots = [(b, value) for b in range(args.L) for value in (1, 2, 3)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                runs = list(pool.map(
                    lambda item: run_root(args.binary, source, limit, item[0],
                                          item[1], args.seconds), roots))
            found = [run for run in runs if run.get("found")]
            complete = sum(bool(run.get("complete")) for run in runs)
            history.append({"limit": limit, "found_roots": len(found),
                            "complete_roots": complete,
                            "errors": [run for run in runs if run.get("error")][:3]})
            if found:
                exact = limit
                break
            if complete != len(roots):
                break
        result["sides"][side] = {"exact_distance": exact, "history": history}
    dx = result["sides"]["X"]["exact_distance"]
    dz = result["sides"]["Z"]["exact_distance"]
    result["exact_CSS_distance"] = min(dx, dz) if dx and dz else None
    (args.case / "quick_distance.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
