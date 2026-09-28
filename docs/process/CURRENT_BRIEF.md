# Current brief. Give every unit a question book, and settle their band

**Written 2026-09-27**, replacing the lexicon-scan brief, whose completion
condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**54 of 96 level-one schedule units carry no question-and-answer book.** That
is the operator's second priority and the obvious next batch, named as such in
the handoff.

**The reason the form matters is measured rather than assumed.** On 2026-09-25
the corpus held one question mark in 4,419 records, no question with an answer
after it, and the model met "what is the cup ?" by carrying on rather than
answering. **A model reproduces the forms it was shown.** The form is now
present in 42 units and absent in 54, so the corpus can show a question being
answered for fewer than half its subjects.

**A second job comes with it.** 62 books are reported outside the typical word
range and most are question books, which run about 220 to 330 words against a
narrative band of roughly 500 to 870. **The gate prints that on every run and
nothing has acted on it.** This project has already been bitten once by a tool
announcing a fact forty times while nobody heard it, so the flag gets resolved
rather than carried: either question books are brought into a band, or they
have their own band and the record says what it is and why.

## What to do

1. **Write a question-and-answer book for every unit that has none.**
2. **Decide the question book's word band** and record it, so the flag either
   stops firing or means something.
3. **Measure the question-mark density afterwards** rather than asserting it
   improved.
4. **Check the exchange count.** The first book written under this brief
   produced 13 exchanges over 14 spreads rather than 16 records. Pair coverage
   counts only books with exactly 16 records, so a short question book is
   invisible to that measure, and that interaction should be stated whichever
   way it is resolved.

## Prior failures, and the specific wrong turns to avoid

**Do not chain the gate to the commit.** Done twice in this session's history
and it pushed a failing tree to `origin` once. Run the gate alone, read the
exit code, stop, then commit.

**Do not pipe a run through a filter and read the exit code.** It reports the
filter's status. This has already cost one wasted training run and hidden one
lint failure.

**Do not read a count from arithmetic.** Six instances. If the gate supplies
the number, the number comes from the gate.

**Do not assume a green local gate means a green clone.** Four divergences, and
the general form is that a check consulting the filesystem or git history
passes on state the runner does not have. A path named in prose must resolve
by tracked file or by `.gitignore`, not by a file that happens to exist here.

**Do not treat a vocabulary rejection as a vocabulary problem.** Sixteen title
refusals were the generator's own word-count bound rather than the lexicon, and
the first question book under this brief rejected `important`, `result`,
`final` and `matters` as outside the ceiling, which is the ceiling working.
**Read what the rejection says before widening anything.**

**Do not widen the lexicon to make generation succeed.** A word the teacher
reached for is evidence worth considering and not a reason to admit on the
spot, and admission is a separate judgement with a definition attached.

**Do not top up a short book by padding it.** There is a fill mode for books
that exist and are short, and a book brought to length with filler is worse
than a short one, because the length then means nothing.

**Do not modify untracked files.** Operator constraint.

**Do not let the word count regress.** Any content book leaving its band, or
any book losing a metadata field, is a defect introduced by this batch rather
than a property of it.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, the terminal-stage record
licensing question, schedules for levels three to seven, `sources/` and level
seven, and the acquisition scheme in `../decisions/SOURCE_ACQUISITION.md`,
which stays unadopted. **Announcing the repository is not this brief's
either.**
