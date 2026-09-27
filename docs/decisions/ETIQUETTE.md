# Salutations, valedictions, and etiquette, and where they belong

**Raised 2026-09-27 by the operator**, after the model was given `hello` and
`hi` and reported both as outside the level. The operator's position is that
salutations, valedictions and general etiquette ought to exist somewhere in
the curriculum, being general communication skills.

**They exist nowhere today.** Checked against the whole lexicon at every
level, not only level one.

| Word | Where |
| --- | --- |
| `yes`, `no`, `not` | **core**, already admissible |
| `please`, `thank`, `thanks`, `sorry` | absent at every level |
| `hello`, `hi`, `goodbye`, `welcome`, `polite` | absent at every level |

**`hello` and `hi` also encode identically.** Both fall outside the lexicon
and become one `<unk>` token, so the model receives the same one-token
prompt for either and, at a fixed seed, returns the same continuation. That
is the tokeniser behaving correctly and it is worth knowing before reading
anything into the answers.

## Why the domain set has no home for them

**Every domain in the set is organised around claims.**
`institutional_interfacing` contests claims about what is,
`normative_adjudication` settles claims about what ought to be,
`compressed_communication` conveys a claim when the whole of it cannot be
conveyed, `record_keeping` asks whether a record is faithful.

**A greeting is not a claim.** Its function is phatic. It opens a channel
and a valediction closes one, and neither asserts anything that could be
true or false. So the gap the operator found is real and it is structural
rather than an oversight in authoring.

## The placement, and why it is not a widening

**Recommended home is `institutional_interfacing`, with its scope record
amended explicitly rather than quietly stretched.**

`INSTITUTIONAL_INTERFACING.md` warns that the unbounded version of this
domain teaches the opposite of the property the project targets, so
admitting anything to it needs an argument that the admission serves the
activity rather than merely fitting beside it.

**The argument is that etiquette is the register in which the domain's four
moves are performed.** That record specifies assent, attack, defence and
concession. Each has a courteous form and a rude one, and the difference is
exactly the distinction `CLAUDE.md` insists on, between evidence-conditioned
assent and a dispositional bias toward contradiction. **A model that attacks
an unsupported claim rudely has failed the domain, not passed it.** So the
courteous register is not adjacent to the four moves. It is how they are
executed without inverting into the failure the domain exists to avoid.

**The bound that keeps this from becoming general social skills.** What is
admitted is opening and closing an exchange, and the forms that soften a
move without weakening it. What is not admitted is friendship, manners as
social ritual, or the wider culture of politeness, none of which serves
claim evaluation.

## The connection to structural tokens, which is not a coincidence

**A salutation and a valediction do for a human reader what a turn marker
does for a tokeniser.** `STRUCTURAL_TOKENS.md` records that Llama 3 marks
turns with `<|start_header_id|>` and `<|eot_id|>`, and that what a reader
uses is the presence of an announcement rather than its spelling.

**A greeting is the human-readable form of the same boundary function.** So
etiquette vocabulary and conversational turn structure are one design
question rather than two, and they should be settled together when the
corpus first carries an exchange between two parties. Nothing at level one
does.

## What is proposed, and what is deferred

**Proposed concepts**, to be authored into
`curriculum/graph/concepts.json` under `institutional_interfacing`:

- `greeting_and_parting`, opening and closing an exchange.
- `asking_politely`, the softened form of a request.
- `thanking`, acknowledging what another party supplied.
- `apologising`, which is distinct from conceding a claim and must not be
  taught as its synonym, since conceding is evidence-conditioned and
  apologising is not.

**Deferred, and these are the operator's.**

1. **The level.** Greeting is among the earliest language a child meets,
   while the institutional register is late. The natural split puts the
   words and the phatic acts at level one and the register above it, which
   would make this domain span the widest level range in the scheme.
   `LEVEL_CALIBRATION.md` is the constraint.
2. **Whether `apologising` is admissible at all** in a project about
   calibrated assent. An apology offered under social pressure is very close
   to the failure `evals/elenchos/` exists to detect.
3. **The words themselves.** Admitting `please`, `thank`, `sorry`, `hello`
   and `goodbye` at level one means each needs a definition in a book,
   because closure is enforced and a word without one breaks it. That is
   generation work and it follows the decision rather than preceding it.

**Nothing is added to the graph or the lexicon by this record.** Both are
the operator's, and this states the case and the bound so that the decision
can be taken on them rather than on a fait accompli.
