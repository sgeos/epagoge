"""Tests for the pilot harness.

Skipped entirely when the optional ``train`` dependency group is absent, so
the gate runs in an environment without it.

The data generator is tested directly, because the first pilot run produced
a paired difference of exactly zero and the cause was a stream with no
learnable structure rather than anything about the model.
"""

from __future__ import annotations

import tempfile
import unittest
from dataclasses import fields
from pathlib import Path
from typing import cast

try:
    from epagoge.pilot import (
        LEGACY_MODEL_DEFAULTS,
        ModelConfig,
        TinyTransformer,
        TrainConfig,
        WarmStart,
        apply_rotary,
        chunk,
        head_count,
        load_checkpoint,
        orderings,
        renamed_parameters,
        rotary_table,
        sample,
        save_checkpoint,
        select_device,
        synthetic_stream,
        verify_loaded,
        warm_start,
    )

    HAVE_TORCH = True
except ImportError:  # pragma: no cover - exercised only without the extra
    HAVE_TORCH = False


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestStream(unittest.TestCase):
    def test_stream_is_reproducible_from_a_seed(self) -> None:
        self.assertEqual(synthetic_stream(500, 32, 7), synthetic_stream(500, 32, 7))

    def test_different_seeds_differ(self) -> None:
        self.assertNotEqual(synthetic_stream(500, 32, 1), synthetic_stream(500, 32, 2))

    def test_tokens_stay_inside_the_vocabulary(self) -> None:
        stream = synthetic_stream(2000, 16, 3)
        self.assertTrue(all(0 <= t < 16 for t in stream))

    def test_the_stream_has_learnable_structure(self) -> None:
        """Each context admits at most three successors, so it is predictable.

        The first pilot used a vocabulary of 256, which gave 65,536 contexts
        over 200,000 tokens, about three visits each. There was nothing to
        learn and every ordering produced an identical result.
        """
        vocab = 32
        stream = synthetic_stream(20_000, vocab, 5)
        successors: dict[tuple[int, int], set[int]] = {}
        for i in range(2, len(stream)):
            key = (stream[i - 2], stream[i - 1])
            successors.setdefault(key, set()).add(stream[i])
        self.assertTrue(all(len(s) <= 3 for s in successors.values()))
        visits = len(stream) / (vocab**2)
        self.assertGreater(visits, 10.0, "contexts must repeat often enough to learn")


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestChunking(unittest.TestCase):
    def test_each_chunk_carries_one_extra_token_for_the_target(self) -> None:
        chunks = chunk(list(range(1000)), 64)
        self.assertTrue(all(len(c) == 65 for c in chunks))

    def test_chunks_do_not_overrun_the_stream(self) -> None:
        stream = list(range(1000))
        for c in chunk(stream, 64):
            self.assertLessEqual(c[-1], stream[-1])


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestOrderings(unittest.TestCase):
    def test_both_orderings_are_permutations(self) -> None:
        a, b = orderings(50, seed=1)
        self.assertEqual(sorted(a), list(range(50)))
        self.assertEqual(sorted(b), list(range(50)))

    def test_orderings_differ(self) -> None:
        a, b = orderings(50, seed=1)
        self.assertNotEqual(a, b)

    def test_orderings_are_reproducible(self) -> None:
        self.assertEqual(orderings(50, seed=1), orderings(50, seed=1))


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestSchedule(unittest.TestCase):
    def test_warmup_rises_then_decay_falls(self) -> None:
        from epagoge.pilot import _schedule

        config = TrainConfig(steps=1000, warmup=100, learning_rate=1e-3)
        first = _schedule(0, config)
        peak = _schedule(99, config)
        late = _schedule(999, config)
        self.assertLess(first, peak)
        self.assertLess(late, peak)

    def test_the_rate_never_stays_at_peak(self) -> None:
        """Warmup with no decay made four thousand steps worse than two thousand."""
        from epagoge.pilot import _schedule

        config = TrainConfig(steps=1000, warmup=100, learning_rate=1e-3)
        self.assertLess(_schedule(999, config), _schedule(100, config))


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestModelConfig(unittest.TestCase):
    def test_vocabulary_is_small_enough_for_contexts_to_repeat(self) -> None:
        self.assertLessEqual(ModelConfig().vocab_size, 64)


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestPaddedChunking(unittest.TestCase):
    """A book's tail is kept rather than dropped.

    Measured 2026-09-25, chunking 146 level-one books at 128 without
    padding kept 8,772 of 35,438 tokens, and every book shorter than 129
    tokens produced nothing at all.
    """

    def test_without_padding_a_short_stream_yields_nothing(self) -> None:
        self.assertEqual(chunk(list(range(100)), 128), [])

    def test_with_padding_a_short_stream_yields_one_chunk(self) -> None:
        pieces = chunk(list(range(100)), 128, pad=0)
        self.assertEqual(len(pieces), 1)
        self.assertEqual(len(pieces[0]), 129)
        self.assertEqual(pieces[0][:100], list(range(100)))
        self.assertEqual(set(pieces[0][100:]), {0})

    def test_padding_keeps_every_token_of_a_long_stream(self) -> None:
        stream = list(range(300))
        pieces = chunk(stream, 128, pad=-1)
        self.assertTrue(all(len(p) == 129 for p in pieces))
        kept = [t for p in pieces for t in p if t != -1]
        self.assertEqual(set(kept), set(stream))

    def test_an_exhausted_stream_stops_rather_than_padding_a_whole_chunk(
        self,
    ) -> None:
        """A chunk of pure padding teaches nothing and is not emitted."""
        pieces = chunk(list(range(129)), 128, pad=0)
        self.assertEqual(len(pieces), 1)

    def test_a_stream_too_short_to_predict_yields_nothing(self) -> None:
        self.assertEqual(chunk([7], 128, pad=0), [])


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestSampling(unittest.TestCase):
    """Sampling exists so that something other than a loss can be read.

    An untrained model is enough to test the contract. What it says is
    noise, and that is the point: these check the shape of the call, not
    the quality of the text.
    """

    def model(self) -> TinyTransformer:
        return TinyTransformer(
            ModelConfig(vocab_size=32, d_model=16, n_layers=1, seq_len=8)
        ).to(select_device("cpu"))

    def test_it_returns_the_requested_count(self) -> None:
        out = sample(self.model(), [1], 5, select_device("cpu"), seq_len=8)
        self.assertEqual(len(out), 5)

    def test_the_prompt_is_not_returned(self) -> None:
        out = sample(self.model(), [1, 2, 3], 4, select_device("cpu"), seq_len=8)
        self.assertEqual(len(out), 4)

    def test_one_seed_gives_one_answer(self) -> None:
        model = self.model()
        first = sample(model, [1], 6, select_device("cpu"), seed=7, seq_len=8)
        second = sample(model, [1], 6, select_device("cpu"), seed=7, seq_len=8)
        self.assertEqual(first, second)

    def test_a_context_longer_than_the_window_is_truncated(self) -> None:
        """The positional embedding is only seq_len long, so a longer
        prompt must not reach the model."""
        out = sample(self.model(), list(range(20)), 3, select_device("cpu"), seq_len=8)
        self.assertEqual(len(out), 3)

    def test_zero_tokens_is_an_empty_answer(self) -> None:
        self.assertEqual(
            sample(self.model(), [1], 0, select_device("cpu"), seq_len=8), []
        )

    def test_a_non_positive_temperature_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            _ = sample(self.model(), [1], 1, select_device("cpu"), temperature=0.0)

    def test_a_negative_count_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            _ = sample(self.model(), [1], -1, select_device("cpu"))


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestWarmStart(unittest.TestCase):
    """Level N starts from the level N minus one model.

    The vocabulary grows between levels, so a row is matched by the word
    it stands for rather than by its position. A word in both lexicons
    keeps what it learned, a new word keeps its fresh initialisation, and
    a departed word is dropped.
    """

    def build(self, vocab: int) -> TinyTransformer:
        return TinyTransformer(
            ModelConfig(vocab_size=vocab, d_model=8, n_layers=1, seq_len=4)
        )

    def test_a_shared_word_keeps_its_vector(self) -> None:
        import torch

        older = ["<pad>", "cup", "water"]
        newer = ["<pad>", "air", "cup", "water"]
        source = self.build(len(older))
        target = self.build(len(newer))
        kept = warm_start(target, source.state_dict(), older, newer)
        self.assertEqual(kept, 3)
        self.assertTrue(
            torch.equal(
                target.state_dict()["token.weight"][2],
                source.state_dict()["token.weight"][1],
            )
        )

    def test_a_new_word_keeps_its_fresh_row(self) -> None:
        import torch

        older = ["<pad>", "cup"]
        newer = ["<pad>", "cup", "air"]
        target = self.build(len(newer))
        fresh = target.state_dict()["token.weight"][2].clone()
        _ = warm_start(target, self.build(len(older)).state_dict(), older, newer)
        self.assertTrue(torch.equal(target.state_dict()["token.weight"][2], fresh))

    def test_a_departed_word_is_dropped_without_error(self) -> None:
        older = ["<pad>", "cup", "gone"]
        newer = ["<pad>", "cup"]
        target = self.build(len(newer))
        kept = warm_start(target, self.build(len(older)).state_dict(), older, newer)
        self.assertEqual(kept, 2)

    def test_a_differently_shaped_body_is_refused(self) -> None:
        """A checkpoint from a wider model is a mistake, not a warm start."""
        older = ["<pad>", "cup"]
        wide = TinyTransformer(
            ModelConfig(vocab_size=2, d_model=16, n_layers=1, seq_len=4)
        )
        with self.assertRaises(ValueError):
            _ = warm_start(self.build(2), wide.state_dict(), older, older)

    def test_the_dataclass_carries_both_vocabularies(self) -> None:
        older = ["<pad>", "cup"]
        newer = ["<pad>", "cup", "air"]
        warm = WarmStart(state={}, older=older, newer=newer)
        self.assertEqual(list(warm.older), older)
        self.assertEqual(list(warm.newer), newer)


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestRotaryPositions(unittest.TestCase):
    """Rotary position embedding, checked on the properties that matter.

    **Added 2026-09-26 with the implementation.** A learned position table
    starves at long sequences: measured on the same thirty held-out books,
    a 128-token window reaches held-out 3.550 while one sequence per book
    at 1,088 reaches 3.854 having seen four times the tokens. Rotary makes
    position a function of relative distance, so there is nothing per index
    to learn. It is hand-written because `nn.TransformerEncoderLayer`
    computes attention internally and rotary has to reach Q and K.
    """

    def config(self, positions: str, seq_len: int = 16) -> ModelConfig:
        return ModelConfig(
            vocab_size=8,
            d_model=16,
            n_layers=2,
            n_heads=2,
            seq_len=seq_len,
            positions=positions,
        )

    def test_rotation_at_position_zero_is_the_identity(self) -> None:
        """cos(0) is one and sin(0) is zero, so nothing moves."""
        import torch

        cos, sin = rotary_table(8, 4, torch.device("cpu"))
        x = torch.randn(1, 1, 4, 8)
        rotated = apply_rotary(x, cos, sin)
        self.assertTrue(torch.allclose(rotated[:, :, 0], x[:, :, 0], atol=1e-6))

    def test_rotation_preserves_the_norm(self) -> None:
        """A rotation is not allowed to change how long a vector is."""
        import torch

        cos, sin = rotary_table(8, 6, torch.device("cpu"))
        x = torch.randn(2, 3, 6, 8)
        rotated = apply_rotary(x, cos, sin)
        self.assertTrue(torch.allclose(x.norm(dim=-1), rotated.norm(dim=-1), atol=1e-5))

    def test_a_rotary_model_is_causal(self) -> None:
        """Changing the last token must not change any earlier output.

        **This is the property a hand-written attention is most likely to
        break**, and it would break silently: the loss would improve because
        the model could see the answer.
        """
        import torch

        torch.manual_seed(0)
        model = TinyTransformer(self.config("rotary")).eval()
        tokens = torch.tensor([[1, 2, 3, 4, 5]])
        with torch.no_grad():
            before = model(tokens)
            changed = tokens.clone()
            changed[0, -1] = 7
            after = model(changed)
        self.assertTrue(torch.allclose(before[:, :-1], after[:, :-1], atol=1e-5))
        self.assertFalse(torch.allclose(before[:, -1], after[:, -1], atol=1e-5))

    def test_a_rotary_model_has_no_position_table(self) -> None:
        """The whole point. Nothing scales with the sequence length."""
        model = TinyTransformer(self.config("rotary"))
        self.assertIsNone(model.position)
        names = {name for name, _ in model.named_parameters()}
        self.assertNotIn("position.weight", names)

    def test_a_rotary_model_does_not_grow_with_the_sequence_length(self) -> None:
        short = TinyTransformer(self.config("rotary", seq_len=16))
        long = TinyTransformer(self.config("rotary", seq_len=1024))
        self.assertEqual(
            sum(p.numel() for p in short.parameters()),
            sum(p.numel() for p in long.parameters()),
        )

    def test_a_learned_model_does_grow_with_the_sequence_length(self) -> None:
        """The contrast, so the reason for rotary is in the tests too."""
        short = TinyTransformer(self.config("learned", seq_len=16))
        long = TinyTransformer(self.config("learned", seq_len=1024))
        self.assertLess(
            sum(p.numel() for p in short.parameters()),
            sum(p.numel() for p in long.parameters()),
        )

    def test_an_unknown_position_scheme_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            _ = TinyTransformer(self.config("sinusoidal"))


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestArchitectureOptions(unittest.TestCase):
    """The four enhancements found by auditing on 2026-09-26.

    Each is a config option so it is measured rather than assumed, except the
    head count, which was a defect: it was fixed at four regardless of width,
    so width 1,024 ran with a head dimension of 256 where 64 to 128 is
    standard.
    """

    def config(self, **kwargs: object) -> ModelConfig:
        base = {
            "vocab_size": 32,
            "d_model": 64,
            "n_layers": 2,
            "seq_len": 16,
            "positions": "rotary",
        }
        return ModelConfig(**{**base, **kwargs})  # type: ignore[arg-type]

    def test_heads_are_derived_to_keep_the_head_dimension_near_sixty_four(
        self,
    ) -> None:
        for width, expected in ((64, 1), (128, 2), (256, 4), (512, 8), (1024, 16)):
            self.assertEqual(head_count(width, 0), expected)
            self.assertEqual(width // head_count(width, 0), 64)

    def test_a_narrow_model_still_gets_one_head(self) -> None:
        self.assertEqual(head_count(16, 0), 1)
        self.assertEqual(head_count(32, 0), 1)

    def test_an_explicit_head_count_still_wins(self) -> None:
        """A sweep over head count is a legitimate thing to want."""
        self.assertEqual(head_count(256, 4), 4)
        self.assertEqual(head_count(256, 1), 1)

    def test_every_norm_and_feed_combination_builds_and_is_causal(self) -> None:
        import torch

        for norm in ("layer", "rms"):
            for feed in ("gelu", "swiglu"):
                torch.manual_seed(0)
                model = TinyTransformer(self.config(norm=norm, feed=feed)).eval()
                tokens = torch.tensor([[1, 2, 3, 4, 5]])
                with torch.no_grad():
                    before = model(tokens)
                    changed = tokens.clone()
                    changed[0, -1] = 7
                    after = model(changed)
                self.assertTrue(
                    torch.allclose(before[:, :-1], after[:, :-1], atol=1e-5),
                    f"{norm} and {feed} broke causality",
                )

    def test_swiglu_stays_comparable_in_size_to_gelu(self) -> None:
        """Otherwise a comparison measures size rather than shape."""
        gelu = TinyTransformer(self.config(feed="gelu"))
        swiglu = TinyTransformer(self.config(feed="swiglu"))
        a = sum(p.numel() for p in gelu.parameters())
        b = sum(p.numel() for p in swiglu.parameters())
        self.assertLess(abs(a - b) / a, 0.05)

    def test_dropout_changes_training_output_and_not_evaluation_output(self) -> None:
        import torch

        torch.manual_seed(0)
        model = TinyTransformer(self.config(dropout=0.5))
        tokens = torch.tensor([[1, 2, 3, 4]])
        model.train()
        with torch.no_grad():
            self.assertFalse(torch.allclose(model(tokens), model(tokens)))
        model.eval()
        with torch.no_grad():
            self.assertTrue(torch.allclose(model(tokens), model(tokens)))

    def test_an_unknown_norm_or_feed_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            _ = TinyTransformer(self.config(norm="batch"))
        with self.assertRaises(ValueError):
            _ = TinyTransformer(self.config(feed="relu"))

    def test_tying_removes_the_head_from_the_parameter_count(self) -> None:
        tied = TinyTransformer(self.config(tie_embeddings=True))
        untied = TinyTransformer(self.config(tie_embeddings=False))
        saved = sum(p.numel() for p in untied.parameters()) - sum(
            p.numel() for p in tied.parameters()
        )
        self.assertEqual(saved, 32 * 64)


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestCheckpointRoundTrip(unittest.TestCase):
    """A checkpoint must reload as the model that was written, or say why not.

    **It did not, and the failure had two halves.** `save_checkpoint`
    recorded five of `ModelConfig`'s ten fields, so a reload rebuilt the five
    it omitted from whatever they default to today. And the module attribute
    holding the layers was renamed, so the level-one checkpoint stopped
    loading at all.

    **The loud half was the lucky half.** `tie_embeddings` defaults to true
    now and was absent then, and under tying the head and the embedding are
    one storage, so an untied checkpoint loads with one matrix overwriting
    the other and `load_state_dict` reports nothing. The rename is what
    turned a wrong model into an exception.
    """

    def config(self, **kwargs: object) -> ModelConfig:
        base = {
            "vocab_size": 12,
            "d_model": 64,
            "n_layers": 2,
            "seq_len": 16,
        }
        return ModelConfig(**{**base, **kwargs})  # type: ignore[arg-type]

    def words(self, count: int) -> list[str]:
        return ["<pad>"] + [f"w{n}" for n in range(1, count)]

    def write(self, config: ModelConfig, path: Path) -> TinyTransformer:
        import torch

        torch.manual_seed(0)
        model = TinyTransformer(config)
        save_checkpoint(model, config, self.words(config.vocab_size), path)
        return model

    def test_the_saved_config_carries_every_field_of_the_dataclass(self) -> None:
        """Enumerated by hand it carried five of ten, which is the defect."""
        import torch

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "m.pt"
            _ = self.write(self.config(), path)
            payload = torch.load(path, map_location="cpu")
        self.assertEqual(
            set(payload["config"]),
            {field.name for field in fields(ModelConfig)},
        )

    def test_every_field_survives_a_round_trip_at_a_non_default_value(self) -> None:
        """Set to a default, an omitted field round-trips by coincidence."""
        config = self.config(
            n_heads=2,
            dropout=0.25,
            norm="rms",
            feed="swiglu",
            tie_embeddings=False,
            positions="rotary",
        )
        for field in fields(ModelConfig):
            self.assertNotEqual(
                getattr(config, field.name),
                field.default,
                f"{field.name} is at its default, so this test cannot see it",
            )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "m.pt"
            _ = self.write(config, path)
            loaded = load_checkpoint(path, select_device("cpu"))
        self.assertEqual(loaded.config, config)

    def test_a_checkpoint_reloads_the_weights_it_was_written_with(self) -> None:
        import torch

        config = self.config(positions="rotary", tie_embeddings=False)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "m.pt"
            written = self.write(config, path)
            loaded = load_checkpoint(path, select_device("cpu"))
        before = written.state_dict()
        after = loaded.model.state_dict()
        self.assertEqual(set(before), set(after))
        for name, tensor in before.items():
            self.assertTrue(torch.equal(tensor, after[name]), name)

    def legacy(self, path: Path) -> dict[str, object]:
        """A payload in the format written before 2026-09-27.

        Five config fields, and the layers under `rotary_blocks`. Built from
        a real model so the tensors are the right shapes.
        """
        import torch

        config = self.config(positions="rotary", tie_embeddings=False)
        torch.manual_seed(1)
        model = TinyTransformer(config)
        state = {
            name.replace("blocks.", "rotary_blocks.", 1)
            if name.startswith("blocks.")
            else name: tensor
            for name, tensor in model.state_dict().items()
        }
        payload = {
            "state": state,
            "words": self.words(config.vocab_size),
            "config": {
                "vocab_size": config.vocab_size,
                "d_model": config.d_model,
                "n_layers": config.n_layers,
                "seq_len": config.seq_len,
                "positions": config.positions,
            },
        }
        torch.save(payload, path)
        return payload

    def test_a_legacy_checkpoint_loads_as_the_model_it_was(self) -> None:
        """Untied and four-headed, which is what those fields meant then."""
        import torch

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.pt"
            payload = self.legacy(path)
            loaded = load_checkpoint(path, select_device("cpu"))
        self.assertFalse(loaded.config.tie_embeddings)
        self.assertEqual(loaded.config.n_heads, LEGACY_MODEL_DEFAULTS["n_heads"])
        after = loaded.model.state_dict()
        expected = renamed_parameters(cast("dict[str, object]", payload["state"]))  # type: ignore[arg-type]
        self.assertEqual(set(expected), set(after))
        for name, tensor in expected.items():
            self.assertTrue(torch.equal(tensor, after[name]), name)

    def test_the_rename_is_applied_and_nothing_else_is_touched(self) -> None:
        import torch

        state = {
            "rotary_blocks.0.attention.qkv.weight": torch.zeros(1),
            "token.weight": torch.zeros(1),
        }
        self.assertEqual(
            set(renamed_parameters(state)),
            {"blocks.0.attention.qkv.weight", "token.weight"},
        )

    def test_two_parameters_sharing_one_storage_is_refused(self) -> None:
        """The silent failure, shown failing.

        This is what loading the untied level-one checkpoint into a tied
        model does. `load_state_dict` raises nothing and the model is wrong.
        """
        import torch

        config = self.config(positions="rotary", tie_embeddings=False)
        torch.manual_seed(2)
        untied = TinyTransformer(config).state_dict()
        tied = TinyTransformer(self.config(positions="rotary", tie_embeddings=True))
        _ = tied.load_state_dict(untied)
        with self.assertRaises(ValueError):
            verify_loaded(tied, untied, Path("in-memory"))

    def test_a_checkpoint_missing_a_shape_field_is_refused(self) -> None:
        """No historical value exists for these, so no value may be invented."""
        import torch

        for absent in ("vocab_size", "d_model", "n_layers", "seq_len"):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "old.pt"
                payload = self.legacy(path)
                config = cast("dict[str, object]", payload["config"])
                del config[absent]
                torch.save(payload, path)
                with self.assertRaises(ValueError) as caught:
                    _ = load_checkpoint(path, select_device("cpu"))
                self.assertIn(absent, str(caught.exception))

    def test_a_checkpoint_without_its_words_is_refused(self) -> None:
        import torch

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.pt"
            payload = self.legacy(path)
            del payload["words"]
            torch.save(payload, path)
            with self.assertRaises(ValueError):
                _ = load_checkpoint(path, select_device("cpu"))

    def test_a_state_that_does_not_fit_raises_a_value_error(self) -> None:
        """Callers report `ValueError`; none reports a torch `RuntimeError`."""
        import torch

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.pt"
            payload = self.legacy(path)
            state = cast("dict[str, object]", payload["state"])
            del state["token.weight"]
            torch.save(payload, path)
            with self.assertRaises(ValueError):
                _ = load_checkpoint(path, select_device("cpu"))


@unittest.skipUnless(HAVE_TORCH, "optional 'train' dependencies absent")
class TestWarmStartGuard(unittest.TestCase):
    """A warm start that copies nothing must say so rather than report zero.

    `train_level.py` passed the whole checkpoint payload where its `state`
    entry belongs, so every parameter name missed, every parameter kept its
    fresh initialisation, and the caller printed that it had warm started.
    """

    def model(self) -> TinyTransformer:
        return TinyTransformer(
            ModelConfig(vocab_size=3, d_model=8, n_layers=1, seq_len=4)
        )

    def test_a_payload_where_a_state_belongs_is_refused(self) -> None:
        import torch

        words = ["<pad>", "cup", "water"]
        payload = {
            "state": self.model().state_dict(),
            "words": words,
            "config": {},
        }
        with self.assertRaises(ValueError):
            _ = warm_start(
                self.model(),
                cast("dict[str, torch.Tensor]", payload),
                words,
                words,
            )

    def test_a_state_that_does_share_names_is_accepted(self) -> None:
        words = ["<pad>", "cup", "water"]
        kept = warm_start(self.model(), self.model().state_dict(), words, words)
        self.assertEqual(kept, len(words))
