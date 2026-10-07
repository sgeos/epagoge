# Brief

Opened 2026-10-07. The previous brief and condition are retained in
`evals/review/level_2_era_overlap/` as evidence of the taste-sense scope.

## Present goals

The level-two lexicon is the active goal. The verified baseline admits 966
distinct headwords through level two against an approximate target of ten
thousand. Level one is closed at 849. Later goals are level-two drafting,
schedules for later levels, expanded evaluation and the experimental
protocol. Confirmatory training remains blocked. Licensing, experimental and
later-schedule decisions remain with the operator.

The last four increments admitted one, four, two, three and two headwords.
Each reviewed a handful of hand-picked candidates through the local teacher.
That rate cannot approach the target, and none of those increments measured
why. The scan of 2026-09-27 had already produced a principled pool. Words
frequent in both the historical readers and the modern federal sources are
neither archaic nor narrowly technical. Of 194 such words, 47 were admitted
then and 139 surface strings remain unadmitted at level two.

## Recommended work

**One. Account for the whole remaining overlap pool.** Every one of the 139
strings receives a recorded decision with a reason. Admit a word when an
introductory definition can be written inside the level-two vocabulary and
grounds through the dictionary closure. Defer a word when its sense is
unclear, when it is a letter, fragment or proper noun, when it is an
inflection of another candidate, or when its only level-two sense would
need an operator decision. Record a missing inflection of an admitted word
as a form finding rather than a new headword.

**Two. Author directly rather than through the teacher for this batch.**
Host swap stood at 7.9 of 9.2 gigabytes with almost no free pages before
work began. That is the exhaustion condition recorded beside the teacher
context constant, and the teacher needs about eighteen gigabytes resident.
Agent-authored definitions are untrusted input exactly as teacher replies
are. They pass the same admission tool, the same vocabulary check and the
same closure check. They are labelled as agent-authored in every record.

**Three. Let the measurement tool account for an agent-authored batch.**
`tools/measure_lexicon_increment.py` refuses any batch without a teacher
generation report. It must accept a batch that declares it used no teacher,
while still refusing forged or inconsistent records. Tests cover the new
path and its failure modes.

**Four. Stop prompts from banning words the level admits.** The prompt
builder prints every substitution key as banned at every level. Twelve
keys are already admissible at level two and seven at level one. This batch
would add more, and a word the teacher is told never to write will not be
taught, which breaks the coverage rule. Filter substitutions by the level
being prompted, report keys that contradict their own level, and test both.

**Five. Record the result.** Measure the increment, preserve earlier
evidence and level-one books, update the handoff and changelog, run the full
gate and commit locally.

## Rationale and prior failures

The prior increments read as progress and measured no throughput. Selection
by hand produced candidates that defined each other, such as sugar and
sweet. A pool chosen by a stated criterion avoids that and is reproducible
from the scan report, whose hash is recorded.

**Sweet and sour are not attempted here.** They are sensory qualities of the
same kind as colours, which this lexicon grounds ostensively. The principled
route is an ostensive admission, which enlarges the seed. Enlarging the seed
changes what the dictionary claims about grounding, so it is recommended to
the operator rather than done.

## Wrong turns to avoid

Do not write a definition that is merely a synonym list or a list of
examples. Do not define two new words through each other. Do not choose a
sense because it is easy to define if it is not the sense the sources use.
Do not lower the level of a word already admitted higher, since that is an
authored decision with its own history. A distinct sense at level two is
permitted when it names a different concept.

Do not trust generated inflections. Review every form, especially of
irregular verbs, and mark mass nouns and periphrastic adjectives. Do not
write a count from arithmetic. Read it from the tool. Do not chain the gate
to the commit. Do not weaken a validator to admit a word. Do not alter prior
review evidence. Do not claim that this batch establishes a general
throughput, a curriculum benefit or semantic correctness beyond agent review.
Do not push without operator authorization for this scope.
