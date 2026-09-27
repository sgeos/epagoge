# Structural tokens, and what the corpus announces

**Recorded 2026-09-27, after a literature spike, on operator direction.**
The question was raised as three: whether an end-of-text token matters,
whether a book title should carry a heading marker, and whether padding
should follow an end-of-work token. The spike answers the first and the
third from settled practice, and answers the second differently from the way
it was asked.

**What is measured here is measured on this tree.** What is cited is cited
from sources vendored into ignored `tmp/references/papers/`, listed at the
end. Nothing below is a result of this project.

## What this corpus does today, measured

Over all 399 level-one books, **356,975 training tokens**.

| Token | Count | Share |
| --- | --- | --- |
| `.` | 30,507 | 8.5% |
| `,` | 28,445 | 8.0% |
| `:` | 92 | 0.03% |
| `;` | 35 | 0.01% |
| `?` | 285 | 0.08% |
| `!` | 4 | 0.001% |
| `<book>` | **0** | **zero** |

**Sentence and clause boundaries are already fed and everything above the
sentence is discarded.** `WORD_RE` in `src/epagoge/tokeniser.py` matches
words, numerals and six punctuation marks. Newlines are not in the pattern,
so record boundaries vanish, and the front matter holding the title, the
`about` line and the `teaches` line never reaches the model at all.

**`<book>` is in the vocabulary, is the seed for every unprompted sample in
`tools/talk.py` and `tools/sample_level.py`, and occurs zero times in
training.** That is a defect rather than a design question.

**Only 45 of 399 books contain a question mark** and the seventeen books
with `form` set to `question` carry roughly a third of all of them. A model
trained here has seen 285 questions and about 30,500 sentence stops.

## What the literature supports

### Packing rather than padding, at the main stage

**Over 95 percent of frontier pre-training tokens are consumed at sequence
lengths of 8,192 or less**, and the token-weighted figure across four
families is 97.31 percent. Llama 3 ran 15.6T of roughly 16.4T at 8,192,
DeepSeek-V3 14.8T at 4,096, Qwen3 roughly 35T of 36T at 4,096, and Olmo 3's
7B 5.93T at 8,192.

At that stage a training sequence is not a document. **It is a packed
window, several short documents concatenated, and the attention mask usually
does not separate the neighbours.** Llama 3 reports document-separating
masks had limited impact in standard pre-training while being important in
continued pre-training on very long sequences, and DeepSeek-V3 packs
documents without cross-sample attention masking.

**Truncation from naive concatenation is measurably harmful.** Best-fit
Packing, at the International Conference on Machine Learning in 2024,
eliminates unnecessary truncation at the same efficiency as concatenation
and reports relative gains of 4.7 percent on reading comprehension, 16.8
percent in context following and 9.2 percent on program synthesis, with
closed-domain hallucination reduced by up to 58.3 percent.

**TinyStories is the closest precedent to this project and separates stories
with an end-of-text token**, which is how a reader learns where a story
stops.

### The announcement is the cue, and the notation is not

This is the finding that answers the heading question, and it answers it in
a way neither the question nor this project's first guess anticipated.

**A three-arm probe over twenty-one narrative and sustained-argument works**
serialises identical text three ways. The `marked` arm writes the structure
as Markdown, the `flat` arm keeps every word but drops the notation and
leaves the heading standing as a bare line, and the `silent` arm deletes the
announcement line entirely. Marked against flat isolates the sigil. Flat
against silent isolates the announcement.

**Deleting the announcement makes the following prose harder to predict at
every scale measured**, over five readers from 0.60B to 8.19B parameters and
two independent pre-training pipelines. The rise in millinats per byte is
+0.466 at 0.6B, +0.223 at 1.7B, +0.571 at 4B, +0.578 at a cross-family
reader and +0.459 at 8B, each with a lower bound above zero.

**Swapping the notation moves nothing.** Every reader's notation contrast
contains zero, tight against a pre-registered bound, with the widest
interval endpoint between 0.55 and 1.68 percent of that reader's measured
information gain against a threshold of 2 percent. In the authors' words, a
zero does not say notation is unimportant, it says the sigil is not the
operative cue. Present a chapter head as `## CHAPTER IV.` or as `CHAPTER
IV.` and a trained reader does the same thing with the prose that follows.

**So a structural marker should exist and its spelling is free.**

### Reserved tokens

**Llama 3 ships 256 reserved special tokens** alongside `<|begin_of_text|>`,
`<|end_of_text|>` and its role markers, unused at release and available
later. GPT-2 shipped essentially one special token, `<|endoftext|>`.

**The cost that practice avoids is concrete in this repository as of
today.** A vocabulary change invalidates every checkpoint, and
`docs/decisions/FIELD_ENUMERATION.md` records the machinery that now makes
that refusal loud rather than silent. Reserving slots means the next
structural token costs a corpus rebuild and not a vocabulary migration.

## What the literature refutes, including one of my own predictions

**The prediction was that structure should be ordinary Markdown text rather
than special tokens, and that is half right and stated wrongly.** The
measured claim is that the choice between a sigil and a bare line is a null.
It is not a finding that text beats tokens. The correction is kept here
rather than removed, because the reason the prediction was wrong is the
useful part: it treated notation as the variable when the variable is
presence.

**The earlier book-as-stream result is now interpretable rather than
refuted.** `evals/pilot/LEVEL_ONE_POSITIONS_AND_RETENTION.md` measured one
sequence per book at 1,088 as worse than a 128-token window. The literature
says the regime where a sequence is a document is the long-context stage,
which frontier runs reach with under one percent of their budget and with
intra-document masking switched on. This project ran that regime with
masking off and, as recorded in `docs/process/HANDOFF.md`, with 25.6 percent
of slots padding. **Those are two confounds in a comparison that was read as
being about sequence length.**

## What is not settled, and must not be claimed

**No training-time evidence exists.** The three-arm probe measures trained
readers at inference. Its authors state the limitation themselves, that it
measures reading and not training, and that it therefore cannot distinguish
an absent training pressure from readers that never formed the machinery.
Their own paper defers the question to a matched training run they had not
performed.

**One pre-registered rule fired against the paper's framing.** A rule asking
whether larger readers reconstruct a deleted announcement from context fired
at 1.7B, with an interval of +0.270 from +0.010, and did not replicate at
any of the three larger readers. The authors report it as a headline rather
than a footnote and say the honest form is that reconstruction is not ruled
out above 1.7B rather than that it has been shown.

**The source is a single-author preprint from August 2026 and is not peer
reviewed.** It is pre-registered and reports rules that went against it,
which is why it is used here, and neither property makes it settled.

**Whether attention should be reset at book boundaries under packing is
open.** Convention at the main stage is not to, and Llama 3 measured the
impact as limited. Against that stands the operator's standing requirement
that each picture book is a self-contained coherent work. This is recorded
as a tension rather than resolved by citation.

## Decisions

1. **An end-of-text token is added and emitted at the end of every book.**
   Universal practice, and the exact TinyStories precedent.
2. **Books are packed into windows separated by that token**, rather than
   one padded stream per book. This removes padding from the main path
   instead of masking it out of the loss.
3. **A block of reserved special tokens is added now**, unused, so that the
   next structural token does not invalidate every checkpoint.
4. **Structure is announced, and no token is minted per structure kind.** A
   book's title becomes an announcement line in the stream. By the notation
   null the spelling is free, so it is written as Markdown, which is the
   form level seven will arrive in anyway.

   > **BLOCKED, found 2026-09-27 while implementing the other four.** **47
   > of 399 titles contain a word the level-one lexicon does not carry**, so
   > announcing titles today would inject unknown tokens into 47 books. The
   > 27 offending words are `activity`, `amount`, `causal`, `chain`,
   > `claim`, `component`, `conservation`, `correspondence`, `cycle`,
   > `discourse`, `duration`, `effect`, `emptiness`, `exchange`,
   > `household`, `marker`, `object`, `physical`, `position`, `presence`,
   > `property`, `sequence`, `spatial`, `system` and three more.
   >
   > **Every one is a concept identifier, and every affected book is a
   > cross-concept book.** Their titles were built from concept names rather
   > than from lexicon words, which is a fourth instance of the rule already
   > recorded in `docs/process/HANDOFF.md`, that a concept name is not a
   > word. `generators/cross_books.py` uses `words_for` for prompts and the
   > title was not routed through it.
   >
   > **UNBLOCKED AND DONE 2026-09-27.** All 47 were rewritten by
   > `generators/retitle_books.py`, which asks the teacher for a title from
   > the book's own text and refuses anything outside the ceiling. 0 of 400
   > titles are now outside it, and a test asserts that.
   >
   > **Every refusal along the way was a bound of mine, not the
   > vocabulary.** Sixteen books were refused across two runs for exceeding
   > a ten-word limit I had guessed at, on titles entirely inside the
   > lexicon, and the teacher answered identically on every retry. The bound
   > is now 12, set from the corpus's own range of 1 to 11 words, and it is
   > stated in the prompt as well as enforced after it. **A constraint
   > enforced only by rejection is one the teacher cannot satisfy.**
5. **No spread-boundary token.** The general answer to a paragraph break is
   a blank line, and the pure-frame specification is explicit that a
   boundary renders as exactly one blank line because a double gap would
   itself be an announcement.
6. **The `<book>` seed defect is fixed as a consequence of 1 and 2**, since
   the token a sampler starts from must be one training emitted.

## First measurement, 2026-09-27

**A model can now end a work, and sometimes does.** Trained for 600 steps on
the announced corpus at width 256 over four layers, held-out loss 3.6514,
**two of six samples ended on their own within 200 tokens**. Before this
change the number was not zero, it was undefined, because no token could
express an ending.

`tools/sample_level.py` reports that count on every run. **It is a capability
check and not a quality one.** It says the model learned that works end; it
says nothing about whether what precedes the ending is worth reading.

**That run is not committed and `evals/pilot/level_1_samples.json` is now
stale.** The committed record is a longer run, 1,600 steps at temperature
0.8, and it was produced under a vocabulary of 2,246 and an untied head that
neither exist now. A 600-step probe must not replace it, so it was reverted,
and re-running it belongs with the measurements
`docs/process/HANDOFF.md` already lists as owed.

## The test this project is unusually able to run

**The missing instrument in the cited work is a training-time test**, and
this project trains a 4.3-million-parameter model on 357,000 tokens in
minutes. The three-arm design transfers directly: one corpus written with
announcements, one with the announcement text flattened, one with the
announcement deleted, everything else held fixed.

**The scale gap must be stated whenever this is reported.** The cited
readers span 0.60B to 8.19B and this model is 4.3M, which is two orders of
magnitude below the smallest of them. A null here would be weak evidence
about readers of that size, and a positive result would be a claim about
small models rather than a replication.

## Sources, fetched 2026-09-27

Vendored into ignored `tmp/references/papers/` under the rule in
`REFERENCE_SOURCES.md`, so nothing licensed is redistributed here.

| File | SHA-256 | Source |
| --- | --- | --- |
| `notation_2608.09093.pdf` | `27eaa4899edf8b84ab206f2ce0cdd7460ea52d3b832d26933c92042b753ca264` | `https://arxiv.org/abs/2608.09093` |
| `bestfit_2404.10830.pdf` | `e5db2f9c2d86bd63087265b6a0e63f535bd6f55e3a18419899e15618c42fa8aa` | `https://arxiv.org/abs/2404.10830` |
| `packing_2107.02027.pdf` | `a00e5dae804b59f5ed57a90bed1e72454acefc971d9d5b35e213d3cda35675e5` | `https://arxiv.org/abs/2107.02027` |

- Freeburg, *The Announcement Carries the Cue: Markup, Boundaries, and the
  Notation of Pre-Training Corpora*, August 2026.
- Ding and others, *Fewer Truncations Improve Language Modeling*,
  International Conference on Machine Learning 2024.
- Krell and others, *Efficient Sequence Packing without
  Cross-contamination*, 2021.
- Llama 3 special tokens and the 256 reserved slots,
  `https://github.com/meta-llama/llama3/blob/main/llama/tokenizer.py`.
