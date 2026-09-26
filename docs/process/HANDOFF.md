# Handoff Prompt

**Refreshed 2026-09-26, describing the tree at the commit that carries
this refresh.** Session 4 published the repository, reviewed the operator's
`keleusma` repository for practice worth adopting, gave every book its
metadata, closed the level-one word band, settled whether capacity or
corpus is the limit, made the scaling law reproducible, and took the model
from perplexity 120 to 41. **It also withdrew four of its own findings**,
which are listed below because the reasoning that produced them is more
useful than the claims were.

**It ended by recommending that the loop stop.** Everything left at level
one is a judgement per item or is blocked on a decision the operator holds,
and the cheapest-looking remaining work is work the project has already
decided against. `CURRENT_BRIEF.md` says which is which. Read this block, run
the validity check, then stop and wait for the human prompt.

**NO COMMIT HASH IS STAMPED HERE, deliberately.** A stamp naming the
commit that contains it is impossible, and one naming the parent is off by
one the moment anything else lands. Every hash in this repository changed
once already. **Validate by ancestry and by content**, which the next
section gives in a form that does not depend on any hash.

**The history was rewritten twice and the repository was then recreated
public at those rewritten commits.** Recorded below under publication.

---

## Validity

**Branch**: `main`, pushed to `origin`, `github.com/sgeos/epagoge`,
public. **CI is green and must be checked, not assumed.** It was red on
the previous head while the local gate passed, because one check is
derived from git history and the runner clones one commit.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint.

**Validate by ANCESTRY and by CONTENT, never by a hash match.**

**Run the gate, read its exit code, then stop before committing.**

**Ancestry cannot be checked by commit identity.** Every hash in this
repository changed on 2026-09-25 when the history was rewritten twice,
first to remove deployment vocabulary and then to remove the project's
former name. **Check by content instead**: the first commit's `README.md`
begins `# Epagoge`, and `git log --all --format='%B' | grep -ic <the
former name>` returns 0. The former name is recorded once, under the
discipline `CLAUDE.md` points to, and nowhere else.

**Content** — each verified on 2026-09-25.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across **twenty-one**
   checks and **exits 0**, in about nine seconds. **The metadata check
   fails after a date rollover** until `tools/stamp_books.py --level 1` is
   re-run, which is the check working rather than a defect.
2. The suite reports **484** tests.
3. `curriculum/vocabulary.json` holds **961 senses over 928 words**, of
   which **845** are at level one and **879** at level two. **178** core,
   **37** ostensive, a seed of **257**, and **84** substitutions.
4. **Both dictionaries are complete and self-hosting**, 808 of 808 at
   level one, closure 100 percent, nothing blocked and no cycles.
5. `curriculum/thesaurus.json` holds **927** entries, 195 with an antonym
   and 132 with a synonym.
6. `curriculum/books/level_1/` holds **246** books over **4,691**
   records. Every unit has a book and **17 are question-and-answer
   books**. **244 of the 246 are at sixteen spreads**; the two that are not
   are `bk.dictionary.1` at 176 records and `bk.dictionary.seed` at 611,
   which are reference books rather than picture books and which the
   validator exempts by design. This item read "every book is at sixteen
   spreads" until 2026-09-25, which anyone checking it would have found
   false.
   **The word count is deliberately not asserted as an equality**, since
   any later fill raises it. It was **172,810** at this refresh, up from
   55,510 the previous morning. Check that it is **at least** that, that
   **all 244** content books are inside the word band, and that none is
   above it.
7. `curriculum/provenance.json` gives every word a first commit and a
   reconstructed admission criterion.
8. `git ls-files secret | wc -l` reports **0**, and history is clean of
   both the deployment vocabulary and the former project name, verified
   by grepping every commit rather than only `HEAD`.
9. `tools/check_references.py` reports **no unresolved references** over
   the tracked documents, with `CHANGELOG.md` exempt.
10. `tools/stamp_books.py --level 1 --check` reports **246 books, 0 missing
   a field**. Every book carries `about`, `teaches`, `author`, `licence`,
   `first_published` and `published`, and the 17 question-and-answer books
   still declare `form`.
11. The disclosure scan reports it covered **tracked and untracked files,
   line by line and with whitespace collapsed**. A scan that does not say
   all three is the old one, which missed both.

**Two numbers in the closure output look like a contradiction and are
not.** It reports 808 defined of 808 needing one, and 825 grounded. The
difference is 17 definitions of seed words, which are written but are not
counted against the requirement because a seed word needs no definition.

## What a resuming session should do first

1. Run the validity check and report the handoff valid or stale.
2. **Check CI.** A green local gate does not mean a green remote one, and
   that has now happened twice for two different reasons.
3. Read `docs/decisions/THREE_PROBLEMS.md`, which says what kind of
   problem each level is.
4. Read `docs/process/PROCESS_STRATEGY.md` for durable practice, then
   `docs/process/CURRENT_BRIEF.md` for what is live. The split is new as
   of 2026-09-25 and exists because a lesson filed in a document marked
   for deletion is deleted with it.
5. **Read `evals/pilot/LEVEL_ONE_*.md` before quoting any number from
   `level_1.json`.**
6. **Wait for the human prompt.**

## The state

| Goal | State |
| --- | --- |
| Level-one reference material | **Done.** 808 of 808, closure 100 percent |
| Level-one corpus | **Complete and at length.** 244 of 244, 172,810 words |
| Corpus or capacity the limit? | **Settled.** Corpus. Saturates at 128 |
| Scaling law | **Reproducible**, and the marginal rate rises |
| Level-one book metadata | **Done.** All six fields on all 246 books |
| Train a level-one model | **Done.** Perplexity 41 at width 1024 |
| Level-two reference material | **Done**, lexicon at 9 percent of target |
| Level-two corpus | **One module of 27 scheduled** |
| Level-two ablation | **Blocked** on corpus scale and on an endpoint |

### One live defect, measured

**The corpus reached its length standard and the defect is closed.** All
244 content books are inside the band, none above, 172,810 words against
55,510 the previous morning. Measured on the finished corpus, the marginal
rate is **0.300 nats a doubling** and the best model reaches perplexity
**41** at width 1024, so growing it further would still pay.

**A third of the level-one lexicon is never used.** 2,051 surface forms
admitted, 1,363 used, **688 never**, and 11 headwords absent in every form.
Mostly inflections, admitted automatically and used only if a writer
happens to need them. Each is a judgement about whether a module should use
it, be drafted for it, or whether admitting it was a mistake, so a loop
should not close it.

**The level-two lexicon holds 879 words against a target near 10,000.**
That is a schedule nobody has written, not a backlog of admissions, and it
is the operator's.

### Four findings this session withdrew, and why they are kept

**Each was recorded as a measurement and was not one.** The reasoning is
kept beside each claim rather than deleted, because the failure mode is
more reusable than the finding was.

1. **"The model is too big for the corpus."** Refuted by a sweep of seven
   widths from 16 to 1024 on one frozen corpus. Held-out loss falls
   monotonically with width and the curve saturates near 128, so smaller is
   decisively worse and bigger barely helps.
   `../../evals/pilot/LEVEL_ONE_CAPACITY.md`.
2. **"Filling books adds low-value tokens, at 0.199 nats per doubling."**
   That compared two figures measured against different held-out sets.
   Against one, the same doubling bought **0.316**, the largest increment
   in the series. `../../evals/pilot/LEVEL_ONE_SCALING.md`.
3. **"A question mark triggers the token `was`."** Six prompts sampled at
   one seed all began alike for a reason unrelated to the prompt. Over
   eight prompts at eight seeds it happens once. **The teacher was shown
   this as a measurement and built a theory on it.**
   `../../evals/pilot/LEVEL_ONE_INTERACTION.md`.

4. **"Distinct-token share tracks quality."** Swept across temperature
   the better-fit model is less varied at every one and recovers past the
   worse model's figure by 1.2, and its attractor frequency falls from 24
   to 3. **Both figures measure sharpness**, and a better model is sharper.
   `../../evals/pilot/LEVEL_ONE_INTERACTION.md`.

**The class they share is in `PROCESS_STRATEGY.md`**: before reporting a
difference, say what was held fixed and check that it was. **All four were
found by doubting a result, not by a new measurement.**

## Findings that outlive the session

- **The endpoint picks the sign.** Same corpus, arms and seeds: at 800
  steps the curriculum arm is worse in 8 of 8, paired t +8.35; at 1,600
  it is better in 7 of 8, t −3.17. **Both would pass a naive test.**
  Anyone reporting an ordering effect from here must say what endpoint
  produced it.
- **The model is limited by corpus, not training.** At width 256 and
  3,200 steps it reaches training loss 0.040 and held-out 7.794 against
  ln(2253) = 7.72 for uniform: it memorises the corpus and predicts
  unseen text worse than chance. Best reachable is perplexity **133**.
- **Held-out loss falls about 0.29 nats per corpus doubling**, putting
  10^6 tokens near perplexity 35. Extrapolated over 2.3 orders of
  magnitude from 0.9, and optimistic and pessimistic for reasons the
  record names.
- **A model reproduces only the forms it was shown.** The corpus held one
  question mark in 4,419 records and no question with an answer, so the
  model continued a question instead of answering. Scale does not touch
  this. 17 question books now exist.
- **Silent partial coverage is this project's characteristic failure.**
  A book ordering covering 13 of 146, a chunker keeping a quarter of the
  corpus, a generator skipping seven domains, nine front-matter builders
  that would have erased a new field. **A tool that returns less than it
  was asked for must say so.**
- **The generation-time check was weaker than the tokeniser** and let
  eleven forms into books the lexicon did not carry. `unlicensed` is
  exact by default now.
- **Seven inflected forms were filed as headwords**: `depends`,
  `reporting`, `settles`, `allowed`, `ones`, `tens`, `explanations`.
  Each blocked every form but the one filed.
- **Nothing compares a derived form against English.** The doubling
  check closes one narrow class; seven verbs needed hand-written entries.
- **A word list extracted from a text is not the text**, which is what
  makes a licensed source usable for vocabulary and not for prose.

## What is YOURS: decisions the operator holds

1. **The endpoint and estimator, item 10.** It fixes the sign of any
   ordering result this project publishes.
2. **Whether consulting Dale-Chall and the NGSL is compatible with CC0.**
   Both are in `tmp/lists/` and neither is committed. Nine thousand words
   wait on this.
3. **Schedules for levels three to seven.** None exist.
4. **The minimum meaningful effect, item 7**, justified from the
   literature.
5. **`sources/` and level seven.** Empty, licensing unexamined, and
   nothing in `evals/` measures a real task.
6. **Whether level-one's 1,280-word upper bound is right**, since it
   exceeds the picture-book convention of 1,000.
7. **Whether the `m1.compare` cycle resolution was the right one.** Two
   alternatives are named in the commit; one adds a 93rd unit.
8. **Whether a parked book should leave the repository.** `exclude/` is
   gitignored as asked, so moving a tracked book there removes it.

## Publication

**Audited on 2026-09-25 and published the same day.** What the audit
changed, and what remains binding.

**Done.** Six open questions that described the deployment domain moved
to `secret/`, each leaving a stub saying it exists and is answered
privately. The same class of statement was removed wherever else it
appeared. Thirteen literals were scrubbed from every commit in history,
verified at zero occurrences. The teacher model is attributed in the
README. Two false status lines were corrected. A stale corpus stream was
removed. The project was renamed and the former name scrubbed from
content, paths and commit messages.

**The repository was recreated, not force-pushed.** Deleting the earlier
remote is what makes its objects unreachable; a force push would have
left them fetchable by hash. That remote was private for its whole life
and no hash from it was ever held by anyone but the operator.

**The scrub binds only what was tracked when it ran.** Everything written
from here on is subject to the same discipline, and the disclosure scan
in the gate is what enforces it rather than anyone's memory.

**The public surface, set 2026-09-25 and verifiable with `gh repo view`.**
Description and six topics set. Licence detected as `0BSD`, which required
reducing `LICENSE` and `LICENSE-CC0` to bare licence text and moving the
scope map to `LICENSING.md`; a preamble in front of the text defeats the
detector. Wiki and projects off, issues on. A build badge in the README.
`CONTRIBUTING.md`, `CITATION.cff`, `llms.txt`, a pull-request template and
three issue templates.

**A ruleset named `main` is active with no bypass actors.** It blocks
deletion, blocks non-fast-forward pushes and requires linear history.
**It binds the owner too**, so another history rewrite means disabling it
in settings first. That is deliberate and it will surprise anyone who has
forgotten it. Required status checks were **not** enabled: under rulesets
that applies to direct pushes as well as pull requests, and since checks
run only after a push lands it would force every change through a pull
request.

## What is NOT yours

**Announcing.** The repository is public; discovery is not. A launch post
reopens the decision without a file changing, and it is the operator's.

## Governing rules that are easy to lose

- **Run the gate, read the exit code, stop, then commit.**
- **Check CI separately.** Twice red while the local gate was green: once
  for a missing virtual environment, once for a shallow clone.
- **A tool that returns less than it was asked for must say so.**
- **A check whose answer depends on the shape of the checkout must say
  which shape it needs.**
- **Finishing beats starting.** A fill run that spends its limit on new
  books leaves the short ones short.
- **Corrections are kept in place.** A wrong claim in a pushed commit is
  corrected in the next one, not amended away.
- **Check a tool's remove path apart from its add path.**
- **A metric that agrees with you whatever happens is not a
  measurement.** One reported 100 percent and would have for an untrained
  model.
- **Read the output, not only the counts.**
- **`git-filter-repo --replace-text` has no comment syntax.** Every line
  is a literal. A commented file was run on 2026-09-25 and its bare `#`
  replaced every `#` in every file in history, corrupting every Python
  source and every Markdown heading. **Take a mirror clone first**; that
  is what made it a detour rather than the end of the project.
- **A rewrite that changes content must be checked against commit
  messages too.** Rewriting the name left one message describing a rename
  that no longer existed and asserting the opposite of the truth.
- **No magic numbers in tests.** Tie an assertion to the lexicon.
- **Never `git checkout` to undo without checking what else is
  uncommitted.**
- **A workflow that triggers on push must not group its concurrency by
  ref.** With `cancel-in-progress`, a second push to `main` cancels the
  first commit's run and leaves that commit with no verdict. Key a branch
  run by `github.run_id`, which cannot collide. Committed in the wrong
  form on 2026-09-25 and caught by reviewing the reference repository.
- **`astral-sh/setup-uv` publishes no floating major tag past v7** while
  its current release is v10, so it is pinned exactly and the other two
  actions are not. The asymmetry is in the workflow file.
- **A guard that has not been shown able to fail is not a guard.** Show a
  new check failing against a deliberately broken input before trusting
  it.
- **A by-name exception list inside a checker is the defect the checker
  exists to catch.** Ask `git check-ignore`, not a list.
- **The disclosure scan now covers untracked files and collapses
  whitespace.** It did neither until 2026-09-25, and both gaps let banned
  vocabulary reach a public push under a green gate. **`CHANGELOG.md`
  carried a deployment-implying phrase from before publication**, wrapped
  across a line break where a line-based scan could not see it. Fixed
  forward; the operator holds whether the history needs anything.
- **Do not fold the tokeniser's typography into prose a person reads.**
  It maps a dash to a hyphen, which is right for word splitting and turned
  `things down-like notes` into nonsense across 99 book descriptions.
- Irreversible or outward-facing actions need confirmation. A prior
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
