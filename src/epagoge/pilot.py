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
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, fields
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


HEAD_CHANNELS = 64
"""Channels per attention head when the head count is derived."""


def head_count(d_model: int, requested: int) -> int:
    """How many heads a width should use.

    Zero means derive, which keeps the head dimension near
    ``HEAD_CHANNELS`` at every width instead of letting it grow with the
    model. At least one head, and never more heads than channels.
    """
    if requested > 0:
        return requested
    return max(1, min(d_model, d_model // HEAD_CHANNELS))


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Deliberately small. The pilot measures variance, not capability."""

    vocab_size: int = DEFAULT_VOCAB
    d_model: int = 128
    n_layers: int = 4
    n_heads: int = 0
    """Attention heads. **Zero means derive one head per 64 channels.**

    **It was fixed at four regardless of width, and that was a defect.** At
    width 1,024 four heads is a head dimension of 256, where 64 to 128 is
    standard, so every wide point in the capacity sweep of 2026-09-26 was
    measured on an unusual shape. Deriving it keeps the head dimension near
    64 at every width, which is what the sweep meant to vary and did not.

    An explicit value still overrides, because a sweep over head count is a
    legitimate thing to want.
    """

    dropout: float = 0.0
    """Dropout on attention output and the feed-forward.

    **No regularisation has ever been tried here.** The capacity sweep
    reached gaps of 2.659 between training and held-out loss, which is heavy
    overfitting, and dropout is the cheapest response. Zero by default so
    the change is measured rather than assumed.
    """

    norm: str = "layer"
    """`layer` or `rms`. RMSNorm drops the mean subtraction and the bias."""

    feed: str = "gelu"
    """`gelu` or `swiglu`.

    SwiGLU is the modern default and uses three matrices where GELU uses
    two, so the hidden width is cut to eight thirds to keep the parameter
    count comparable. Otherwise a comparison measures size, not shape.
    """
    seq_len: int = 128
    tie_embeddings: bool = True
    """Whether the output head shares the input embedding's matrix.

    **Absent until 2026-09-26, and it was thirteen percent of the model.** At
    2,246 words and width 256 an untied head is 575,000 parameters against
    4.3 million total, spent on a second copy of what the embedding already
    holds. Tying is the usual choice for a model this small.
    """

    positions: str = "learned"
    """How position reaches attention: ``learned`` or ``rotary``.

    **`learned` is a table with one row per index, and that is why it scales
    badly here.** Measured 2026-09-26 on the same thirty held-out books: a
    128-token window reaches held-out 3.550 and one sequence per book at
    1,088 reaches 3.854, having seen four times the tokens. A 512 window
    reaches 3.935, so 512 and 1,088 are indistinguishable and both are far
    behind 128.

    At 128 each position row is seen by about eleven training sequences. At
    1,088 it is seen by a fifth of one, because a book is a single sequence
    and there are only 216 of them. **A table cannot be learned from that.**

    `rotary` makes position a function of relative distance instead, so
    there is nothing per index to learn and nothing to starve. It is
    offered alongside rather than replacing `learned`, so the comparison
    stays inside one codebase and old checkpoints still load.

    **CORRECTED 2026-09-27. Old checkpoints stopped loading the next day.**
    Unifying the two position paths into one `Block` renamed the module
    attribute from `rotary_blocks` to `blocks`, and nothing compared a
    written checkpoint against the code that would read it.
    `RENAMED_PARAMETERS` carries the rename, so the claim is true again.
    """


@dataclass(frozen=True, slots=True)
class TrainConfig:
    steps: int = 2000
    batch_size: int = 16
    learning_rate: float = 3e-4
    warmup: int = 100
    min_lr_fraction: float = 0.1
    eval_batches: int = 24


def rotary_table(
    head_dim: int, length: int, device: torch.device, base: float = 10000.0
) -> tuple[Tensor, Tensor]:
    """Cosine and sine tables for rotary position embedding.

    Half the head dimension is rotated against the other half, so the table
    is built over ``head_dim // 2`` frequencies and each is used twice.
    """
    half = head_dim // 2
    inverse = 1.0 / (
        base ** (torch.arange(0, half, device=device, dtype=torch.float32) / half)
    )
    angles = torch.outer(
        torch.arange(length, device=device, dtype=torch.float32), inverse
    )
    return angles.cos(), angles.sin()


def apply_rotary(x: Tensor, cos: Tensor, sin: Tensor) -> Tensor:
    """Rotate the halves of each head's vector by the position's angle.

    ``x`` is (batch, heads, length, head_dim). The rotation is the standard
    one: the first half and second half of the head dimension are treated
    as the real and imaginary parts of a complex vector and multiplied by
    ``e^{i*theta}``.
    """
    first, second = x.chunk(2, dim=-1)
    cos = cos[None, None, : x.shape[2], :]
    sin = sin[None, None, : x.shape[2], :]
    return torch.cat((first * cos - second * sin, first * sin + second * cos), dim=-1)


class CausalSelfAttention(nn.Module):
    """Multi-head causal attention, written out so rotary can reach Q and K.

    **`nn.TransformerEncoderLayer` computes attention internally**, so there
    is no way to rotate its queries and keys from outside. This is the
    smallest amount of hand-written attention that admits rotary position,
    and it uses `scaled_dot_product_attention` so the kernel is still
    torch's rather than ours.

    **BOTH POSITION SCHEMES NOW USE THIS BLOCK, and until 2026-09-26 only
    rotary did.** The learned path used `nn.TransformerEncoderLayer`, which
    carries biases on its projections where this does not: thirteen bias
    tensors against nine. So the measured 0.4 nats attributed to rotary was
    confounded with bias removal and with whatever else the two
    implementations differ in. Sharing the block makes position the only
    difference, which is what the comparison claimed to be measuring.
    """

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        heads = head_count(config.d_model, config.n_heads)
        if config.d_model % heads:
            raise ValueError(
                f"d_model {config.d_model} is not divisible by {heads} head(s)"
            )
        self.n_heads = heads
        self.head_dim = config.d_model // heads
        self.dropout = nn.Dropout(config.dropout)
        if self.head_dim % 2:
            raise ValueError(
                f"rotary needs an even head dimension, got {self.head_dim} "
                f"from d_model {config.d_model} over {heads} head(s)"
            )
        self.qkv = nn.Linear(config.d_model, 3 * config.d_model, bias=False)
        self.out = nn.Linear(config.d_model, config.d_model, bias=False)

    def forward(self, hidden: Tensor, cos: Tensor | None, sin: Tensor | None) -> Tensor:
        batch, length, _ = hidden.shape
        qkv = self.qkv(hidden).view(batch, length, 3, self.n_heads, self.head_dim)
        query, key, value = (qkv[:, :, i].transpose(1, 2) for i in range(3))
        if cos is not None and sin is not None:
            query = apply_rotary(query, cos, sin)
            key = apply_rotary(key, cos, sin)
        attended = torch.nn.functional.scaled_dot_product_attention(
            query, key, value, is_causal=True
        )
        merged = attended.transpose(1, 2).reshape(batch, length, -1)
        return self.dropout(self.out(merged))


def _norm(config: ModelConfig) -> nn.Module:
    if config.norm == "rms":
        return nn.RMSNorm(config.d_model)
    if config.norm != "layer":
        raise ValueError(f"norm must be 'layer' or 'rms', got {config.norm!r}")
    return nn.LayerNorm(config.d_model)


class SwiGLU(nn.Module):
    """Gated feed-forward, as Llama and PaLM use.

    **The hidden width is eight thirds rather than four times.** SwiGLU needs
    three matrices where GELU needs two, so keeping the multiplier at four
    would make it half again as large and a comparison against GELU would be
    measuring size rather than shape.
    """

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        hidden = int(8 * config.d_model / 3)
        hidden += -hidden % 8
        self.gate = nn.Linear(config.d_model, hidden, bias=False)
        self.up = nn.Linear(config.d_model, hidden, bias=False)
        self.down = nn.Linear(hidden, config.d_model, bias=False)
        self.drop = nn.Dropout(config.dropout)

    def forward(self, hidden: Tensor) -> Tensor:
        return self.drop(
            self.down(nn.functional.silu(self.gate(hidden)) * self.up(hidden))
        )


def _feed(config: ModelConfig) -> nn.Module:
    if config.feed == "swiglu":
        return SwiGLU(config)
    if config.feed != "gelu":
        raise ValueError(f"feed must be 'gelu' or 'swiglu', got {config.feed!r}")
    return nn.Sequential(
        nn.Linear(config.d_model, 4 * config.d_model),
        nn.GELU(),
        nn.Linear(4 * config.d_model, config.d_model),
        nn.Dropout(config.dropout),
    )


class Block(nn.Module):
    """Pre-norm block: causal attention, then a feed-forward.

    Rotary is applied only when tables are passed, so the same block serves
    both position schemes and neither gets an advantage the comparison was
    not meant to measure.
    """

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.norm_attention = _norm(config)
        self.attention = CausalSelfAttention(config)
        self.norm_feed = _norm(config)
        self.feed = _feed(config)

    def forward(self, hidden: Tensor, cos: Tensor | None, sin: Tensor | None) -> Tensor:
        hidden = hidden + self.attention(self.norm_attention(hidden), cos, sin)
        return hidden + self.feed(self.norm_feed(hidden))


class TinyTransformer(nn.Module):
    """A conventional decoder-only transformer, and nothing more.

    Standard by intent. The ablation's architecture decision forbids
    deviation, and the pilot should share the setup whose variance it claims
    to measure.
    """

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        if config.positions not in ("learned", "rotary"):
            raise ValueError(
                f"positions must be 'learned' or 'rotary', got {config.positions!r}"
            )
        self.config = config
        self.rotary = config.positions == "rotary"
        self.token = nn.Embedding(config.vocab_size, config.d_model)
        # **No table at all under rotary**, so nothing scales with the
        # sequence length and nothing has to be learned per index.
        self.position = (
            None if self.rotary else nn.Embedding(config.seq_len, config.d_model)
        )
        self.blocks = nn.ModuleList(Block(config) for _ in range(config.n_layers))
        self.norm = nn.LayerNorm(config.d_model)
        self.head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        if config.tie_embeddings:
            # **The head and the embedding are one matrix.** Untied, the head
            # is vocab_size by d_model, which at 2,246 words and width 256 is
            # 575,000 of 4.3 million parameters: thirteen percent of the model
            # spent on a second copy of what the embedding already holds.
            self.head.weight = self.token.weight
        self.apply(self._initialise)
        # **Residual projections are scaled down by the depth.** Without it
        # the variance of the residual stream grows with the layer count. This
        # is the GPT-2 initialisation and it was not being done.
        for name, parameter in self.named_parameters():
            if name.endswith(
                ("feed.2.weight", "attention.out.weight", "feed.down.weight")
            ):
                with torch.no_grad():
                    _ = parameter.mul_(1.0 / math.sqrt(2 * config.n_layers))

    @staticmethod
    def _initialise(module: nn.Module) -> None:
        """Normal(0, 0.02), which is usual for a transformer and was not used.

        Default PyTorch initialisation is uniform and scaled by fan-in, which
        suits a plain multilayer network rather than this.
        """
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            # Every Linear here is built with bias=False except the feed
            # forward's two, and pyright knows the attribute is a Parameter
            # rather than an optional, so the guard is on the module kind.
            if "bias" in dict(module.named_parameters()):
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, tokens: Tensor) -> Tensor:
        length = tokens.shape[1]
        hidden = self.token(tokens)
        cos: Tensor | None = None
        sin: Tensor | None = None
        if self.rotary:
            head_dim = self.config.d_model // head_count(
                self.config.d_model, self.config.n_heads
            )
            cos, sin = rotary_table(head_dim, length, tokens.device)
        else:
            if self.position is None:
                raise RuntimeError("learned positions were asked for and none exist")
            hidden = hidden + self.position(torch.arange(length, device=tokens.device))
        for block in self.blocks:
            hidden = block(hidden, cos, sin)
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


def _summed_loss(
    model: TinyTransformer,
    batches: list[tuple[Tensor, Tensor]],
    model_config: ModelConfig,
    pad_id: int | None,
) -> tuple[float, int]:
    """Total loss and the number of tokens it was measured over.

    **A mean of per-batch means is the wrong average when batches hold
    different numbers of real tokens**, and they do whenever anything is
    padded. It gave a batch that was mostly padding the same weight as a full
    one. At 128 tokens 6.8 percent of slots are padding and at 1,088 it is
    25.6, so the error grew with the sequence length and therefore fell
    hardest on exactly the arm this project was comparing.

    Summing and dividing once by the token count is the per-token figure the
    documents have been calling held-out loss all along.
    """
    objective = (
        nn.CrossEntropyLoss(reduction="sum")
        if pad_id is None
        else nn.CrossEntropyLoss(reduction="sum", ignore_index=pad_id)
    )
    total = 0.0
    counted = 0
    with torch.no_grad():
        for inputs, targets in batches:
            logits = model(inputs)
            flat = targets.reshape(-1)
            total += float(objective(logits.reshape(-1, model_config.vocab_size), flat))
            counted += int(
                flat.numel() if pad_id is None else int((flat != pad_id).sum())
            )
    return total, counted


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
    all_eval = _batches(held_out, order_eval, train_config.batch_size, device)
    eval_batches = all_eval[: train_config.eval_batches]
    # **A partial evaluation must say so.** This took the first
    # `eval_batches` batches in index order, which for a held-out set that is
    # the tail of the curriculum is a systematic slice and not a sample. At
    # 267 held-out chunks and batch 8 that was 24 of 33 batches, so every
    # held-out figure this project has reported came from 73 percent of its
    # own held-out set, silently.
    if len(eval_batches) < len(all_eval):
        print(
            f"  NOTE: held-out loss over {len(eval_batches)} of "
            f"{len(all_eval)} batches; raise eval_batches to use them all",
            file=sys.stderr,
        )
    total, counted = _summed_loss(model, eval_batches, model_config, pad_id)
    # **Training loss is measured in eval mode over the same batches**, not
    # taken from the last step of the loop. A running figure is dominated
    # by whichever batch happened to come last and by dropout, and it is
    # the gap that this number exists to make meaningful.
    train_total, train_counted = _summed_loss(
        model, batches[: train_config.eval_batches], model_config, pad_id
    )
    return TrainResult(
        model=model,
        held_out_loss=total / max(counted, 1),
        train_loss=train_total / max(train_counted, 1),
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


LEGACY_MODEL_DEFAULTS: Final[dict[str, object]] = {
    "n_heads": 4,
    "dropout": 0.0,
    "norm": "layer",
    "feed": "gelu",
    "tie_embeddings": False,
    "positions": "learned",
}
"""What a field meant in a checkpoint written before it was recorded.

**A field absent from a checkpoint takes the value it had then, never the
value it defaults to now.** `n_heads` was fixed at four rather than derived
and the head was untied, and both changed on 2026-09-26. The other four
entries repeat today's default, and they are listed anyway so that this
mapping covers every optional field rather than only the two that moved.

**The tying case fails silently, which is why this exists.** Under tying
`head.weight` and `token.weight` are one storage, so an untied checkpoint
holding two different matrices loads with one overwriting the other,
`load_state_dict` reports nothing wrong, and the model is simply not the one
that was trained. The level-one checkpoint of 2026-09-26 holds two matrices
differing by 4.58, so this is the live case and not a hypothetical.

**A field here and not in the checkpoint is recoverable. A field in neither
is not**, and `load_checkpoint` refuses rather than inventing one. That is
what makes adding a field to `ModelConfig` without a historical value a loud
failure instead of a quiet reinterpretation of every checkpoint on disk.
"""

RENAMED_PARAMETERS: Final[tuple[tuple[str, str], ...]] = (
    ("rotary_blocks.", "blocks."),
)
"""Parameter prefixes that have been renamed, old name first.

**The two position paths were unified into one `Block` on 2026-09-26** and
the attribute holding the layers went from `rotary_blocks` to `blocks`. The
tensors are the same ten per layer under the same names, so this is a
relabelling rather than a reinterpretation, which is why remapping is
admissible here where guessing at a shape would not be.
"""


def renamed_parameters(state: Mapping[str, Tensor]) -> dict[str, Tensor]:
    """Apply every recorded rename to the names in a loaded state dict."""
    out: dict[str, Tensor] = {}
    for name, tensor in state.items():
        current = name
        for old, new in RENAMED_PARAMETERS:
            if current.startswith(old):
                current = new + current[len(old) :]
                break
        out[current] = tensor
    return out


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

    **The config is written whole rather than field by field.** Enumerated
    by hand it recorded five of ten fields, so `n_heads`, `dropout`, `norm`,
    `feed` and `tie_embeddings` were all absent and a checkpoint reloaded
    into whatever those default to today.

    **Three of those five omissions are silent and two are loud**, measured
    2026-09-27 by dropping each field from a written checkpoint in turn.
    `norm` and `feed` are loud, because RMSNorm and SwiGLU carry different
    parameter names and the load refuses. `n_heads`, `tie_embeddings` and
    `dropout` are silent, because every tensor still fits. **`n_heads` is the
    worst of the three**: written at two and read back as four, the model
    loads without complaint and splits attention differently than it was
    trained to. No shape check can see that, which is why the field must be
    recorded rather than inferred.

    This is the fourth instance in
    this repository of a record built from a subset of its own dataclass's
    fields, after three in the book code, and the remedy is the same one:
    derive the field list instead of retyping it.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(  # pyright: ignore[reportUnknownMemberType]
        {
            "state": model.state_dict(),
            "words": list(words),
            "config": asdict(config),
        },
        path,
    )


@dataclass(frozen=True, slots=True)
class Checkpoint:
    """A trained model with the vocabulary and shape it was trained at."""

    model: TinyTransformer
    words: tuple[str, ...]
    config: ModelConfig


def verify_loaded(
    model: TinyTransformer, state: Mapping[str, Tensor], path: Path
) -> None:
    """Confirm every saved tensor is in the model unchanged after loading.

    **`load_state_dict` checks names and shapes, not aliasing.** Where two
    parameters share one storage, loading a checkpoint that holds two
    different matrices for them succeeds, the second assignment overwrites
    the first, and nothing anywhere says so. That is not a shape error and no
    existing check would see it.

    This is the guard for that class, and it was written after being shown to
    fail: loading the untied level-one checkpoint into a tied model raises
    here and loaded silently before.
    """
    loaded = model.state_dict()
    for name, expected in state.items():
        here = loaded.get(name)
        if here is None:
            continue
        if not torch.equal(here.detach().cpu(), expected.detach().cpu()):
            raise ValueError(
                f"{path}: {name} does not match the checkpoint after loading. "
                "Two parameters most likely share one storage, so one "
                "overwrote the other, and the model is not the one that was "
                "trained."
            )


def load_checkpoint(path: Path, device: torch.device) -> Checkpoint:
    """Rebuild a model at the shape its checkpoint was written with.

    **Nothing is inferred from the caller.** A checkpoint that carries its
    own shape cannot be loaded into the wrong one, which is the failure
    this replaces: an error message blaming the model width when the
    vocabulary had grown by six words.

    A checkpoint written before this format is refused with a message
    saying so, rather than being guessed at.

    **A field the checkpoint does not carry is filled from
    `LEGACY_MODEL_DEFAULTS`, which is what it meant then**, and a renamed
    parameter is remapped through `RENAMED_PARAMETERS`. Both are
    relabellings of a structure that is verified to match, so neither is a
    guess. Anything that does not reconcile raises `ValueError`, because
    every caller here reports that and none reports a bare torch
    `RuntimeError`.
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
    saved = cast("dict[str, object]", body["config"])
    missing = [
        field.name
        for field in fields(ModelConfig)
        if field.name not in saved and field.name not in LEGACY_MODEL_DEFAULTS
    ]
    if missing:
        raise ValueError(
            f"{path} records no {', '.join(missing)} and there is no historical "
            "value to fall back on, so the shape it was trained at is unknown. "
            "Retrain to write one in the current format."
        )
    # **Older checkpoints predate several of these fields.** Absent ones
    # take the value they had then, never today's default.
    config = ModelConfig(
        vocab_size=cast("int", saved["vocab_size"]),
        d_model=cast("int", saved["d_model"]),
        n_layers=cast("int", saved["n_layers"]),
        n_heads=cast("int", saved.get("n_heads", LEGACY_MODEL_DEFAULTS["n_heads"])),
        dropout=cast("float", saved.get("dropout", LEGACY_MODEL_DEFAULTS["dropout"])),
        norm=cast("str", saved.get("norm", LEGACY_MODEL_DEFAULTS["norm"])),
        feed=cast("str", saved.get("feed", LEGACY_MODEL_DEFAULTS["feed"])),
        seq_len=cast("int", saved["seq_len"]),
        tie_embeddings=cast(
            "bool",
            saved.get("tie_embeddings", LEGACY_MODEL_DEFAULTS["tie_embeddings"]),
        ),
        positions=cast(
            "str", saved.get("positions", LEGACY_MODEL_DEFAULTS["positions"])
        ),
    )
    model = TinyTransformer(config).to(device)
    state = renamed_parameters(cast("Mapping[str, Tensor]", body["state"]))
    try:
        _ = model.load_state_dict(state)
    except RuntimeError as exc:
        raise ValueError(
            f"{path} does not fit a model built from the config it carries. "
            f"torch says: {exc}"
        ) from exc
    verify_loaded(model, state, path)
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

    **A state sharing no name with the model is refused.** A missing key
    means "keep the fresh initialisation", which is right for one parameter
    and means "copy nothing at all" for every parameter at once. Until
    2026-09-27 `train_level.py` passed the whole checkpoint payload here
    rather than its `state` entry, so every key missed, nothing was copied,
    zero was returned, and the caller printed that it had warm started. A
    tool that returns less than it was asked for must say so.
    """
    target = model.state_dict()
    if not any(name in state for name in target):
        raise ValueError(
            "the warm-start state shares no parameter name with the model, so "
            "nothing would be copied. A whole checkpoint payload was most "
            "likely passed where its 'state' entry belongs."
        )
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
