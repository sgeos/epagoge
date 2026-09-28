# Current brief. Close the gap between a candidate and an admitted word

**Written 2026-09-28**, replacing the brief that built `elenchos`, whose
completion condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**The level-two lexicon is the operator's first priority and holds 934 words
against a target near ten thousand.** A complete draft lexicon precedes
level-two corpus drafting, by operator direction, so everything downstream
waits on it.

**Candidates are not the obstacle.** The scan of 2026-09-27 produced 2,376
words frequent in at least one public-domain source, and 9,487 more in the long
tail.

**Definitions are the obstacle, and the pipeline has a hole in the middle.**
Every admitted word needs a definition or level two stops being self-hosting,
and `admit.py` refuses without one, correctly. `generate_dictionary.py` writes
definitions for words that are already admitted. **Nothing takes a candidate
and produces the definition that would let it be admitted**, so the only route
is writing them by hand, which is what the 47-word batch did.

**Nine thousand words at a hundred a session is ninety sessions.** That is not
a plan, and the reason to build the bridge is that it makes every later batch
cheap rather than that it makes this one large.

## What to do

1. **Write the missing step**: take candidate words with their concepts,
   have the teacher draft definitions inside the level's own vocabulary, and
   emit exactly what `admit.py` consumes.
2. **Run it for a substantial first batch**, themed so that concept assignment
   is tractable rather than a per-word guess.
3. **Record what the acceptance rate is**, because it decides whether the
   remaining gap is reachable at all and nobody has measured it.

## Prior failures, and the specific wrong turns to avoid

**Do not admit a word without a definition.** Coverage is reported and the
closure check can still exit 0 while a word sits undefined, so a silent
degradation is possible. Check the coverage figure, not just the exit code.

**Do not widen the lexicon to make the pipeline look productive.** A candidate
the curriculum has no use for is not an improvement, and `UNUSED_FORMS.md`
records what happens when forms are admitted faster than they are used.

**Archaism is invisible to the scan and to the teacher.** Measured on
2026-09-27: the era contrast does not separate archaism from topic, and the
public-domain sources are old because they are public domain. **Judgement at
drafting is the only place this is caught**, and it has to be spent.

**Check the generated forms, not just the word.** Admitting a noun generates a
plural and an adjective generates comparison forms, and both rules have
manufactured nonsense before: `funs`, `magics`, `farrer`, `beautifuler`. The
`mass` and `periphrastic` qualifiers exist for exactly this and should be used
rather than discovered again.

**A word the teacher reaches for is evidence, not permission.** Admission is a
separate judgement with a definition attached.

**Record provenance at admission.** The corpus is CC0 and some candidate lists
are not, so where a word was proposed matters more than the word does.

**Do not read a count from arithmetic.** Six instances. The gate supplies these
numbers.

**Do not chain the gate to the commit.** Done in this session and it pushed a
failing tree to `origin`.

**Do not let a new tool default its output to a tracked path.** Three tools did
and one was overwritten twice before the default was removed.

**Do not report an acceptance rate from one batch as a property of the
pipeline.** One themed batch is one sample, and themed batches are the easy
case.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, which keeps step one of the
sourcing pipeline shut. The terminal-stage record licensing question, schedules
for levels three to seven, `sources/` and level seven, and the acquisition
scheme in `../decisions/SOURCE_ACQUISITION.md`, which stays unadopted.
**Announcing the repository is not this brief's either.**
