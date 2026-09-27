# Current brief. Run the first real lexicon scan and set the threshold

**Written 2026-09-27**, replacing the brief that found the frontier, whose
completion condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**The level-two lexicon is the operator's first priority and it holds 879
words against a target of about ten thousand.** A complete draft lexicon
precedes level-two corpus drafting, by operator direction, so everything
downstream waits on it.

**`tools/scan_lexicon.py` exists and has never been run on a real source.**
The pipeline in `../decisions/LEXICON_SOURCING.md` has five steps and the
project has done none of them. The tool was written, tested against
fixtures, and left.

**The threshold is the specific missing measurement.** That record says what
counts as frequent "is a parameter with a default of five and no measurement
behind it" and that it "should be set from what the first real scan looks
like rather than guessed now." **A default nobody measured is the same defect
class as a check nobody ran**, which this project has already met once when
its static analysis reported thirty-six errors on first execution.

## What is out of scope, and this is the important half

**Do not attempt the whole lexicon.** Every admitted word needs a definition
or level two stops being self-hosting, and `admit.py` refuses a word without
one. Nine thousand definitions is not one session's work, and a session that
admits words without them trades the project's central property for a count.

**Do not touch step one of the pipeline.** It seeds from Dale-Chall and the
New General Service List. Dale-Chall has no licence anyone could find and the
NGSL is CC BY-SA, which a CC0 repository cannot carry, and whether consulting
them is compatible with CC0 is unsettled and operator-held. **The pipeline
was deliberately built so the answer changes which files are passed in rather
than what the tools do**, so the scan runs without them.

## What to do

1. **Vendor public-domain and CC0 sources into ignored `tmp/`**, with a
   tracked record naming each one, its retrieval date, the licence determined
   at retrieval and a content hash. Bodies are not tracked.
2. **Include both Victorian readers and modern federal or Smithsonian
   material**, because the contrast is what makes archaism measurable.
3. **Run the scan and set the threshold from what it looks like**, reporting
   the distribution and the sensitivity at neighbouring values.
4. **Measure the archaism problem** the record asserts and has never
   quantified.
5. **Admit a first batch with definitions**, sized to what can be defined
   properly, so the pipeline is proven end to end from source to admitted
   word rather than reported on.

## Prior failures, and the specific wrong turns to avoid

**Do not chain the gate to the commit.** Done an hour ago. The gate, the
commit and the push in one shell command pushed a failing tree to `origin`,
because the commit ran on the gate's output instead of its exit code. Run the
gate alone, read the exit code, stop, then commit.

**Do not read a count from arithmetic.** Five instances, most recently a pin
count written as six when the measured values were three, one and one. If a
tool can supply the number, the number comes from the tool.

**Do not pool frequency across sources.** The per-source choice is
load-bearing and recorded. A word frequent in one source and absent from the
rest is a word that source needed, and pooling buries it. The tool already
does the right thing; the mistake would be in reading its output.

**Do not treat the scan as a decision.** It proposes. The project's thesis is
that uncurated input produces undesirable properties, and a frequency list is
uncurated by construction.

**Do not expect the counter to see archaism.** A public-domain source is
public domain because it is old. A word can be frequent, plainly useful in
1880 and wrong for a child now, and the modern-source contrast identifies
candidates for judgement rather than deciding any of them.

**Do not report a threshold as tuned.** If it is chosen by looking at a
distribution, say that, and give the neighbouring values so a reader can see
what the choice costs.

**Do not commit a source body or a licensed word list.** Both are licensing
exposure and one is size exposure, and `sources/` is tracked, so a mistake
there lands in history.

**Do not let coverage fall.** Level two reports 850 of 850 words needing a
definition. A word admitted without one shows as undefined while the closure
check may still exit 0, which is a silent degradation rather than a failure.
Check the coverage figure, not just the exit code.

**Do not widen the lexicon to make a scan look productive.** A candidate the
curriculum has no use for is not an improvement, and `UNUSED_FORMS.md`
records what happens when forms are admitted faster than they are used.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, the terminal-stage record
licensing question, schedules for levels three to seven, `sources/` and level
seven, and the acquisition scheme drafted in
`../decisions/SOURCE_ACQUISITION.md`, which stays unadopted.
