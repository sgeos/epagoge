"""Variance pilot trainer.

Measures run-to-run behaviour of the training setup: the seed-to-seed
standard deviation of the primary endpoint, and the correlation between
paired runs that share an initialisation and their data and differ only in
ordering.

**This measures the training setup, not the curriculum.** It therefore runs
on any corpus and does not wait on the concept graph or on corpus
generation. That is the whole reason it is the cheapest unblocker.

Requires the optional ``train`` dependency group. Every other module in this
package is standard library only.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, cast

import torch
from torch import Tensor, nn

DEFAULT_VOCAB: Final[int] = 32
"""Small deliberately.

A second-order Markov source has vocabulary-squared contexts, and the stream
must revisit each often enough for structure to exist. At 256 a
200,000-token stream visits each context about three times, so the model
correctly learns nothing and every ordering produces an identical result.
The first smoke test showed exactly that, sitting at the chance loss of
ln(256) with a paired difference of zero.
"""


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Deliberately small. The pilot measures variance, not capability."""

    vocab_size: int = DEFAULT_VOCAB
    d_model: int = 128
    n_layers: int = 4
    n_heads: int = 4
    seq_len: int = 128


@dataclass(frozen=True, slots=True)
class TrainConfig:
    steps: int = 2000
    batch_size: int = 16
    learning_rate: float = 3e-4
    warmup: int = 100
    min_lr_fraction: float = 0.1
    eval_batches: int = 24


class TinyTransformer(nn.Module):
    """A conventional decoder-only transformer, and nothing more.

    Standard by intent. The ablation's architecture decision forbids
    deviation, and the pilot should share the setup whose variance it claims
    to measure.
    """

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.config = config
        self.token = nn.Embedding(config.vocab_size, config.d_model)
        self.position = nn.Embedding(config.seq_len, config.d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=config.d_model,
            nhead=config.n_heads,
            dim_feedforward=4 * config.d_model,
            batch_first=True,
            norm_first=True,
            dropout=0.0,
        )
        self.blocks = nn.TransformerEncoder(layer, num_layers=config.n_layers)
        self.norm = nn.LayerNorm(config.d_model)
        self.head = nn.Linear(config.d_model, config.vocab_size, bias=False)

    def forward(self, tokens: Tensor) -> Tensor:
        length = tokens.shape[1]
        positions = torch.arange(length, device=tokens.device)
        hidden = self.token(tokens) + self.position(positions)
        mask = nn.Transformer.generate_square_subsequent_mask(
            length, device=tokens.device
        )
        hidden = self.blocks(hidden, mask=mask, is_causal=True)
        return self.head(self.norm(hidden))


def synthetic_stream(length: int, vocab_size: int, seed: int) -> list[int]:
    """A deterministic token stream with learnable structure.

    A fixed random second-order Markov process. Loss falls because there is
    real structure, and the stream is reproducible from a seed.

    **Stated limitation.** This is not natural language, and variance
    measured on it need not transfer exactly to a natural-language corpus.
    The pilot's purpose is the behaviour of the training setup, but this is
    the assumption most worth re-checking once a real corpus exists.
    """
    rng = random.Random(seed)
    table: dict[tuple[int, int], list[int]] = {}
    stream = [rng.randrange(vocab_size), rng.randrange(vocab_size)]
    for _ in range(length):
        key = (stream[-2], stream[-1])
        if key not in table:
            # S311: reproducibility from a declared seed is the requirement.
            table[key] = [rng.randrange(vocab_size) for _ in range(3)]
        stream.append(rng.choice(table[key]))
    return stream


def chunk(stream: list[int], seq_len: int, pad: int | None = None) -> list[list[int]]:
    """Split a stream into fixed-length chunks. Ordering acts on these.

    **Without ``pad`` the tail of every stream is thrown away**, and when
    the streams are books rather than a corpus that is most of the corpus.
    Measured 2026-09-25 over 146 level-one books: 35,438 tokens became 68
    chunks of 128, which is 8,772 tokens, so three quarters were dropped
    and every book shorter than 129 tokens contributed nothing at all. The
    median book is 192 tokens.

    Passing the padding id keeps the tail as a padded chunk. The caller is
    then responsible for ignoring that id in the loss, which `train_once`
    does, or the model learns to predict padding.
    """
    if pad is None:
        usable = (len(stream) - 1) // seq_len * seq_len
        return [stream[i : i + seq_len + 1] for i in range(0, usable, seq_len)]
    out: list[list[int]] = []
    for start in range(0, max(len(stream) - 1, 0), seq_len):
        piece = stream[start : start + seq_len + 1]
        if len(piece) < 2:
            break
        out.append(piece + [pad] * (seq_len + 1 - len(piece)))
    return out


def _batches(
    chunks: list[list[int]], order: list[int], batch_size: int, device: torch.device
) -> list[tuple[Tensor, Tensor]]:
    out: list[tuple[Tensor, Tensor]] = []
    for start in range(0, len(order) - batch_size + 1, batch_size):
        rows = [chunks[i] for i in order[start : start + batch_size]]
        block = torch.tensor(rows, dtype=torch.long, device=device)
        out.append((block[:, :-1], block[:, 1:]))
    return out


def _schedule(step: int, config: TrainConfig) -> float:
    """Linear warmup then cosine decay.

    Warmup alone leaves the rate at its peak forever. Measured 2026-09-24,
    that made four thousand steps converge worse than two thousand, and
    variance measured under a setup that destabilises would not transfer to
    an ablation that uses a schedule.
    """
    if step < config.warmup:
        return config.learning_rate * (step + 1) / config.warmup
    progress = (step - config.warmup) / max(config.steps - config.warmup, 1)
    cosine = 0.5 * (1.0 + math.cos(math.pi * min(progress, 1.0)))
    floor = config.min_lr_fraction
    return config.learning_rate * (floor + (1.0 - floor) * cosine)


def train_once(
    chunks: list[list[int]],
    order: list[int],
    held_out: list[list[int]],
    model_config: ModelConfig,
    train_config: TrainConfig,
    init_seed: int,
    device: torch.device,
    pad_id: int | None = None,
    warm_from: WarmStart | None = None,
) -> float:
    """Train one model and return its held-out loss.

    ``init_seed`` fixes the initialisation. Two calls sharing an init seed and
    ``chunks`` but differing in ``order`` are a pair.

    ``pad_id`` is excluded from the loss where the chunks carry padding.

    **The model is discarded.** That is right for the ablation, which
    compares two orderings by one number, and wrong as the only thing the
    project can do with a trained model. :func:`train_model` returns it for
    the cases where something other than a loss is wanted.
    """
    _model, loss = train_model(
        chunks,
        order,
        held_out,
        model_config,
        train_config,
        init_seed,
        device,
        pad_id,
        warm_from=warm_from,
    )
    return loss


@dataclass(frozen=True, slots=True)
class TrainResult:
    """A trained model and enough numbers to say what is wrong with it.

    **Held-out loss alone cannot separate undertrained from overfitted**,
    and those call for opposite work: one wants more steps or more
    capacity, the other wants more corpus. The gap between training and
    held-out loss separates them, so both are returned.
    """

    model: TinyTransformer
    held_out_loss: float
    train_loss: float
    curve: tuple[tuple[int, float], ...]
    """Step and mean training loss over the preceding window."""

    @property
    def gap(self) -> float:
        """Held-out minus training. Large means the corpus is the limit."""
        return self.held_out_loss - self.train_loss


def train_model(
    chunks: list[list[int]],
    order: list[int],
    held_out: list[list[int]],
    model_config: ModelConfig,
    train_config: TrainConfig,
    init_seed: int,
    device: torch.device,
    pad_id: int | None = None,
    warm_from: WarmStart | None = None,
) -> tuple[TinyTransformer, float]:
    """Train one model and return it with its held-out loss.

    **Held-out loss cannot distinguish a model that learned the language
    from one that learned which words are common.** Sampling can, which is
    why the model is available here rather than only its score.
    """
    result = train_diagnostic(
        chunks,
        order,
        held_out,
        model_config,
        train_config,
        init_seed,
        device,
        pad_id,
        warm_from=warm_from,
    )
    return result.model, result.held_out_loss


def train_diagnostic(
    chunks: list[list[int]],
    order: list[int],
    held_out: list[list[int]],
    model_config: ModelConfig,
    train_config: TrainConfig,
    init_seed: int,
    device: torch.device,
    pad_id: int | None = None,
    curve_every: int = 100,
    warm_from: WarmStart | None = None,
) -> TrainResult:
    """Train one model and return it with training and held-out loss.

    ``warm_from`` initialises the model from an earlier level before any
    step is taken, which is what makes level N a continuation of level N
    minus one rather than a fresh run.
    """
    # torch ships incomplete stubs for these two calls. The suppression is a
    # gap in the framework's typing, not a weakening of this module's.
    torch.manual_seed(init_seed)  # pyright: ignore[reportUnknownMemberType]
    model = TinyTransformer(model_config).to(device)
    if warm_from is not None:
        _ = warm_start(model, warm_from.state, warm_from.older, warm_from.newer)
    optimiser = torch.optim.AdamW(model.parameters(), lr=train_config.learning_rate)
    # **Padding is excluded from the loss.** A padded tail chunk is there to
    # keep the text, not to be predicted, and a model rewarded for emitting
    # padding would learn the one thing the corpus never says.
    loss_fn = (
        nn.CrossEntropyLoss()
        if pad_id is None
        else nn.CrossEntropyLoss(ignore_index=pad_id)
    )

    batches = _batches(chunks, order, train_config.batch_size, device)
    model.train()
    curve: list[tuple[int, float]] = []
    window: list[float] = []
    for step in range(train_config.steps):
        inputs, targets = batches[step % len(batches)]
        for group in optimiser.param_groups:
            group["lr"] = _schedule(step, train_config)
        logits = model(inputs)
        loss = loss_fn(logits.reshape(-1, model_config.vocab_size), targets.reshape(-1))
        optimiser.zero_grad(set_to_none=True)
        loss.backward()
        _ = nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimiser.step()  # pyright: ignore[reportUnknownMemberType]
        window.append(loss.item())
        if curve_every > 0 and (step + 1) % curve_every == 0:
            curve.append((step + 1, sum(window) / len(window)))
            window = []

    model.eval()
    order_eval = list(range(len(held_out)))
    eval_batches = _batches(held_out, order_eval, train_config.batch_size, device)[
        : train_config.eval_batches
    ]
    total = 0.0
    with torch.no_grad():
        for inputs, targets in eval_batches:
            logits = model(inputs)
            total += loss_fn(
                logits.reshape(-1, model_config.vocab_size), targets.reshape(-1)
            ).item()
    # **Training loss is measured in eval mode over the same batches**, not
    # taken from the last step of the loop. A running figure is dominated
    # by whichever batch happened to come last and by dropout, and it is
    # the gap that this number exists to make meaningful.
    train_total = 0.0
    with torch.no_grad():
        for inputs, targets in batches[: train_config.eval_batches]:
            logits = model(inputs)
            train_total += loss_fn(
                logits.reshape(-1, model_config.vocab_size), targets.reshape(-1)
            ).item()
    return TrainResult(
        model=model,
        held_out_loss=total / max(len(eval_batches), 1),
        train_loss=train_total / max(len(batches[: train_config.eval_batches]), 1),
        curve=tuple(curve),
    )


@dataclass(frozen=True, slots=True)
class WarmStart:
    """An earlier level's weights, with both vocabularies to map between.

    Both word lists are carried because the mapping is by word and neither
    list can be recovered from the other or from the checkpoint. Passing
    them separately from the state is what lets one loaded checkpoint
    serve every arm and every seed of a run.
    """

    state: Mapping[str, Tensor]
    older: Sequence[str]
    """The word list the checkpoint was trained with, in token order."""

    newer: Sequence[str]
    """The word list this run uses, in token order."""


VOCABULARY_TENSORS: Final[tuple[str, ...]] = ("token.weight", "head.weight")
"""The parameters whose first axis is the vocabulary.

Named rather than inferred from shape, because a model whose width happens
to equal its vocabulary size would have every tensor match.
"""


def save_checkpoint(
    model: TinyTransformer,
    config: ModelConfig,
    words: Sequence[str],
    path: Path,
) -> None:
    """Write weights together with the vocabulary they were trained on.

    **A checkpoint without its word list is unusable the moment the
    lexicon changes.** Six words were admitted after one was written and
    loading it failed on a size mismatch, with nothing on disk saying what
    size it had been or which word each row stood for.

    The model speaks the vocabulary it was trained with. Reading a
    checkpoint back therefore means rebuilding that tokeniser rather than
    the current one, and carrying the word list is what makes that
    possible.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(  # pyright: ignore[reportUnknownMemberType]
        {
            "state": model.state_dict(),
            "words": list(words),
            "config": {
                "vocab_size": config.vocab_size,
                "d_model": config.d_model,
                "n_layers": config.n_layers,
                "seq_len": config.seq_len,
            },
        },
        path,
    )


@dataclass(frozen=True, slots=True)
class Checkpoint:
    """A trained model with the vocabulary and shape it was trained at."""

    model: TinyTransformer
    words: tuple[str, ...]
    config: ModelConfig


def load_checkpoint(path: Path, device: torch.device) -> Checkpoint:
    """Rebuild a model at the shape its checkpoint was written with.

    **Nothing is inferred from the caller.** A checkpoint that carries its
    own shape cannot be loaded into the wrong one, which is the failure
    this replaces: an error message blaming the model width when the
    vocabulary had grown by six words.

    A checkpoint written before this format is refused with a message
    saying so, rather than being guessed at.
    """
    payload = cast(
        "object",
        torch.load(path, map_location=device),  # pyright: ignore[reportUnknownMemberType]
    )
    if not isinstance(payload, dict) or "words" not in payload:
        raise ValueError(
            f"{path} has no vocabulary in it, so the words its rows stand for "
            "are unknown. Retrain to write one in the current format."
        )
    body = cast("dict[str, object]", payload)
    saved = cast("dict[str, int]", body["config"])
    config = ModelConfig(
        vocab_size=saved["vocab_size"],
        d_model=saved["d_model"],
        n_layers=saved["n_layers"],
        seq_len=saved["seq_len"],
    )
    model = TinyTransformer(config).to(device)
    _ = model.load_state_dict(cast("Mapping[str, Tensor]", body["state"]))
    model.eval()
    return Checkpoint(
        model=model, words=tuple(cast("list[str]", body["words"])), config=config
    )


def warm_start(
    model: TinyTransformer,
    state: Mapping[str, Tensor],
    older: Sequence[str],
    newer: Sequence[str],
) -> int:
    """Initialise ``model`` from a smaller level's weights. Returns rows kept.

    **Level N starts from the level N minus one model**, which is the
    project's training design and not an optimisation. Each level is a
    continuation of the last rather than a fresh run, so a level-two model
    inherits what level one learned about the words they share.

    **The vocabulary grows between levels**, so the embedding and the
    output head grow with it and the rows cannot simply be copied. A row
    is matched by the word it stands for: a word in both lexicons keeps
    its learned vector, a word new at this level keeps the fresh
    initialisation it was given, and a word that has left is dropped.

    Every other parameter is copied outright, since nothing else is
    indexed by the vocabulary.
    """
    target = model.state_dict()
    index = {word: position for position, word in enumerate(newer)}
    kept = 0
    merged: dict[str, Tensor] = {}
    for name, tensor in target.items():
        source = state.get(name)
        if source is None:
            merged[name] = tensor
            continue
        if name not in VOCABULARY_TENSORS:
            if source.shape != tensor.shape:
                raise ValueError(
                    f"{name}: checkpoint is {tuple(source.shape)} and the model "
                    f"is {tuple(tensor.shape)}; the two were not built alike"
                )
            merged[name] = source.clone()
            continue
        # **The width must match even where the height may not.** Only the
        # vocabulary axis grows between levels; a different model width is
        # a checkpoint from another experiment, and copying rows into it
        # raises deep in torch rather than here.
        if source.shape[1:] != tensor.shape[1:]:
            raise ValueError(
                f"{name}: checkpoint rows are {tuple(source.shape[1:])} and the "
                f"model's are {tuple(tensor.shape[1:])}; only the vocabulary "
                "may differ between levels"
            )
        grown = tensor.clone()
        for position, word in enumerate(older):
            destination = index.get(word)
            if destination is None or position >= source.shape[0]:
                continue
            grown[destination] = source[position]
            kept += 1
        merged[name] = grown
    _ = model.load_state_dict(merged)
    return kept // max(len(VOCABULARY_TENSORS), 1)


def sample(
    model: TinyTransformer,
    prompt: list[int],
    count: int,
    device: torch.device,
    *,
    seed: int = 0,
    temperature: float = 1.0,
    top_k: int = 0,
    seq_len: int = 128,
) -> list[int]:
    """Continue ``prompt`` for ``count`` tokens, sampling from the model.

    Seeded, because a sample nobody can reproduce is an anecdote. The
    context is truncated to the training sequence length, since the
    positional embedding is only that long.

    ``top_k`` of zero samples from the full distribution. Truncating it
    flatters the model by hiding the tail it puts mass on, so the default
    does not.
    """
    if temperature <= 0.0:
        raise ValueError(f"temperature must be positive, got {temperature}")
    if count < 0:
        raise ValueError(f"count must not be negative, got {count}")
    generator = torch.Generator(device="cpu")
    _ = generator.manual_seed(seed)
    model.eval()
    out = list(prompt)
    with torch.no_grad():
        for _ in range(count):
            window = out[-seq_len:]
            block = torch.tensor([window], dtype=torch.long, device=device)
            logits = model(block)[0, -1] / temperature
            if top_k > 0:
                cut = torch.topk(logits, min(top_k, logits.numel())).values[-1]
                logits = logits.masked_fill(logits < cut, float("-inf"))
            probabilities = torch.softmax(logits, dim=-1).to("cpu")
            nxt = int(torch.multinomial(probabilities, 1, generator=generator).item())
            out.append(nxt)
    return out[len(prompt) :]


def select_device(preference: str | None = None) -> torch.device:
    if preference:
        return torch.device(preference)
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def parameter_count(config: ModelConfig) -> int:
    model = TinyTransformer(config)
    return sum(p.numel() for p in model.parameters())


def orderings(count: int, seed: int) -> tuple[list[int], list[int]]:
    """Two distinct orderings of the same chunks.

    The pilot does not need the curriculum ordering. It needs two orderings,
    because what it measures is how much the endpoint moves when only order
    changes, which is the quantity the ablation's power depends on.
    """
    rng = random.Random(seed)
    a = list(range(count))
    b = list(range(count))
    rng.shuffle(a)
    rng.shuffle(b)
    if a == b and count > 1:
        a[0], a[1] = a[1], a[0]
    return a, b


def format_seconds(seconds: float) -> str:
    return (
        f"{int(seconds // 60)}m{int(seconds % 60):02d}s"
        if seconds >= 60
        else f"{seconds:.1f}s"
    )


def is_finite(value: float) -> bool:
    return math.isfinite(value)
