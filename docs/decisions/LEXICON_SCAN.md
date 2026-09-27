# The first real lexicon scan, and what it does not measure

**Measured 2026-09-27.** `tools/scan_lexicon.py` had been written, tested
against fixtures and never run on a source. This is the first run, the
threshold decision it was supposed to inform, and two findings that came out
of doing it rather than out of planning it.

**The pipeline is in `LEXICON_SOURCING.md` and its step one is skipped.**
That step seeds from Dale-Chall and the New General Service List. Dale-Chall
has no licence anyone could find, the NGSL is CC BY-SA, and whether
consulting either is compatible with CC0 is unsettled and operator-held. The
tool takes seed lists as files, so the scan runs without them and the
answer changes which files are passed rather than what the tool does.

## The sources

**Public domain or CC0 only. Bodies live in ignored `tmp/lexicon-sources/`
and are not tracked.**

| File | Source | Tokens | SHA-256, first 16 |
| --- | --- | --- | --- |
| `tmp/lexicon-sources/src_mcguffey_1.txt` | McGuffey's First Eclectic Reader, Revised Edition, https://gutenberg.org/ebooks/14640 | 7,737 | `d25c72582b33dbf1` |
| `tmp/lexicon-sources/src_mcguffey_2.txt` | McGuffey's Second Eclectic Reader, https://gutenberg.org/ebooks/14668 | 17,476 | `7bbffe1a74b1f2a0` |
| `tmp/lexicon-sources/src_mcguffey_3.txt` | McGuffey's Third Eclectic Reader, https://gutenberg.org/ebooks/14766 | 26,809 | `544a38c181c9ed93` |
| `tmp/lexicon-sources/src_mcguffey_4.txt` | McGuffey's Fourth Eclectic Reader, https://gutenberg.org/ebooks/14880 | 64,278 | `0d4fb7a43bfc0238` |
| `tmp/lexicon-sources/src_noaa_ocean.txt` | NOAA Ocean Service, Ocean Facts, 23 pages, https://oceanservice.noaa.gov/facts/ | 12,124 | `f7ba69a8cfbaf6ab` |
| `tmp/lexicon-sources/src_noaa_jetstream.txt` | NOAA JetStream weather school, 134 pages, https://noaa.gov/jetstream | 118,031 | `25f03f5817768884` |
| `tmp/lexicon-sources/src_nasa_spaceplace.txt` | NASA Space Place, 8 articles, https://spaceplace.nasa.gov | 7,172 | `594d2bd584537403` |

**Retrieved 2026-09-27.** The readers are public domain by age. The federal
material is public domain by statute. Two transformations were applied: the
Project Gutenberg licence header and footer were cut from the readers, and
markup, scripts and navigation were stripped from the web pages.

**The hashes are a snapshot and not a reproducibility guarantee, and the
distinction is not decorative.** A Gutenberg file is stable, so its hash will
match on a re-fetch. **A live website's will not**, because the page changes
and because the markup stripping is sensitive to that change. For the federal
sources the hash says which bytes produced these counts and nothing stronger.

## The threshold, and there is no knee in the data

**Total candidates, 11,863 at every threshold.** What the threshold moves is
the split between bulk work and one-at-a-time judgement.

| Frequent at | Frequent somewhere | Long tail everywhere |
| --- | --- | --- |
| 2 | 5,976 | 5,887 |
| 3 | 3,998 | 7,865 |
| **5** | **2,376** | **9,487** |
| 8 | 1,468 | 10,395 |
| 10 | 1,182 | 10,681 |
| 15 | 799 | 11,064 |
| 20 | 579 | 11,284 |
| 30 | 387 | 11,476 |

**The default of five is kept, and it is not vindicated.** The curve is
smooth. There is no elbow, no plateau and no natural break, so nothing in the
data prefers five to three or to eight. **What the scan establishes is that
the choice is arbitrary within a wide band**, which is more than was known
and less than the record hoped for. Five is kept because moving it without a
reason would be churn.

**This is a decision by eye and the record says so** rather than implying a
derivation.

## One source supplies half the frequent group

| Source | Tokens | Frequent in it | Per 10,000 tokens | Frequent in it alone |
| --- | --- | --- | --- | --- |
| JetStream | 118,031 | 1,528 | 129.5 | 1,200 |
| McGuffey 4 | 64,278 | 751 | 116.8 | 456 |
| McGuffey 3 | 26,809 | 200 | 74.6 | 57 |
| McGuffey 2 | 17,476 | 145 | 83.0 | 42 |
| Ocean Facts | 12,124 | 214 | 176.5 | 76 |
| McGuffey 1 | 7,737 | 96 | 124.1 | 24 |
| Space Place | 7,172 | 103 | 143.6 | 51 |

**1,200 of the 2,376 frequent words are frequent in JetStream and nowhere
else**, so one source of seven supplies half the group. **That is corpus
composition rather than a threshold artifact**, and the per-10,000 column is
how the difference shows: the rate does not track size, with the smallest
NOAA source densest at 176.5 and a middling reader sparsest at 74.6.

**But an absolute threshold is still not comparable across sources.** Five
occurrences in 7,737 tokens and five in 118,031 are different claims about
how characteristic a word is, and the tool treats them alike. This is
recorded rather than fixed, because fixing it means choosing a rate and no
measurement supports one yet.

## The era contrast does not measure archaism, and its symmetry is the proof

**`LEXICON_SOURCING.md` asserts that archaism is invisible to a counter.**
The design here was meant to make it visible by scanning Victorian readers
against modern federal material, so that a word frequent in 1880 and absent
now would show up. **It does not work, and the reason is worth more than the
attempt.**

| Direction | Frequent group | Absent from the other era | Share |
| --- | --- | --- | --- |
| Victorian, absent from modern | 908 | 514 | 56.6% |
| Modern, absent from Victorian | 1,662 | 984 | 59.2% |
| Frequent in both | 194 | | |

**The two directions are nearly the same, at 56.6 and 59.2 percent.** If the
contrast were measuring era, it would not be symmetric, because modern
English has not lost as much vocabulary to the last century as it gained.
**What is symmetric is topical disjointness**, and that is what these figures
measure. Victorian readers are about farms, families and moral tales.
JetStream is about weather. Neither mentions the other's subject.

**Removing the obvious confounds does not rescue it.** Of the 514, **80 are
capitalised at least 80 percent of the time**, a proper-noun proxy that
catches `Alfred`, `Annie` and `Bessie`, and 19 are two letters or fewer,
leaving 418. **Inspecting the first 45 of those 418, most are still topical
rather than archaic**: `barn`, `beaver`, `bee`, `berries`, `breakfast`,
`brook` and `buds` are words a modern child knows and a weather manual has no
use for. The genuinely archaic ones in that window are few, `bade`, `behold`,
`billows`, `bosom`, `bough` and `bridle`.

**So the record's claim stands and now has a reason.** Archaism cannot be
separated from topic by counting, **because the public-domain modern corpus
available is federal technical material and is topically disjoint from
Victorian readers by construction.** A modern source in the readers' own
subject matter would be needed, and modern material is not public domain.
**This is structural and not a parameter.**

## What the contrast is good for, which is selection rather than exclusion

**The 194 words frequent in both eras are the useful output.** A word a
grade-appropriate Victorian reader used often and a modern federal source
also uses often is neither archaic nor narrowly technical. **That is a
selection rule with a reason behind it**, as against a frequency rank, which
has none.

**161 of the 194 were not already admissible.** The first admission batch is
drawn from them.

## The first batch

**47 words admitted at level two**, each carrying the source that proposed
it, which is what the `source` field on a term exists for.

**Level two holds 934 distinct words admissible against a target of about
10,000**, so **roughly 9,066 remain**. Nothing here claims the lexicon is
close.

**Closure did not fall. Level two defines 897 of 897 words needing a
definition, at 100 percent, grounded 914, self-hosting yes**, against 850 of
850 before. No word was admitted without a definition.

**`gray` was proposed and refused.** It is frequent in both eras and the
lexicon already admits `grey`. Admitting both would give one word two
spellings, which is a spelling decision and not a vocabulary one. **This is
the clearest small example of the scan proposing and not deciding.**

## Three defects found by doing this, not by planning it

**The lexicon could not say that an adjective compares with `more`.**
Declaring `beautiful` an adjective generated `beautifuler` and
`beautifulest`, exactly as the plural rule once generated `funs` and
`magics`. The safeguard had been to leave such a word undeclared, which
loses the part of speech in order to protect the forms. **`periphrastic` now
qualifies `adjective`** the way `mass` qualifies `noun`, and the comparison
check skips it. The shipped lexicon had no instance, because 58 declared
adjectives had been chosen by hand to avoid it.

**`admit.py` carried its own copy of the recognised parts of speech.** It
rejected `mass`, added on 2026-09-26, and `periphrastic`, added the same day
as this scan, so a qualifier the validator understood could not be admitted
through the tool that admits words. **That is the field-enumeration defect in
`FIELD_ENUMERATION.md`**, a second copy of a list with one authority, and the
tool now reads the authority. It also generated a plural for a mass noun,
which the validator had been exempting since the day before, so the two
halves of the same rule disagreed.

**`hours` was filed as its own headword at level six.** It is the plural of
`hour`, which this batch admits at level two, and the collision is what
surfaced it. **That is the ninth inflected form found filed as a word**,
after `copied` was the eighth. Removed, with `hour` carrying the form.

## Two gate properties this exposed, and neither is a bug

**A check derived from git history cannot pass in the commit that changes the
lexicon.** `word_provenance.py --check` compares the tracked provenance file
against what the history produces, and the history does not contain a word
until the commit adding it exists. So the gate passed before this batch was
committed and failed after, and the file had to be regenerated in a following
commit. **The same shape already caught `stamp_books --check`**, which skips
files modified in the working tree, which is exactly the set whose dates a
pending commit is about to change. This is the second instance and it is
structural.

**A check that resolves paths passes locally on untracked files.** The source
table first named the scan sources by basename. Locally they resolved because
the files were sitting in `tmp/`; in the runner's clone they did not exist and
the reference check reported eight unresolved. **Writing the full ignored path
makes `git check-ignore` answer instead**, which works in any clone because
`.gitignore` is tracked. The check was right both times and what differed was
which of its three resolution paths answered.

## What this does not settle

**No judgement was made on the long tail.** 9,487 words at the chosen
threshold, which the pipeline says to inspect one at a time, and none of them
was.

**The 2,376 frequent words are not admitted and most should not be.** They
include proper nouns, markup residue such as `abi` and `acronyms`, and
technical weather vocabulary well above grade four.

**No archaism judgement was made.** The 418 candidates are a pool for
judgement at drafting time, which is where the record already said this
happens.

**The threshold may be wrong and nothing here would detect it.** A threshold
is only testable against how many of its proposals survive judgement, and
judgement has run on 47 words.
