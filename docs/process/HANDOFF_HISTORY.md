# Handoff Prompt

**Refreshed 2026-09-28 at the close of a session that ran unattended, and
written for a different agent than the one that wrote it.**

**READ `AGENTS.md` FIRST IF YOU ARE NOT THE AUTHORING AGENT.** It says what a
clone has and what it does not, which is the difference between this repository
and the workshop it was built in. Four things are deliberately untracked and
one of them makes an obligation in `CLAUDE.md` undischargeable. That is flagged
for the operator, not solved.

**NO COMMIT HASH IS STAMPED HERE, deliberately.** A stamp naming the commit
that contains it is impossible and one naming the parent is off by one the
moment anything else lands. **Validate by ancestry and by content.**

## The tree is clean

**Nothing is running, nothing is uncommitted, continuous integration is green
on the pushed head.** The loop that drove this session is stopped.

## What a resuming session should do first

1. Run the validity check below and report the handoff valid or stale.
2. **Check continuous integration separately.** A green local gate is not a
   green clone, and the two have now diverged five times.
3. **Read the failure classes in `PROCESS_STRATEGY.md` before measuring
   anything.** They are the most valuable thing in this repository and three of
   them were added by failures that happened *after* being written down.
4. Read `CURRENT_BRIEF.md`, then the named work below.
5. **Wait for the human prompt.**

## Validity

**Branch**: `main`, pushed to `origin`, `github.com/sgeos/epagoge`, public.

**Ancestry cannot be checked by commit identity.** Every hash changed on
2026-09-25 when the history was rewritten twice. **Check by content**: the
first commit's `README.md` begins `# Epagoge`, and grepping every commit
message for the former name returns 0.

**Content, each read from a tool on 2026-09-28.**

1. `./tools/check.sh` reports **ALL CHECKS PASSED** over **twenty-two** checks
   and **exits 0**.
2. The suite reports **579** tests.
3. `curriculum/vocabulary.json` holds **1,036 terms**, **178** core, **37**
   ostensive. **849** distinct words admissible at level one and **954** at
   level two. **77 terms carry a source recorded at admission.**
4. **Both dictionaries are self-hosting.** Level one defines **812 of 812**
   words needing one; level two **917 of 917**. Closure 100 percent at both,
   seed 257, nothing blocked and no cycles.
5. `curriculum/books/level_1/` holds **523** books over **9,131** records. The
   word count is deliberately **not** asserted as an equality, since any later
   fill raises it. It was **330,710**, summed from the per-book figures the
   books check prints. **Check it is at least that.**
6. `tools/stamp_books.py --level 1 --check` reports **523 books, 0 missing a
   field**.
7. **Unused surface forms 395**, of 2,049 admitted, and **headwords never used
   at all is 0**.
8. **All 96 level-one schedule units carry a question-and-answer book**, every
   one at its full sixteen spreads.
9. **Concept pairs realised: 312 of 8,128**, counted as the union across a
   content book's own records with the dictionary books excluded. **Two other
   counting methods give 88 percent and 0.5 percent and both are wrong**; the
   reasons are in `../decisions/COMBINATORIAL_RICHNESS.md`.
10. `git ls-files secret | wc -l` reports **0**, and the disclosure scan
    reports it covered tracked and untracked files, line by line and with
    whitespace collapsed. **A scan that does not say all three is the old one.**
11. **`evals/pilot/level_1.pt` is not in the repository** and cannot be. It is
    trained at the reference configuration on the authoring host. A clone must
    retrain before `talk.py`, `elenchos.py` or `retention.py` will run.

## The state, and what changed in this session

**The frontier moved and the reason is one flag.**
`evals/pilot/REFERENCE_CONFIGURATION.md` is the answer to "what should I train
with". **Muon at 3.066 held-out over three seeds against 3.183 for the
defaults**, on 344,348 training tokens at 3,400 steps, which is 20.2 epochs.
**0.117 nats, more than the entire previous reference configuration bought.**

**Every unit can now show a question being answered.** 96 of 96, from 42.
Question marks went 646 to 1,381, one per 24.7 sentences from one per 49.
**They contribute zero new concept pairs**, measured, because a question book
teaches its own unit's concepts and its narrative sibling already realised
them.

**`elenchos` exists and has run.** It was an empty directory. It now has a
specification written before any probe, twenty probes validated against the
lexicon by a test, a scorer, and a first result. **The result is a floor and
the control is what shows it**: the model appears to resist pressure perfectly
until you see it does the same thing when agreed with.

**The lexicon pipeline has no hole in it.** `define_candidates.py` is the
missing step between a scan candidate and an admitted word. **954 words at
level two, so 9,046 remain.**

### Live defects and open risks

**The machine is close to its memory ceiling.** Raising the teacher's context
to 6,144 drove swap to 14.9 GB of 16.4 and free memory to 0.1 GB, which is the
exhaustion condition this host has crashed under. Reverted. **Do not raise
`NUM_CTX` without measuring.**

**The definition prompt does not scale and the fix is partial.** It listed the
whole lexicon, so it grew with the work. A 700-word defining vocabulary fixes
the ask at constant size, but **concept assignment is still per word** and is
the remaining manual step in the loop.

**Every figure in `evals/pilot/` measured before 2026-09-27 is about 0.25 nats
optimistic**, from a truncated evaluation. Comparisons survive; absolutes do
not. The affected records carry a banner.

**44 narrative books sit below the word band and nobody has looked at why.**
They are cross-concept variants at 200 to 270 words against a 320 floor. The
design permits a short book, so these are not defects, but the share is larger
than expected.

### Findings that outlive the session

**A hyperparameter with one name is not necessarily one quantity.** Three
confounds in a day: the learning rate across widths, the learning rate across
two optimisers, and the weight decay across two optimiser groups. **Only the
third was caught by anything other than hindsight**, and what caught it was the
training loss moving in a direction regularisation cannot move it.

**Both defaults were already optimal, which nobody could have known.** AdamW's
3e-4 and Muon's 0.02 both sit at bracketed optima. **The caveat that the
comparison was untuned was correct to raise and resolved the opposite way**,
and it is struck through rather than deleted so a reader sees the question was
asked.

**The scaling law reproduced here.** Optimal rate halves as width doubles:
measured exactly 2 from 256 to 512, and 3 from 512 to 1,024. Right in
direction, not exact at the top end, on a three-point curve at one seed.

**Two improvements did not add, for the third time.** Muon and
warmup-stable-decay together are 0.080 worse than Muon alone, and the training
loss shows why: each alone fits harder, together the model underfits.

**A filtered view is not a sample.** A rule was written from a grep that could
only return the shape it appeared to discover, and it rejected every definition
in the next run.

**A recorded property is not a guard.** Three failures this session recurred
*after* being documented, and in each case only a change that made the failure
impossible held. **The test is whether the next person can still fail the same
way.**

## Named work, in the operator's priority order

1. **The level-two lexicon.** 954 words against about ten thousand. The
   pipeline is built and the remaining manual step is concept assignment. **The
   words the teacher reached for and could not have are the cheapest next
   batch**: `honey`, `fruit`, `flour`, `clothing`, `beans`, `petals`, `yeast`,
   `nut`, `roasted`, `rows`.
2. **Schedules for levels three to seven.** None exist. Targets are calibrated.
3. **More `elenchos` probes.** Twenty cannot resolve an effect at the threshold
   the specification fixed, because the per-probe spread is 0.0909 against a
   threshold of 0.05.
4. **The 44 out-of-band narrative books**, to decide whether they are short by
   design.

## What is YOURS: decisions the operator holds

1. **Whether an agent without `secret/` may write tracked prose.** `CLAUDE.md`
   requires reading the code-name discipline first and it is not in the clone,
   and the scan that would catch a mistake skips for the same reason. **New
   with this handoff.**
2. **The Dale-Chall and New General Service List licensing question**, which
   keeps step one of the sourcing pipeline shut.
3. **`sources/` and level seven.** The acquisition scheme is drafted in
   `../decisions/SOURCE_ACQUISITION.md` and **deliberately not adopted**.
4. **Whether terminal-stage records carry a distinct licensing status**, open
   question twenty-five.
5. **The endpoint and estimator, pre-registration item 10**, now a precision
   decision rather than a sign decision.
6. **Whether the ablation's third arm is enough.**

## What is NOT yours

**Announcing.** The repository is public; discovery is not. A launch post
reopens the decision without a file changing.

## Governing rules that are easy to lose

- **Run the gate alone, read the exit code, stop, then commit.** Chaining them
  in one command pushed a failing tree once.
- **Check continuous integration separately.** Five divergences. The general
  form is that a check consulting the filesystem or git history passes on state
  the runner does not have.
- **A history-derived check cannot pass in the commit that changes what it
  derives from.** `word_provenance.py` now refuses rather than relying on
  anyone remembering this.
- **Read counts from the tool.** Six instances of arithmetic in a record.
- **Do not pipe a run through a filter and read the exit code.**
- **`--out` is required on every measurement tool.** Three defaulted to a
  tracked path and one was overwritten twice.
- **Before reporting a difference, say what was held fixed and check that it
  was.**
- **Corrections are kept in place**, beside the claim, not amended away.
- **Do not weaken a check to make something pass.**
- **`git-filter-repo --replace-text` has no comment syntax.** A commented file
  corrupted every file in history once. Take a mirror clone first.
- **The ruleset on `main` binds the owner too.**
- Irreversible or outward-facing actions need confirmation, and a prior
  authorisation does not extend to the next one.

---

## Superseded 2026-09-28, the block written at the close of the previous session


**Refreshed 2026-09-27 at the close of a twenty-five commit session.**

**The single most important line in this file.**
`tools/diagnose_level.py` scored 24 of 48 held-out batches for most of that
session and announced it on every run. **Every figure it produced before
this refresh is about 0.25 nats optimistic.** Comparisons survive, because
the truncation was identical everywhere; absolute losses do not. Four
evaluation records carry a banner saying which is which.

**NO COMMIT HASH IS STAMPED HERE, deliberately.** A stamp naming the commit
that contains it is impossible and one naming the parent is off by one the
moment anything else lands. Every hash in this repository changed once
already. **Validate by ancestry and by content**, which the next section
gives in a form that does not depend on any hash.

## The tree is clean

**Nothing is running, nothing is uncommitted, CI is green.**

**At this refresh**: 469 books over 8,267 records and **315,444 words**,
every content book inside the word band and every book carrying its six
metadata fields. **Concept pairs realised: 312 of 8,128**, and only one
concept is held by a single book.

**The corpus can now show a question being answered.** 42 of 96 schedule
units carry a question-and-answer book, against 17 before, and the corpus
holds one question mark per 49 sentences against one per 103. **54 units
still have none**, which is the next obvious batch.

**Pair coverage can be counted three ways and two are wrong.** Counting
every concept any record mentions gives 88 percent, because the dictionary
books form one clique. Counting only what a book's schedule unit teaches
gives 0.5 percent, because a cross-concept book's partner is not in the
schedule. **The union across a content book's own records, dictionary books
excluded, is the figure this file means.**

**The measurement debt this file has carried since 2026-09-26 is paid.**
All three owed measurements were re-run on the current tree and the
conclusions of two of them changed. Every evaluation record that still
holds a figure taken before the current corpus now says so at its top.

## What a resuming session should do first

1. Run the validity check below and report the handoff valid or stale.
2. **Check CI separately.** A green local gate is not a green remote one,
   and the two have diverged three times.
3. Read `CURRENT_BRIEF.md`, then the named work queue further down.
4. **Read the failure classes in `PROCESS_STRATEGY.md` before measuring
   anything.** Six defects were found in one session, three of them in
   reasoning rather than in code, and every one is of a recurring kind.
5. **Wait for the human prompt.**

## Validity

**Branch**: `main`, pushed to `origin`, `github.com/sgeos/epagoge`, public.
**CI is green and must be checked, not assumed.** It was red on an earlier
head while the local gate passed, because one check is derived from git
history and the runner clones one commit.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint.

**Ancestry cannot be checked by commit identity.** Every hash changed on
2026-09-25 when the history was rewritten twice. **Check by content**: the
first commit's `README.md` begins `# Epagoge`, and grepping every commit
message for the former name returns 0.

**Content, each verified 2026-09-27.**

1. `./tools/check.sh` reports **ALL CHECKS PASSED** over **twenty-two**
   checks and **exits 0**.
2. The suite reports **537** tests.
3. `curriculum/vocabulary.json` holds **970 senses over 936 words**, of
   which **849** are admissible at level one. **178** core, **37**
   ostensive, a seed of **257**. **The tokeniser is larger than the
   lexicon**: **2,279** ids, because 22 of them are special or structural.
4. **Both dictionaries are self-hosting**, 812 of 812 at level one, closure
   100 percent, grounded 833, nothing blocked and no cycles.
5. `curriculum/books/level_1/` holds **469** books over **8,267** records,
   467 of them content books. The word count is deliberately **not**
   asserted as an equality, since any later fill raises it. It was
   **315,444**; check it is **at least** that, that all content books are
   in the band and none above.
6. `tools/stamp_books.py --level 1 --check` reports **469 books, 0 missing a
   field** and no date disagreeing with history.
7. **Unused surface forms 405**, and **headwords never used at all is 0**.
   Level-one vocabulary utilisation is **829 of 849**.
8. **`evals/pilot/level_1.pt` loads and is trained at the reference
   configuration** in `../../evals/pilot/REFERENCE_CONFIGURATION.md`, not at
   the defaults. `tools/talk.py`, `tools/retention.py` and
   `tools/plan_pairs.py` all run against it.
9. **Concept pairs realised: 312 of 8,128**, counted as the union across a
   content book's own records with the dictionary books excluded. **Two
   other counting methods give 88 percent and 0.5 percent and both are
   wrong**; the reasons are in `../decisions/COMBINATORIAL_RICHNESS.md`.
10. **42 of 96 schedule units carry a question-and-answer book**, and the
    corpus holds **646 question marks in 378,156 training tokens**, one per
    49 sentences.
11. `git ls-files secret | wc -l` reports **0**, and the disclosure scan
   reports it covered tracked and untracked files, line by line and with
   whitespace collapsed. **A scan that does not say all three is the old
   one, which missed both.**

## Corrections to the refresh above, kept in place

**Four numbers in the block above were carried forward without being
re-run, and are corrected rather than quietly fixed.** The previous refresh
asserted 960 senses over 928 words with 841 at level one, and closure at 807
of 807. The tree reports 961 over 927 with 840, and 803 of 803. The books
check corroborates 840 independently, reporting level-one utilisation as 820
of 840. **A refresh that restates a number must re-run it.**

**A pushed commit message claimed 533 tests where the tree has 526.**
`5bf8c2b`. The count was written from arithmetic rather than from the gate.
Corrected here rather than amended, because the commit is pushed.

## The three owed measurements are paid, and two changed their answer

**Re-run 2026-09-27 on the current tree**, with both position paths sharing
one `Block`, heads derived, and the corrected token-weighted evaluation.

1. **The position comparison.** Rotary still wins and the figure moved, to
   **0.292 nats at 128 and 0.547 at 1,088** over three seeds a cell. **The
   earlier claim that sequence length and position scheme were independent
   is withdrawn.** The rotary advantage nearly doubles with window length,
   and most of what looked like a penalty for making a book one sequence was
   the position table starving: 128 beats 1,088 by 0.326 nats with a learned
   table and by **0.071** with rotary.
2. **The held-out figures.** Every eval record that still carries a figure
   from before the corrected evaluation is marked stale at its top.
   `LEVEL_ONE_VARIANCE.md` is the one that matters beyond labelling, because
   `evals/PRE_REGISTRATION.md` item 6 depends on its numbers.
3. **The capacity sweep.** **Width 1,024 is not the best width and the old
   ranking is withdrawn.** With heads derived it is worse than 512 and 256
   at every duration. Best measured is **3.037 at width 256 and 3,200
   steps**. Undertraining was the obvious explanation and was tested and
   ruled out.

**A fourth thing was found while paying them.** At 6,400 steps every width
collapses, width 512 reaching a training loss of 0.501 against held-out
4.130. Token replacement at 0.15 turns that into **2.913**, which is 1.217
nats and the best result at that width.

## Superseded: the owed-measurement block, kept for its reasoning

**Every one was invalidated by a defect found in auditing, not by a new
result.** Anything quoting the old figures is quoting a confounded number.

1. **The rotary comparison.** "Rotary is worth 0.4 nats" was confounded: the
   learned path used `nn.TransformerEncoderLayer` and the rotary path a
   hand-written block, **thirteen bias tensors against nine**. Both now share
   one `Block` so position is the only difference. Re-run the 128 against
   1,088 grid.
2. **Every held-out figure this project has ever reported.** The evaluation
   took the first `eval_batches` = 24 batches in index order, which at 267
   held-out chunks is **24 of 33, a systematic slice of the curriculum
   tail**. And it averaged per-batch means, which is the wrong average when
   batches hold different numbers of real tokens, and padding is 6.8 percent
   of slots at 128 tokens and **25.6 at 1,088** — so the error grew with
   sequence length and fell hardest on the arm being compared. Both fixed;
   it now sums and divides once by the token count and announces partial
   coverage.
3. **The wide points of the capacity sweep.** `n_heads` was fixed at four at
   every width, so width 1,024 ran at **head_dim 256** where 64 to 128 is
   standard. Now derived at one head per 64 channels.

**One suspicion was tested and cleared.** Attention does not see padding:
padding is a suffix and attention is causal, verified empirically in both
paths rather than argued.

## The state

| Goal | State |
| --- | --- |
| Level-one lexicon | **Done.** 841 words, closure 100 percent, seed 257 |
| Level-one corpus length | **Done at `c1b2ba2`**, 244 of 244 in band |
| Level-one book metadata | **Done for committed books**, pending for new ones |
| Combinatorial richness | **262 pairs of 7,626**, from 109. More is the lever |
| Architecture | **Enhanced, unmeasured.** Tying, init, heads, rotary |
| Ordering ablation | **Blocked** on an endpoint the operator holds |

### Live defects

**The corpus realises 262 concept pairs of 7,626.** Better than the 109 it
started at and still three percent. `COMBINATORIAL_RICHNESS.md` has the rule
and `tools/plan_pairs.py` plans any number more. **Exhaustive singles and
pairs is 7,750 books and 7.25M tokens, inside the stated budget**, so this is
a scheduling question rather than a feasibility one.

**The model is worst at the concepts the project exists to teach.**
`giving_a_reason`, `disagreeing` and `agreeing` at loss 4.011 against 2.017
for `emptiness`. The epistemic relations are the point and they are at the
bottom.

**`coverage.py` is undiscriminating.** It flags 116 of 124 concepts as taught
once and never revisited, which is 94 percent, so it ranks nothing. Its
value is as an inventory; `tools/retention.py` says which to write for
first.

**Unused surface forms should be re-counted**; the figure of 529 of 2,038
predates 153 new books. `docs/decisions/UNUSED_FORMS.md` judged every one
and left fourteen
sense questions to the operator.

### Added 2026-09-27, after the checkpoint and structural-token work

- **A serialised record must say what it does not carry.**
  `../decisions/FIELD_ENUMERATION.md`. `save_checkpoint` wrote five of
  `ModelConfig`'s ten fields, so a reload rebuilt the other five from
  today's defaults. Two of those five fail loudly and three silently, and
  `n_heads` is the worst: written at two and read as four, every tensor fits
  and attention is split differently than it was trained to.
- **A work now has a beginning and an end.**
  `../decisions/STRUCTURAL_TOKENS.md`. `<book>` occurred zero times in
  356,975 training tokens while being the seed of every unprompted sample.
  `<eot>` is new, sixteen reserved slots are held, and two of six samples
  ended on their own after 600 steps.
- **The announcement is the cue and the notation is not.** Measured
  elsewhere over five readers from 0.6B to 8.2B: deleting a structural
  announcement makes the following prose harder to predict, and swapping
  Markdown for a bare line moves a measured zero. **No training-time
  evidence exists**, and this project can produce it cheaply.
- **The vocabulary grew by 21 ids, so every checkpoint on disk is now
  refused**, cleanly, by the machinery landed the same day.
- **`evals/pilot/level_1_samples.json` is stale**, produced under a
  vocabulary of 2,246 and an untied head, neither of which exists.
- **47 of 399 book titles hold a concept identifier rather than lexicon
  words**, which blocks announcing titles and is a fourth instance of the
  rule that a concept name is not a word.

### Added 2026-09-27, the ablation's own instrument

- **The ordering arms were measuring gradient noise as much as ordering.**
  `pilot._batches` takes consecutive positions from an arm's order, so an
  arm sets both the visit sequence and what each batch holds. A curriculum
  order averages **1.562** distinct subjects a batch against **2.975**
  shuffled, over 160 batches. **Corrected from 1.20 and 1.88**, which came
  from a proxy for a book's chunk count; the proportions held.
- **The pre-registered contrast measures batch composition and nothing
  else.** Over six control block sizes the curriculum arm's loss is linear
  in homogeneity at r = -0.984, and the topological arm sits on that line
  within one to two seed standard deviations. Item 3 names exactly that
  pair.
- **The flat arm is the only one carrying signal.** `shuffled` sits five to
  seven seed standard deviations below the line.
- **An ordering property tracks held-out loss after controls.** At matched
  batch diversity the graph-respecting arm loses by 0.0255 nats in **42 of
  42** paired runs. Displacement is eliminated, padding is 6.45 percent
  everywhere, and the most generous diversity metric leaves 77 percent
  unexplained.
- **Length ordering was the rival explanation and it is eliminated.** An
  arm matched to the graph-respecting arm on length, +0.213 against +0.211,
  and to the graph-ignoring arm on diversity, behaves like the latter: 0.025
  nats below topological in 6 of 6 seeds, and 0.004 above shuffled. It sits
  15 percent of the way across the gap.
- **What survives may be one thing described two ways.** Every arm
  respecting the graph sits 0 to 49 from the curriculum order and every arm
  ignoring it sits above 118, and two random linear extensions are 57.9
  apart, so the valid set is a region about 50 wide. **Respecting the graph
  and staying near a valid order cannot be separated**, and the arms on the
  homogeneity curve are exactly the ones inside the set.
- **This is the fifth defect and the first in the reasoning rather than the
  code.** It came from concluding by elimination without asking what had not
  been eliminated.
- **Three controls exist now and none is on by default.**
  `--block-shuffle N` shuffles books inside blocks of N, holding the
  sequence and discarding batch homogeneity. `--arms` selects which arms
  run, and `length` is an arm carrying the length gradient without the
  graph. `--eval-batches 0` scores the whole held-out set, where the default
  24 was scoring 86 percent of it. **An ablation should use the first and
  the last; the default comparison is deliberately unchanged, because
  changing it is the operator's.**
- **The binding constraint is no longer measurement.** The surviving effect
  is 0.7 percent of the loss and **item 7 fixes whether that counts**.
  Narrowing the attribution further cannot make meaningful an effect nobody
  has called meaningful.
- **The reference configuration is recorded** in
  `../../evals/pilot/REFERENCE_CONFIGURATION.md`, and the shipped
  checkpoint is trained at it: rotary, width 512, 3,200 steps, token
  replacement 0.05. **Frontier 3.156 against 3.236 for the defaults**, three
  seeds, whole held-out set.
- **Capacity pays only if it is regularised.** Unregularised, width 512 is
  slightly worse than 256; regularised it is clearly better. That
  interaction is why earlier width sweeps made the wide points look bad.
- **`diagnose_level.py` scored 24 of 48 held-out batches** until today, so
  **every figure it produced is about 0.25 nats optimistic**, including four
  records written the same day. Comparisons survive because the truncation
  was identical; absolute losses do not. Both tools now take the whole set.
- **Corpus doubling is worth about 0.26 nats and the rate is not falling**,
  measured over an eightfold range against one held-out set. At thirty books
  a round that is fifteen rounds per doubling, which makes it **the most
  expensive lever measured this week**: token replacement was worth 1.217
  nats at the collapse point and rotary 0.292.
- **The optimum is twenty epochs at every corpus size**, to within a tenth,
  so the best step count doubles with the corpus. **Anything sweeping corpus
  size must sweep steps with it**, or it measures the interaction.
- **The corpus-size subsample was a curriculum prefix and is now a sample.**
  The prefix overstated the last doubling by two thirds.
- **Controlled, about sixty percent of the effect disappears.** Shuffling
  books inside blocks of 32 keeps every book within 10 percent of its
  curriculum position and removes 87 percent of the homogeneity gap. The
  curriculum-minus-shuffled gap falls from +0.115 to +0.044 at 800 steps and
  +0.117 to +0.049 at 1,600, six seeds each, while the two already
  heterogeneous arms move by at most 0.008.
- **So every ordering figure from this harness overstates by about two and a
  half times**, including "the endpoint picks the sign", which was measured
  uncontrolled. `--block-shuffle` is the control and an ablation must use it.
- **It was also a noise source.** Seed standard deviation halves under the
  control at 1,600 steps and the pairing correlation recovers from zero.
- **Pairing no longer pays.** Variance fell elevenfold as the corpus grew
  eightfold, so a 1 percent effect needs one seed rather than twelve paired
  or 246 unpaired.

### Findings that outlive the session

- **A full pairwise corpus is affordable and I was wrong to say otherwise.**
  124 singles is 116k tokens; 7,626 pairs, one pair a book, is 7.1M. Both
  tiers together are **7.25M tokens, inside the stated 1M to 10M budget**.
  Triples are 310,124 and cost 5.2M tokens at eight concepts a book. **The
  binding constraint is teacher-hours, not corpus size**: about twelve days
  for singles and pairs.
- **The literature splits the thesis in two.**
  `docs/decisions/CURRICULUM_LITERATURE.md` has it. Corpus quality is well
  supported; ordering by content difficulty is contradicted three times,
  including by Rohde and Plaut in 1999. What does work is sequence-length
  curricula and **model-measured** revisiting.
- **A guard that has not been shown able to fail is not a guard.** Every
  check added this session was shown failing against a broken input first.
- **The teacher's context was inherited, not chosen.** It served 32,768
  tokens for prompts of 1,260, which held 21 GB on a 32 GB machine and made
  a six-second call take over 300. `generate.ask` now declares `num_ctx` and
  caps `num_predict`, because **a bounded failure beats an unbounded wait**.
- **A concept name is not a word.** Putting `emptiness` in a prompt cost a
  book: the teacher echoed it, it is not in the lexicon, and every subject
  line was rejected despite twenty-three usable spreads.

## Named work, in the operator's priority order

1. **The level-two lexicon**, 879 words against about 10,000 at a fourth
   grade target. `../decisions/LEXICON_SOURCING.md` has the pipeline: seed
   from lists, scan public-domain and CC0 sources, accept the frequent in
   bulk, inspect the per-source long tail, record provenance at admission.
   **A complete draft precedes level-two corpus drafting**, by standing
   direction.
2. **Question-and-answer books for the 54 units without one.** 42 of 96
   have one, and the form is what lets a model answer rather than continue.
3. **Implement what `TRAINING_TECHNIQUES.md` adopts**: maximal update
   parametrization, Muon, warmup-stable-decay. Under the 2026-09-27
   direction these are outstanding work rather than experiments to justify
   one at a time.
4. **Schedules for levels three to seven**, against targets already fixed
   in `../decisions/LEVEL_CALIBRATION.md`. Research and design work.

## What is YOURS: decisions the operator holds

1. **The endpoint and estimator, pre-registration item 10.** **The reason
   given here was that the endpoint fixes the sign, at 800 steps the
   curriculum arm worse in 8 of 8 and at 1,600 better in 7 of 8. That
   reason no longer holds and the item still does.** Those runs were
   uncontrolled for batch composition, which overstates an arm difference by
   about two and a half times, and on the current corpus the sign does not
   flip: the curriculum arm is worse at both endpoints. What the endpoint
   still decides is the paired standard deviation, 0.0074 at 800 steps
   against 0.0103 at 1,600, and therefore the seed count. **Item 10 is now a
   precision decision rather than a sign decision.**
2. **Whether the ablation's third arm is enough.** `shuffled` now ignores
   the graph. Wu, Dyer and Neyshabur ask for a growing-set control; in a
   trainer that cycles a fixed order the growth phase is the first eleven
   percent, so the shuffled arm is chiefly a flat baseline.
3. **The level-two lexicon, 879 words against about 10,000.** A complete
   draft lexicon precedes corpus drafting, by operator direction.
4. **Schedules for levels three to seven.** None exist.
5. **`sources/` and level seven.** Empty, licensing unexamined. **Wikipedia
   for module seeding is recorded as open**: it is CC BY-SA and prose derived
   from it may be a derivative work.
6. **Fourteen sense questions** in `UNUSED_FORMS.md`.
7. **Whether to clear 219 GB of Rust build output under ~/projects.** The
volume was
   at 96 percent and swap exhaustion is the likeliest cause of this
   machine's crashes. Steam and three games were removed on instruction,
   taking free space from 41 to 172 GiB; saves are in
   `~/steam-saves-2026-09-26`.

**Items 5, 6 and 7 were answered on 2026-09-27 and the entries above are
left standing rather than edited away.** What changed:

- **Item 5 has a speculative position and a real one.** The metadata-only
  acquisition scheme is drafted in `../decisions/SOURCE_ACQUISITION.md` in
  enough detail to adopt and is **deliberately not adopted**. The standing
  position is deferral until the first acquisition, `sources/` stays
  tracked, and `sources/bodies/` is ignored as a guard so a body cannot be
  committed by accident before the decision. The Wikipedia question is
  untouched.
- **Item 6 is resolved and its count was stale.** Two of the fourteen,
  `drunk` and `lighted`, had already been decided in `08f5013` and the
  record was never updated, so this file carried fourteen for a day where
  twelve was right. Four forms are culled through the `mass` qualifier and
  seven kept. The rule is that an archaic form need not be admitted while a
  current one is kept even when unused.
- **Item 7 is done and its figure did not reproduce.** The 219 GB above
  measures nothing that exists. Measured on 2026-09-27 there were **120.3
  GiB** across 91 `target` directories. **75.1 GiB was reclaimed** from 66
  of them, Keleusma and 1830 excluded on instruction, along with 2.16 GiB of
  unpinned Rust toolchains and 1.62 GiB of caches belonging to applications
  that were not running. The volume moved from 75 percent with 229 GiB free
  to **66 percent with 305 GiB free**.
- **Rust 1.92 must not be uninstalled.** Thirteen toolchain pin files name
  it, every one of them inside a Keleusma tree, and removing it as an old
  version would have broken the project that was explicitly excluded. Three
  further pins name 1.89.0, one names 1.77 and one names a 2024 nightly.
- **`~/Library/Caches/Mozilla.sccache` holds 10 GiB and was deliberately
  kept.** It is the compiler cache that makes the 75 GiB of deleted build
  output cheap to rebuild, so clearing both would have been the worst
  available combination.

## What is NOT yours

**Announcing.** The repository is public; discovery is not. A launch post
reopens the decision without a file changing.

## Governing rules that are easy to lose

- **Run the gate, read the exit code, stop, then commit.**
- **Check CI separately.** Red while the local gate was green three times,
  most recently because `stamp_books --check` skips files modified in the
  working tree, which is exactly the set whose dates the pending commit is
  about to change.
- **A tool that returns less than it was asked for must say so.**
- **Before reporting a difference, say what was held fixed and check that it
  was.** Five instances this session: a loss compared across held-out sets, a
  sample compared across seeds, a metric compared across temperatures, a
  latency measured once and trusted as a constant, and an architecture
  comparison confounded by bias asymmetry.
- **A metric compared at a fixed temperature measures sharpness, not
  quality.** Distinct-token share and attractor frequency both reverse with
  temperature.
- **Corrections are kept in place**, beside the claim, not amended away.
- **Do not weaken a check to make something pass.**
- **`git-filter-repo --replace-text` has no comment syntax.** A commented
  file corrupted every file in history once. Take a mirror clone first.
- **A workflow that triggers on push must not group concurrency by ref**, or
  a second push cancels the first commit's verdict.
- **The ruleset on `main` binds the owner too.** Another history rewrite
  means disabling it in settings first.
- Irreversible or outward-facing actions need confirmation, and a prior
  authorisation does not extend to the next one.

---


## EVERYTHING BELOW THIS LINE IS ACCUMULATED HISTORY

### Superseded 2026-09-25, end of session three

Replaced rather than deleted. It described 171 books and a corpus of
39,900 tokens, and said the live defect was size. The defect was size
and also length, form and lexicon utilisation, none of which it saw.

## Validity

**Branch**: `main`, pushed to `origin`, `github.com/sgeos/epagoge`,
private. **CI is green** and must be checked, not assumed.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint.

**Validate by ANCESTRY and by CONTENT, never by a hash match.**

**Run the gate, read its exit code, then stop before committing.**

**Ancestry**: `main` should contain **`c0cf2c4`**, which completed the
level-one corpus. If it does not, this file predates a reset.

**Content** — each verified on 2026-09-25.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across **fifteen**
   checks and **exits 0**. The books check now enforces `--spreads 16`.
2. The suite reports **455** tests.
3. `curriculum/vocabulary.json` holds **958 senses over 925 words**, of
   which **842** are at level one. **177** core, **37** ostensive, a seed
   of **255**, and **84** substitutions.
4. **Both dictionaries are complete and self-hosting**, 805 of 805 at
   level one, closure 100 percent, nothing blocked and no cycles.
5. `curriculum/thesaurus.json` holds **922** entries, 195 with an antonym
   and 132 with a synonym.
6. `curriculum/books/level_1/` holds **171** books over **39,900**
   tokens.
   **Every schedule unit has a book and every book is at sixteen
   spreads.** Many units hold two, some three.
7. `evals/pilot/level_1.json` records eight paired seeds over the whole
   corpus, and `evals/pilot/LEVEL_ONE_VARIANCE.md` says what it does and
   does not settle.
8. `git ls-files secret | wc -l` reports **0**, and history is clean.

## What a resuming session should do first

1. Run the validity check and report the handoff valid or stale.
2. **Check CI.** A green local gate does not mean a green remote one.
3. Read `docs/process/CURRENT_BRIEF.md`.
4. Read **`evals/pilot/LEVEL_ONE_VARIANCE.md` before quoting any number
   from `level_1.json`.**
5. **Wait for the human prompt.**

## The state

**Reference material and the level-one corpus are done. The corpus is not
big enough to run an experiment on.**

| Goal | State |
| --- | --- |
| Level-one dictionary and closure | **Done.** 805 of 805 |
| Thesaurus | **Done.** 922 entries |
| Missing words | **Done, and continuous** via `tools/admit.py` |
| Level-one corpus | **Done.** 92 of 92 units, every book at 16 spreads |
| Train a level-one model | **Done.** The result decides nothing, by design |
| Level-two dictionary and thesaurus | **Done** |
| Level-two ablation | **Blocked on corpus scale and on item 10** |

### The live defect is size

**39,900 tokens against a level-one budget of 10^6 to 10^7**, a factor of
25 to 250 short. `CORPUS_SCALE.md` asks for twelve to six hundred books
per topic and the corpus holds one or two. **800 steps at batch eight
over 345 chunks is about eighteen passes**, so repetition still dominates
and an ordering signal has eighteen chances to wash out.

`generate_books.py --variants N` writes an Nth book per unit. That is
ordinary generation work and needs no decision from anyone.

## Findings that outlive the session

- **The endpoint picks the sign.** Same corpus, same arms, same seeds:
  at 800 steps the curriculum arm is worse in 8 seeds of 8, paired t
  +8.35; at 1,600 it is better in 7 of 8, t -3.17. **Both would pass a
  naive paired test.** Pre-registration item 10 is load-bearing, not
  bureaucratic, and anyone reporting an ordering effect from this
  repository must say what endpoint produced it.
- **The pilot transfers.** rho 0.9574 on real text against 0.9539
  synthetic, pairing gain 22.8x against 20.7x.
- **Two harness defects were silent.** The chunker discarded three
  quarters of the corpus by dropping every book's tail, and the ordering
  covered 13 books of 146 because a cycle made `linear_extension` return
  early without saying so. **A tool that returns less than it was asked
  for must say so.**
- **A word a book defines is not a concept the book teaches.** Conflating
  them manufactured 24 cycles between unrelated books.
- **The generation-time check was weaker than the tokeniser** and let
  eleven forms into books that the lexicon did not carry. `unlicensed` is
  exact by default now.
- **Where an inflected form is also a word, the word carries it and the
  base stops listing it.** `clear`/`clearing`, `think`/`thought`,
  `live`/`life`/`living`.
- **Four inflected forms were filed as headwords**: `depends`,
  `reporting`, `settles`, `allowed`. Each blocked every form but the one
  filed. An audit finds roughly fifteen more, mostly above level two.
- **Nothing compares a derived form against English.** The doubling check
  closes one narrow class. `admit`, `spend`, `quit`, `hang`, `swing`,
  `bend` and `spread` each needed a hand-written entry.
- **Adjectives had no comparative mechanism until 2026-09-25.** A verb
  took every inflection and a noun its plural, both enforced, while
  `kinder` was hand-listed. `adjective` is now a part of speech, 58
  level-one adjectives are declared, and `missing-comparison` gates them.
  It is declared rather than inferred, because `dead` does not grade and
  `beautiful` compares with more and most.
- **`substitutions` is half of triage** and was unused for two sessions.
  It now carries the contractions, the register drift, and `color` for
  `colour`.
- **A generated book can break closure**, because a definition in a book
  is canonical where the dictionary has none.
- **The teacher leaks prompt vocabulary** into its answers: `sequence`,
  `referring`, `reflexive`, `verb`. Not fixed.

## What is YOURS: decisions the operator holds

1. **The endpoint and estimator, item 10.** Now the highest-value
   decision in the repository, because it fixes the sign of any ordering
   result.
2. **The minimum meaningful effect, item 7**, justified from the
   literature rather than chosen for affordability.
3. **The `m1.compare` cycle resolution.** I moved `correspondence` into
   `m1.compare`. Moving `more_and_fewer` into `m1.count` also works, and
   a third unit for `same_and_different` alone is the most faithful and
   takes the level to 93 units.
4. **Levels three to seven of the schedule.**
5. **Concept complexity per level.** Level one now measures depth 8 and
   the graph reaches 10. The number moved because concepts were added,
   which is evidence the metric tracks the graph rather than the level.
6. **Whether level one can reach level two.**
7. **Whether a mature version behaves distinctly enough.** `evals/` still
   has nothing measuring **unrequested action**.
8. **Whether a definition needs its own claim class.**
9. **Whether multi-head latent attention is admissible.**

## What is NOT yours

**Publishing.** The repository is private and audited clean. Discovery
scales with attention, so a launch post reopens the decision without a
file changing.

## Governing rules that are easy to lose

- **Run the gate, read the exit code, stop, then commit.**
- **Check CI separately.** The local gate is not the gate.
- **A tool that returns less than it was asked for must say so.** Two
  silent truncations cost a session's worth of measurement.
- **Read the output, not only the counts.**
- **Verify a new check by making it fail.**
- **Check a tool's remove path apart from its add path.**
- **Corrections are kept in place, not deleted.** A wrong claim in a
  pushed commit message is corrected in the next one, not amended away.
- **A heuristic needs two pieces of evidence.**
- **No magic numbers in tests.** Tie an assertion to the lexicon.
- **Never `git checkout` to undo without checking what else is
  uncommitted.**
- **Elegance is not evidence.**
- Irreversible or outward-facing actions need confirmation.


### Superseded 2026-09-25, end of session two

Replaced rather than deleted. It described a corpus of 49 books with
12 short of the standard and 43 units that could not be authored at
all, and every one of those numbers moved within a day.

## Validity

**Branch**: `main`, pushed to `origin`, `github.com/sgeos/epagoge`,
private. **CI is green** and must be checked, not assumed. It was red for
an entire session because the local gate and the remote gate did not test
the same thing.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint.

**Validate by ANCESTRY and by CONTENT, never by a hash match.**

**Run the gate, read its exit code, then stop before committing.** A
commit landed on a red gate three times in session 2, every time because
the gate and the commit were chained in one invocation. Reading the exit
code is not the control. Not issuing the commit is the control.

**Ancestry**: `main` should contain **`ebcc1d9`**, which completed the
level-one dictionary. If it does not, this file predates a reset.

**Content** — each verified on 2026-09-25.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across **fifteen**
   checks and **exits 0**.
2. The suite reports **439** tests.
3. `curriculum/vocabulary.json` holds **836 senses over 827 words**, of
   which **738** are at level one. **174** core, **37** ostensive, a seed
   of **252**. **232** nouns and **231** verbs carry a part of speech, and
   every one carries its plural or its inflections, enforced.
4. **Both dictionaries are complete and self-hosting.** Level one reports
   **701 of 701** words defined at **100 percent closure**; level two
   **735 of 735**. Nothing on the frontier, nothing blocked, no cycles.
5. `curriculum/thesaurus.json` holds **799** entries covering every sense
   at both levels, **194** with an antonym and **132** with a synonym.
6. `curriculum/books/level_1/` holds **49** books, **47** of them content.
   **35 are at the sixteen-spread standard** and 12 are short.
7. `tools/train_level.py` runs on `mps` and writes `evals/pilot/`. **The
   corpus-to-model loop is closed.**
8. `git ls-files secret | wc -l` reports **0**, and history is clean, not
   only `HEAD`.

## What a resuming session should do first

1. Run the validity check and report the handoff valid or stale.
2. **Check CI.** A green local gate does not mean a green remote one.
3. Read `docs/process/CURRENT_BRIEF.md`, which carries the goals, their
   real blockers, and every wrong turn already made once.
4. Read `docs/decisions/LEVEL_CALIBRATION.md`, which fixes what each level
   is for.
5. **Wait for the human prompt.**

## The state

**Reference material is done. The corpus is not.**

| Goal | State |
| --- | --- |
| Level-one dictionary and closure | **Done.** 701 of 701 |
| Thesaurus, synonyms and antonyms | **Done.** 799 entries, both levels |
| Missing words | **Done, and continuous** via `tools/admit.py` |
| **Level-one corpus** | **35 of 47 books at standard. See below** |
| Train a level-one model | Pipeline closed; blocked on the corpus |
| Level-two dictionary and thesaurus | **Done.** 735 of 735 |
| Level-two ablation | Blocked on the corpus and on training |

### The live defect, and it is smaller than it looks

**Only 49 of the 92 level-one units can have a book at all.** The other 43
carry only `introduces`, naming a concept the graph does not hold, so the
generator cannot derive its neighbours and skips them. **46 of the 49 have
books.**

Covering the rest means **authoring 51 graph concepts** with prerequisite
edges and domain assignments. That is design work and it is the operator's.
Saying "48 of 92" implied a generation shortfall. It is a graph question.

**Three teachable units are still withheld**, and **12 books are short of
sixteen spreads**, needing 23 in total. **`check.sh` does not yet pass
`--spreads`**, and must once the corpus complies. A check that is wired
and never run is a failure this project has recorded three times.

## Findings that outlive the session

- **The corpus validator is more permissive than the lexicon**, since it
  accepts a word by stripping suffixes. Exact tokenisation is the stronger
  check and found a real missing form four times.
- **Seven nonsense words were admissible vocabulary for several commits.**
  `rised`, `choosed`, `costed`, `shined`, `shrinked`, `slided`, `winned`,
  each from the regular past rule applied to an irregular verb absent from
  the table. **No check compares a derived form against English.**
- **A word the teacher reached for is evidence, not an error.** Over twenty
  words entered through `admit.py` from what generation was blocked by.
- **Check a tool's remove path separately from its add path.** Two tools
  were quietly destructive in a way their add path concealed. The
  dictionary generator replaced instead of accumulating, and
  `sync_thesaurus` deleted every level-two entry when run at level one.
- **A commit message asserting a property the tree lacks is worse than the
  missing property.** Said twice, of incremental writes and of an
  assumption I had not recorded.
- **Read closure, not acceptance.** Two interventions raised acceptance and
  moved closure not at all.
- **Generation crossed over for definitions and not for stories.**
  Definition acceptance fell 22.6, 16.4, then 6.0 percent while authoring
  yielded about a hundred a round. Story acceptance runs near 50 percent.
- **The bootstrap needed a seed written in something else.** A dictionary
  restricted to function words accepted nothing in twenty-four attempts.
  **37 ostensive words**, unchanged for many rounds, which is the number
  guarding the self-hosting claim, since a large enough seed closes any
  lexicon.
- **The disclosure scan checks vocabulary, not description.** A section
  identified the deployment domain using entirely ordinary words. There is
  no automated answer to that class.
- **A completion condition that cannot be satisfied is worse than none.**
  One required a book for units that can never have one.

## What is YOURS: decisions the operator holds

1. **The 51 graph concepts** that would unblock 43 level-one units.
2. **Levels three to seven of the schedule**, which need profile-derived
   subject weighting and are therefore a disclosure decision.
3. **Whether level one can reach level two.** Both carry a four-year step,
   and level one has the smallest token budget in the scheme, so the corpus
   grows least where the reader grows fastest.
4. **Concept complexity per level.** Depth is the candidate metric, level
   one measures 5 and the graph reaches 10, and no target is set.
5. **Whether a mature version behaves distinctly enough.** `evals/` still
   has nothing measuring **unrequested action**.
6. **Whether the arms stay distinguishable when books are the unit.** Now
   testable and still the sharpest open risk.
7. **Whether a definition needs its own claim class.**
8. **Whether multi-head latent attention is admissible.**

## What is NOT yours

**Publishing.** The repository is private and audited clean. Discovery
scales with attention, so a launch post reopens the decision without a file
changing.

## Governing rules that are easy to lose

- **Run the gate, read the exit code, stop, then commit.**
- **Check CI separately.** The local gate is not the gate.
- **Read the output, not only the counts.** Reading the books found a real
  defect and a measurement error of mine in the same pass.
- **Verify a new check by making it fail.**
- **Corrections are kept in place, not deleted.** `BOOK_FORMATS.md` is
  marked superseded in part rather than removed.
- **A heuristic needs two pieces of evidence.** One inflection read `a`,
  `i` and `it` as verbs and wrote six nonsense words into core.
- **A guard over records must test `defines.kind`.**
- **No magic numbers in tests.** Tie an assertion to the lexicon.
- **Never `git checkout` to undo without checking what else is
  uncommitted.** It cost two authored waves.
- **Elegance is not evidence.** The level page counts rise by exactly six
  signatures a step and that is a consequence, not a reason.
- Irreversible or outward-facing actions need confirmation.


### Superseded live block, written 2026-09-25 mid-session

Kept for its findings. Its counts named seven books and 208 defined words
and went stale within the hour. What it recorded as the live defect, that
the corpus was a fraction of its schedule, was true and was stated with
the wrong denominator.

**Branch**: `main`, pushed to `origin`, `git@github.com:sgeos/epagoge.git`,
private. The repository was deleted and recreated after a history rewrite,
because a force-push leaves unreferenced objects fetchable by hash.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint.

**Validate by ANCESTRY and by CONTENT, never by a hash match.**

**Run the gate bare and read its exit code, then stop.** A commit landed on
a red gate twice in session 2. Reading the exit code is not enough if the
commit runs in the same invocation.

**Ancestry**: `main` should contain **`ebcc1d9`**, which completed the
dictionary. If it does not, this file predates a reset and is stale.

**Content** — each verified on 2026-09-25.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across **fourteen**
   checks, and **exits 0**.
2. The suite reports **432** tests.
3. `curriculum/vocabulary.json` holds **825 senses over 816 words**, of
   which **724** are at level one. **174** core, **37** ostensive, a seed
   of **235**. **218** nouns and **215** verbs carry a part of speech, and
   every one of them carries its plural or its inflections, enforced.
4. **The level-one dictionary is complete and self-hosting.**
   `tools/validate_closure.py` reports **687 of 687** words defined,
   **100 percent coverage and 100 percent closure**, with nothing on the
   frontier, nothing blocked and no cycles.
5. `curriculum/thesaurus.json` holds **749** entries covering every
   level-one sense, **194** carrying an antonym and **132** a synonym.
6. `tools/train_level.py` runs on `mps` and writes
   `evals/pilot/level_1.json`. **The corpus-to-model loop is closed.**
7. `git ls-files secret | wc -l` reports **0**, and history is clean, not
   only `HEAD`.

## What a resuming session should do first

1. Run the validity check and report the handoff valid or stale.
2. Read `docs/process/CURRENT_BRIEF.md`. It carries the seven goals, their
   real blockers, and every wrong turn already made once.
3. Read `docs/process/COMPLETION_CONDITION.md`.
4. **Wait for the human prompt.**

## The state

**The reference material is done. The corpus is not.**

| Goal | State |
| --- | --- |
| Dictionary coverage and closure | **Done.** 687 of 687, closure 100% |
| Thesaurus synonyms and antonyms | **Done.** 749 entries |
| Missing words added | **Done, and continuous** via `tools/admit.py` |
| **Level-one corpus draft** | **In progress. See the count below** |
| Train a level-one model | Pipeline closed; blocked on the corpus |
| Level-two dictionary and thesaurus | Blocked on a level-two lexicon |
| Level-two ablation | Blocked on the corpus |

### The live defect

**The corpus is a fraction of its schedule.** `curriculum/schedule/
level_01.json` holds **92 units** and `curriculum/books/level_1/` holds far
fewer books. **Everything downstream waits on this and nothing else does.**

One book per unit is roughly 40,000 words. **That is a draft, not the
budget.** `CORPUS_SCALE.md` wants 1,923 books at the low end. Say which is
meant whenever reporting, because conflating them overstates the project.

## Findings that outlive the session

- **The corpus validator is more permissive than the lexicon**, because it
  accepts a word by stripping suffixes. Exact tokenisation has no such
  latitude and is the stronger check. It has now found a real missing form
  three times, twelve plurals then `years` then `ends`.
- **Read closure, not acceptance.** Two interventions raised acceptance and
  moved closure not at all. The one that looked like a third failure was
  the only one that worked.
- **Generation crossed over for definitions and not for stories.**
  Definition acceptance fell 22.6, 16.4, 6.0 percent while authoring
  yielded about a hundred a round. Story acceptance runs near 50 percent.
  The rule is about definitions and I overstated it once as being about
  generation.
- **The bootstrap needed a seed written in something else.** A dictionary
  restricted to the function words accepted nothing in twenty-four
  attempts, blocked by `body`, `food`, `hand`, `head`, `mouth` and `one`.
  Nobody defines those. **37 ostensive words**, and the set has not grown
  in six rounds, which is the number guarding the self-hosting claim.
- **A large enough seed closes any lexicon.** That is why the completion
  condition bounds it.
- **A word the teacher reached for is evidence, not an error.** Eight words
  were admitted from one run's quarantine, and `hair` came with them
  because `fur` could not be defined without it.
- **A commit message asserting a property the tree does not have is worse
  than the missing property.** One claimed books were written as each
  finished when the call was still at the end of the run. The gate cannot
  catch this.
- **A long run must write as it goes.** One teacher timeout killed a
  ten-book chunk and lost all of it.

## What is YOURS: decisions the operator holds

1. **Whether the corpus draft is one book per unit or the full budget.**
   Everything downstream is sized by this answer.
2. **Levels three to seven of the schedule**, which need profile-derived
   subject weighting and so are a disclosure decision.
3. **Whether a mature version behaves distinctly enough.** `evals/` still
   has nothing measuring **unrequested action**.
4. **Whether the arms stay distinguishable when books are the unit.** Still
   the sharpest open risk, and now testable.
5. **Whether a definition needs its own claim class.**
6. **Whether multi-head latent attention is admissible.**
7. **Five manifest topics still have no home.**

## What is NOT yours

**Publishing.** The repository is private and audited clean. Discovery
scales with attention, so a launch post reopens the decision without a
file changing.

## Governing rules that are easy to lose

- **Run the gate bare, read the exit code, and stop before committing.**
- **A scan returning unexpected volume is presumed broken until its pattern
  is inspected.**
- **Read the output, not only the counts.** Reading the books found a real
  defect and one measurement error of my own in the same pass.
- **Verify a new check by making it fail.**
- **Corrections are kept in place, not deleted.**
- **A heuristic needs two pieces of evidence.** One inflection read `a`,
  `i` and `it` as verbs and wrote six nonsense words into core.
- **A guard over records must test `defines.kind`.**
- **No magic numbers in tests.** Tie an assertion to the lexicon.
- **Never `git checkout` to undo without checking what else is
  uncommitted.** It cost two authored waves.
- Irreversible or outward-facing actions need confirmation.


History records what was true at an increment. It is not stale, and
rewriting it corrupts the record. New sessions append; they do not edit.

### Session 1 continued, 2026-09-24, `6d8cce7` to `5fe15b6`

The previous live block described `b7e3c00` and went stale in almost every
number. It is not reproduced, because what it recorded as the live defect —
foundation domains feeding nothing — was resolved, and its content checks
named seven domains where there are now eleven. `CHANGELOG.md` carries the
sequence in full.

What changed in shape rather than in count. Domains went from seven to
eleven and are now declared rather than inferred. A curriculum schedule
exists, and it is where a concept gets its level. The lexicon became
prescriptive and grew from 64 level-one content words to 760. Books became
the unit of the corpus, then the unit of the ablation's ordering. The
corpus split into three artifacts for three readers.

Three external character standards were cross-referenced and one prediction
was tested and held. Four scope reviews of the project's own domains found
two that were missing the thing they are named for.

### Superseded live block, written 2026-09-24 at `eb04d6a`

Kept for its findings. Its content checks named `78` nodes without the
domain count, and it predated the `everyday` split and the foundation-feed
defect.

## Validity

**Branch**: `main`. There are no other branches and no remote.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint. A tracked document that names the
deployment domain is a defect regardless of how true it is.

**Validate by ANCESTRY and by CONTENT, never by a hash match.** A check
requiring `HEAD` to equal a recorded commit claims nothing else ever lands.

**Ancestry**: `main` should contain **`eb04d6a`** (accounting added), the
last commit before this was written. If it does not, this file predates a
reset and is stale.

**Content** — cheap, independent, each verified on 2026-09-24. Check the
rendered ORDER of this list, not just the next unused number.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across nine checks. It
   gates lint, format, strict typing, tests, a 95 percent coverage floor,
   graph and corpus validation, and the disclosure scan. Anything red means
   a statement below needs re-reading before it is believed.
2. The suite reports **192** tests. A lower number means this file predates
   work; a much higher one means it postdates this refresh.
3. `curriculum/graph/concepts.json` holds **78** nodes across **seven**
   domains and yields **4** derived transfer edges. If there is a domain
   named `everyday`, this file predates the 2026-09-24 split and is stale.
4. Vocabulary completeness is **100 percent**, 138 terms and **0** unmapped.
   A non-zero unmapped count means concepts are missing from the graph, not
   that the words are ordinary.
5. `git ls-files secret | wc -l` reports **0**. If it reports anything else,
   stop and do not commit.

## What a resuming session should do first

1. Run the validity check and report the handoff valid, or
   invalid-and-stale, on its outcome.
2. Read `docs/decisions/OPEN_QUESTIONS.md`. Nineteen answered, four
   deferred, two open. The answers carry their reasoning and several carry
   corrections that must not be re-reverted.
3. Read `evals/PRE_REGISTRATION.md`. It is **incomplete by design** and
   must be complete before the first ablation run.
4. **Wait for the human prompt.** Do not begin corpus generation on your
   own — see what is not yours, below.

## The state

**Green and clean.** Twenty-five commits, nothing uncommitted, nothing
unpushed, no remote. Seven documents in `secret/`, none tracked.

Fourteen decision records, seven specifications, three architecture
documents, 192 tests at 98 percent coverage.

**What exists.** A concept graph with prerequisite, instantiation, and
specialisation edges and two reach metrics. A corpus record schema with
twelve enforced rules across four record types. A claim taxonomy of six
classes. A primitive register of 34 hand-authored axioms. A per-level
vocabulary. A variance-pilot harness, run. A review tool that is also the
sampled audit. A teacher model pulled and verified.

**What does not exist.** Any generated corpus, any trained model, any
curriculum schedule. The 20-record sample corpus is a demonstration that
exercises every feature; it is not curriculum.

### Findings that outlive the session

- **The variance pilot measured a pairing gain of 20.7x seeds, free.**
  Twelve paired seeds beat 246 unpaired. The original five-seed unpaired
  design was off by two orders of magnitude in efficiency. Its numbers do
  **not** carry over, because the optimiser and schedule have since changed
  to Muon with warmup-stable-decay.
- **The pilot's first run was wrong in an instructive way.** It trained 23
  epochs, where ordering effects necessarily wash out, inflating the
  correlation from 0.954 to 0.987. Both results are kept because the
  difference is the finding.
- **An unexplained systematic difference appeared between two orderings
  that should be equivalent**, seven of eight pairs in one direction, sign
  following the ordering and not the execution position. Marginal at about
  p = 0.04. It is the shape of a false positive, and the ablation now
  carries a null arm because of it.
- **The teacher conflates adjacent concepts unless the prompt excludes
  them.** Asked to teach that use wears things out, it returned two
  sentences in three about things breaking. One negative constraint fixed
  it. Prompts must carry the concept's nearest graph neighbours as explicit
  exclusions; the graph already holds them.
- **Maximal update parametrization is confound removal, not optimisation.**
  Without it the three scale points carry different optimal hyperparameters,
  so any scale-dependence could be a tuning artifact — which lands on this
  project's own proposed mechanism.

## What is YOURS: decisions the operator holds

1. **The curriculum schedule.** Non-trivial and unstarted. Levels are
   authored, capacity per level and completion by the end are unmodelled,
   and nothing has scheduled anything. This is the largest open design task.
2. **Whether to soften the conjunction disclosure.** Finding A of the
   internal pre-commit audit. Each tracked constraint is innocuous; their conjunction
   narrows the domain. An option for tighter cover is recorded and not
   applied.
3. **The coverage manifest has never been reviewed by the operator.**
   It was derived by an agent and drives corpus generation.
4. **History as a domain**, recorded as a further addition and not added.
6. **Whether multi-head latent attention is admissible.** It is a low-rank
   projection, which `JACOBIAN_SPACE.md` bans in the base model. It must be
   measured against the effective-rank floor, not adopted on efficiency.

## What is NOT yours, and why it stays unstarted

**Corpus generation.** Blocked on the curriculum schedule, not on tooling.
The generator, the verification layers, and the teacher prompts do not
exist, and writing them before a schedule exists would encode guesses into
the place where changing them is most expensive.

**The ablation.** Blocked on the pre-registration, which is blocked on
re-measuring variance under the new optimiser.

**Re-running the variance pilot.** Cheap and unblocked, but its result is
only useful once the trainer uses the intended optimiser and schedule, which
the pilot harness does not.

## Governing rules that are easy to lose

- **Run `./tools/check.sh` before any commit.** The static analysis was
  configured in the initial commit and had never been executed; on first run
  it failed thirty-six ways.
- **A scan that returns unexpected volume is presumed broken until its
  pattern is inspected.** An unanchored alternation matched `ore` inside
  `before` and produced a hundred lines that would have looked identical to
  a clean result. That happened one minute after recording the same failure
  as a finding.
- **The vocabulary design was corrected three times, each time by running
  the validator rather than by reasoning.** Derivation from the graph was
  wrong twice. A concept can be taught before its name is introduced, so a
  word's level is authored and the graph bounds it from below only.
- **A low anchor-reach score may mean a concept is not worth teaching, or
  it may mean the graph is incomplete.** The metric cannot distinguish them.
  The teddy bear scored zero until its edges were drawn.
- **Corrections are kept in place, not deleted.** Several records carry a
  withdrawn claim beside its replacement. Removing one corrupts the record
  of why the replacement is right.
- **Never train toward being selected** by other models, and never let
  quirk absorb a negative result. Both are recorded with the reasoning.
- Irreversible or outward-facing actions need confirmation. Nothing is
  published, and publication needs explicit in-session authorisation.
rewriting it corrupts the record. New sessions append; they do not edit.

### Domain restructure, 2026-09-24, at `b7e3c00`

Seven domains became eleven. Every name that survived is an activity,
because a domain named for an activity excludes what does not serve it
while a domain named for a bare field admits everything in the field.
Mathematics is the deliberate exception and is frozen by the ablation.

Domains are now **declared** in a registry rather than inferred from node
membership, so that a domain decided upon and not yet written is visible.
Four are declared and empty.

Thirteen candidate names were withdrawn with reasons, all recorded in
`../decisions/DOMAIN_SET.md`, because the reasons constrain future
additions. The sharpest is that four separate candidates for the normative
domain each pre-committed to where obligations come from, when the conflict
between sources is the domain's actual subject.

### Session 1, 2026-09-23/24

Project created from nothing. Pre-planning closed after nineteen questions.
First implementation was the concept graph. The variance pilot ran. The
teacher model was pulled. Vocabulary went from unmapped to fully mapped.

Four corrections worth carrying forward are in the governing rules above.
The full sequence is in `CHANGELOG.md`, which is written for this purpose.
