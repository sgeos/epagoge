# External references, and why they are fetched rather than vendored

**Decided 2026-09-26, operator direction.** The project consults external
references for facts about English. **They live in `tmp/references/`, which
is ignored**, so nothing licensed is redistributed by this repository and a
clone stays CC0 by construction.

**This record exists so that independent work can fetch the same things.**
It is the one place where naming a source with a link is the right thing to
do, because a check that depends on a file nobody can obtain is not a check.

## What to fetch, and how to verify it

    mkdir -p tmp/references && cd tmp/references
    curl -LO https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz
    curl -LO https://www.gutenberg.org/files/3202/files/mthesaur.txt
    tar xzf wn3.1.dict.tar.gz

| File | Bytes | SHA-256 as fetched 2026-09-26 |
| --- | --- | --- |
| `wn3.1.dict.tar.gz` | 16 MB | `3f7d8be8ef6ecc7167d39b10d66954ec734280b5bdcd57f7d9eafe429d11c22a` |
| `mthesaur.txt` | 24 MB | `7c9742b1ed94435a893c0719b426725edb8a5242f8c526a75461bd6cee2dfd32` |

**A checksum here is a record of what was consulted, not a demand.** An
upstream file may legitimately change; if it does, say so rather than
pinning the project to a byte sequence it does not control.

## WordNet 3.1, for irregular inflection

**Princeton University.** `https://wordnet.princeton.edu/`. The licence is
permissive and BSD-shaped, requiring the copyright notice to travel with
redistribution. **That is why it is not vendored**: carrying it would put a
notice requirement inside a CC0 tree.

**What is used is `noun.exc`, `verb.exc` and `adj.exc`**, one line per
irregular form, the form first and its base second. 2,054 noun, 2,401 verb
and 1,490 adjective entries.

**Why it is worth the trouble.** Every irregular form this project got
wrong by hand is in those files: `thieves thief`, `farther far`, `lit
light`, `copied copy`. All four were found by reading 535 unused surface
forms one at a time, which is the most expensive way to find them.
`tools/check_inflections.py` compares the two tables instead.

**It is a reference and not an authority.** WordNet records what English
does. This project decides what a level admits, and the operator's rule
that archaic inflections need not be admitted means a mismatch is a
question. Measured 2026-09-26, all 22 forms WordNet has that level one does
not are archaic, British variants, homographs WordNet conflates, or optional
spellings, so all 22 are correctly absent.

**The check reads the part of speech from the filename**, because WordNet
lists `cupped` under verbs and this project admits `cup` as a noun only.
Keyed on the word alone it reported 89 non-gaps and buried the four real
ones.

## Moby Thesaurus II, for synonymy

**Grady Ward, placed in the public domain.** Project Gutenberg etext 3202,
`https://www.gutenberg.org/ebooks/3202`. 30,259 lines, comma separated, the
root word first and its synonyms after.

**Public domain, so it could be vendored and is not.** It is 24 MB of
material the repository does not need to carry, and the same fetch step
serves both references.

**Not yet used.** `curriculum/thesaurus.json` holds 927 hand-built senses
with 195 antonyms and 132 synonyms. Moby is a candidate for widening that,
and the shape of the problem is that Moby is keyed on words while this
project is keyed on senses, so an entry cannot be imported without deciding
which sense it belongs to.

## What was rejected, and why

**Wiktionary.** CC BY-SA. Share-alike is incompatible with redistributing
derived content as CC0, and prose written by a model that read a Wiktionary
entry is plausibly derivative.

**GCIDE.** GPL. The same problem in a different licence.

**Webster's Unabridged 1913.** Public domain and usable, but its
inflections are period-accurate rather than current, which is the opposite
of what an inflection table needs.

**Wikipedia, for seeding modules.** CC BY-SA, so the same objection, and
sharper: the proposal was to use article content as the substance of a
module rather than as a list of facts. **The distinction the project relies
on is that a word list extracted from a text is not the text**, and article
prose does not survive it. Using Wikipedia to decide *what a module covers*
is weaker ground for a derivative-work claim than using it as input to a
generator, but it remains the operator's judgement and is recorded as open.
