#!/usr/bin/env python3
"""Turn a level's training run into the numbers the pre-registration needs.

Reads what ``train_level.py`` wrote and reports seed-to-seed variance, the
paired correlation, what pairing is worth, and the seeds a given effect
would need. **It decides nothing.** Whether an effect exists is settled by
the pre-registered threshold against these numbers, not by their sign.

**Read the corpus size before the statistics.** A paired correlation
measured on a corpus far below the scale the ablation is meant to run at
describes that corpus and not the design, which is exactly how the first
pilot's 20.7x gain came to be quoted after it had stopped applying.

    PYTHONPATH=src python3 tools/analyse_level.py evals/pilot/level_1.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge.variance import PairedObservation, estimate, required_seeds


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument(
        "--effect",
        type=float,
        default=0.01,
        help="minimum meaningful effect in held-out loss",
    )
    args = parser.parse_args(argv[1:])

    payload = cast(dict[str, object], json.loads(args.file.read_text(encoding="utf-8")))
    rows = cast(list[dict[str, object]], payload["results"])
    observations = [
        PairedObservation(
            seed=int(cast(int, row["seed"])),
            treatment=float(cast(float, row["curriculum"])),
            control=float(cast(float, row["topological"])),
        )
        for row in rows
        if "curriculum" in row and "topological" in row
    ]
    if len(observations) < 2:
        print(
            f"{len(observations)} usable pair(s); at least two are needed for a "
            "variance estimate",
            file=sys.stderr,
        )
        return 1

    got = estimate(observations)
    print(f"{args.file}")
    print(
        f"  corpus       {payload.get('tokens')} tokens in "
        f"{payload.get('chunks')} chunks, {payload.get('parameters')} parameters"
    )
    print(f"  pairs        {got.n}")
    print(f"  seed sd      {got.seed_sd:.5f}  within a condition")
    print(f"  paired sd    {got.paired_sd:.5f}  of the within-pair difference")
    print(f"  correlation  {got.correlation:.4f}")
    print(f"  pairing gain {got.pairing_gain:.1f}x seeds")
    print(f"  mean diff    {got.mean_difference:+.5f}  curriculum minus topological")
    print()
    paired = required_seeds(got.paired_sd, args.effect, paired=True)
    unpaired = required_seeds(got.seed_sd, args.effect, paired=False)
    print(f"  to detect {args.effect} in held-out loss:")
    print(f"    paired     {paired} seeds per condition")
    print(f"    unpaired   {unpaired} seeds per condition")
    print()
    print("  This reports. The pre-registered threshold decides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
