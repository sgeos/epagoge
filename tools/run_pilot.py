#!/usr/bin/env python3
"""Run the variance pilot and report what the pre-registration needs.

    .venv/bin/python tools/run_pilot.py --pairs 8 --steps 2000

Writes a JSON result alongside the printed report. Requires the optional
``train`` dependency group.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path

from epagoge.pilot import (
    ModelConfig,
    TrainConfig,
    chunk,
    orderings,
    parameter_count,
    select_device,
    synthetic_stream,
    train_once,
)
from epagoge.variance import (
    PairedObservation,
    bootstrap_required_seeds,
    detectable_effect,
    estimate,
    required_seeds,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=int, default=8)
    parser.add_argument("--steps", type=int, default=2000)
    parser.add_argument("--tokens", type=int, default=200_000)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--out", type=Path, default=Path("tmp/pilot_result.json"))
    args = parser.parse_args()

    model_config = ModelConfig()
    train_config = TrainConfig(steps=args.steps)
    device = select_device(args.device)

    stream = synthetic_stream(args.tokens, model_config.vocab_size, seed=0)
    chunks = chunk(stream, model_config.seq_len)
    split = int(0.9 * len(chunks))
    train_chunks, held_out = chunks[:split], chunks[split:]

    print(f"device            {device}")
    print(f"parameters        {parameter_count(model_config):,}")
    print(f"train chunks      {len(train_chunks)}")
    print(f"held-out chunks   {len(held_out)}")
    print(f"steps             {train_config.steps}")
    print(f"pairs             {args.pairs}")
    print(f"chance loss       {math.log(model_config.vocab_size):.4f}")
    print(f"source entropy    {math.log(3):.4f}")
    print()

    observations: list[PairedObservation] = []
    started = time.time()
    for index in range(args.pairs):
        first, second = orderings(len(train_chunks), seed=1000 + index)
        a = train_once(
            train_chunks, first, held_out, model_config, train_config, index, device
        )
        b = train_once(
            train_chunks, second, held_out, model_config, train_config, index, device
        )
        observations.append(PairedObservation(seed=index, treatment=a, control=b))
        elapsed = time.time() - started
        print(
            f"  pair {index:2d}  A {a:.5f}  B {b:.5f}  diff {a - b:+.6f}"
            f"   [{elapsed / 60:.1f}m]"
        )

    est = estimate(observations)
    print()
    print("MEASURED")
    print(f"  pairs                       {est.n}")
    print(f"  seed sd (unpaired sigma)    {est.seed_sd:.6f}")
    print(f"  paired sd                   {est.paired_sd:.6f}")
    print(f"  correlation rho             {est.correlation:.4f}")
    print(f"  mean difference             {est.mean_difference:+.6f}")
    print(f"  pairing gain                {est.pairing_gain:.1f}x seeds, free")
    print()
    print("SEEDS REQUIRED, by target effect (relative to mean held-out loss)")
    mean_loss = sum((o.treatment + o.control) / 2 for o in observations) / len(
        observations
    )
    rows: list[dict[str, float | int]] = []
    for relative in (0.02, 0.01, 0.005, 0.002):
        effect = relative * mean_loss
        paired = required_seeds(est.paired_sd, effect, paired=True)
        unpaired = required_seeds(est.seed_sd, effect, paired=False)
        boot = bootstrap_required_seeds(
            observations, effect, resamples=5000, rng=random.Random(0)
        )
        print(
            f"  {relative * 100:4.1f}% = {effect:.5f}   paired {paired:5d}"
            f"   unpaired {unpaired:6d}   plan-with {boot.conservative:5d}"
        )
        rows.append(
            {
                "relative": relative,
                "effect": effect,
                "paired": paired,
                "unpaired": unpaired,
                "conservative": boot.conservative,
            }
        )
    print()
    print("DETECTABLE EFFECT, by seed count (paired)")
    for n in (5, 10, 20, 30):
        print(f"  n={n:3d}  {detectable_effect(est.paired_sd, n):.6f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "device": str(device),
                "parameters": parameter_count(model_config),
                "steps": train_config.steps,
                "pairs": est.n,
                "mean_loss": mean_loss,
                "seed_sd": est.seed_sd,
                "paired_sd": est.paired_sd,
                "correlation": est.correlation,
                "mean_difference": est.mean_difference,
                "pairing_gain": est.pairing_gain,
                "observations": [
                    {"seed": o.seed, "treatment": o.treatment, "control": o.control}
                    for o in observations
                ],
                "requirements": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
