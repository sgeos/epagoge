<!--
Replace this block with a short summary of what the change does and why.
Reference a related issue with `Fixes #N` to auto-link.
-->

## Summary

<!-- One or two sentences. -->

## Type of change

- [ ] Corpus. A book, or a change to one
- [ ] Lexicon. A word, a sense, or a definition
- [ ] Tooling or library code
- [ ] Evaluation or measurement
- [ ] Documentation
- [ ] Maintenance. Continuous integration, packaging, process

## Checklist

- [ ] `./tools/check.sh` exits zero. Say so even if the disclosure scan reported a skip, which is expected in a clone
- [ ] Any figure quoted in the change was measured on this tree, or the same sentence says it was not
- [ ] No check was weakened to make this pass. If a check is wrong, the change says so and fixes it deliberately
- [ ] The contribution is the contributor's own work and carries no terms of its own

## For a corpus or lexicon change

- [ ] Every word used is already admitted at the book's level
- [ ] Every word defined reduces to the seed, and no definition closes a cycle
- [ ] The book fits its signature and its word band
- [ ] Front matter was built with `epagoge.book.book_head` rather than by hand

## Notes for the reviewer

<!--
Anything worth particular attention. Alternatives considered and rejected,
places where a second opinion would help, or a measurement you are unsure of.
-->
