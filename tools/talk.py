#!/usr/bin/env python3
"""Talk to a trained level model, or ask it to continue a line.

**This is the only way to find out what the model says.** Held-out loss
cannot separate a model that learned the language from one that learned
which words are common, and the project reported a loss for two sessions
without a token ever being generated.

Loads weights written by `train_level.py --save` or `sample_level.py`,
and refuses to invent them: a checkpoint that does not exist is an error
rather than a fresh untrained model, because an untrained model answers
every prompt and means nothing.

    .venv/bin/python tools/talk.py --level 1
    .venv/bin/python tools/talk.py --level 1 --prompt "the cup is"

Input outside the level's vocabulary is reported rather than silently
mapped to the unknown token, since a prompt the model cannot read is the
most likely reason for a disappointing answer.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

from epagoge.pilot import ModelConfig, TinyTransformer, sample, select_device
from epagoge.tokeniser import BOOK, SPECIALS, Tokeniser, build
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def encode_prompt(tokeniser: Tokeniser, text: str) -> tuple[list[int], list[str]]:
    """Token ids for ``text``, and the words the level does not carry."""
    unknown = tokeniser.unknown(text)
    ids = [tokeniser.ids[BOOK]] if not text.strip() else tokeniser.encode(text)
    return ids, sorted(set(unknown))


def answer(
    model: TinyTransformer,
    tokeniser: Tokeniser,
    text: str,
    *,
    tokens: int,
    device: torch.device,
    seed: int,
    temperature: float,
    seq_len: int,
) -> str:
    ids, unknown = encode_prompt(tokeniser, text)
    if unknown:
        print(
            f"  [outside level: {' '.join(unknown)}]",
            file=sys.stderr,
        )
    produced = sample(
        model,
        ids,
        tokens,
        device,
        seed=seed,
        temperature=temperature,
        seq_len=seq_len,
    )
    specials = {tokeniser.ids[s] for s in SPECIALS}
    return tokeniser.decode([t for t in produced if t not in specials])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--prompt", type=str, default=None)
    parser.add_argument("--tokens", type=int, default=60)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument("--d-model", type=int, default=256)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--device", type=str, default=None)
    args = parser.parse_args(argv[1:])

    weights = args.weights or ROOT / f"evals/pilot/level_{args.level}.pt"
    if not weights.is_file():
        print(
            f"no weights at {weights}. Train some first:\n"
            f"  .venv/bin/python tools/sample_level.py --level {args.level}",
            file=sys.stderr,
        )
        return 1

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, args.level)
    config = ModelConfig(
        vocab_size=tokeniser.size,
        d_model=args.d_model,
        n_layers=args.layers,
        seq_len=args.seq_len,
    )
    device = select_device(args.device)
    model = TinyTransformer(config).to(device)
    state = torch.load(weights, map_location=device)  # pyright: ignore[reportUnknownMemberType]
    try:
        _ = model.load_state_dict(state)
    except RuntimeError as exc:
        print(
            f"{weights} does not fit d_model={args.d_model} layers={args.layers}.\n"
            f"Pass the shape the checkpoint was trained with.\n{exc}",
            file=sys.stderr,
        )
        return 1
    model.eval()

    if args.prompt is not None:
        print(
            answer(
                model,
                tokeniser,
                args.prompt,
                tokens=args.tokens,
                device=device,
                seed=args.seed,
                temperature=args.temperature,
                seq_len=args.seq_len,
            )
        )
        return 0

    print(
        f"level {args.level}, vocabulary {tokeniser.size}, "
        f"temperature {args.temperature}. Blank line or Ctrl-D to leave."
    )
    turn = 0
    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text.strip():
            return 0
        print(
            answer(
                model,
                tokeniser,
                text,
                tokens=args.tokens,
                device=device,
                seed=args.seed + turn,
                temperature=args.temperature,
                seq_len=args.seq_len,
            )
        )
        turn += 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
