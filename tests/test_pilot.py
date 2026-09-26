"""Tests for the pilot harness.

Skipped entirely when the optional ``train`` dependency group is absent, so
the gate runs in an environment without it.

The data generator is tested directly, because the first pilot run produced
a paired difference of exactly zero and the cause was a stream with no
learnable structure rather than anything about the model.
"""

from __future__ import annotations

import unittest

try:
    from epagoge.pilot import (
        ModelConfig,
        TinyTransformer,
        TrainConfig,
        WarmStart,
        apply_rotary,
        chunk,
        orderings,
        rotary_table,
        sample,
        select_device,
        synthetic_stream,
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
