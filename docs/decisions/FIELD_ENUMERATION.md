# A record built from a subset of its own dataclass's fields

**Recorded 2026-09-27, after the fourth instance.** Three were found in the
book code on 2026-09-26 and the fourth in the checkpoint code the next day.
The shape is always the same. A dataclass gains a field, and somewhere else
a function rebuilds that dataclass or serialises it by naming its fields one
at a time. The new field is not in the list, nothing fails, and the record
is quietly written or read without it.

**The remedy is always the same too.** Derive the field list from
`dataclasses.fields` rather than retyping it, and test that every field
survives a round trip at a value that is not its default. A round trip at
default values passes by coincidence, because an omitted field comes back as
the default it was never given.

## The four instances

| Where | What it enumerated | What was lost |
| --- | --- | --- |
| `describe_books` | 7 of `Book`'s 12 fields | `form`, on 17 question books |
| `books_from_json` | 6 of 12 | every field it did not name |
| `generate_books` front matter | 4 of 12 | the rest, on every new book |
| `save_checkpoint` | 5 of `ModelConfig`'s 10 | `n_heads`, `dropout`, `norm`, `feed`, `tie_embeddings` |

The three book instances are in `src/epagoge/book.py` and
`generators/generate_books.py`, and `tests/test_book.py` now walks
`dataclasses.fields(Book)`. The fourth is in `src/epagoge/pilot.py`, and
`tests/test_pilot.py` walks `dataclasses.fields(ModelConfig)`.

## Why the fourth is worse than the first three

**A book is read by a person and a checkpoint is read by a machine.** A book
missing a field is visible to anyone who looks at it. A model rebuilt from a
config missing a field is a different model that reports no error.

**Measured 2026-09-27 by dropping each field from a written checkpoint in
turn.** Two of the five omissions are loud and three are silent.

| Field | Omitted | Why |
| --- | --- | --- |
| `norm` | **Loud** | RMSNorm carries different parameter names |
| `feed` | **Loud** | SwiGLU has three matrices where GELU has two |
| `dropout` | Silent | No parameters, and inactive in evaluation |
| `tie_embeddings` | Silent | Every tensor still fits |
| `n_heads` | Silent | Every tensor still fits |

**`n_heads` is the sharpest of them.** Written at two and read back as four,
the model loads without complaint and splits attention differently than it
was trained to. No shape check can see that, because the shapes are right.

**`tie_embeddings` is the one that bit.** Under tying the output head and the
input embedding are one storage, so an untied checkpoint holding two
different matrices loads with one overwriting the other. The level-one
checkpoint of 2026-09-26 holds two matrices differing by 4.58, so this was
live rather than hypothetical. `verify_loaded` in `src/epagoge/pilot.py`
compares the model against the checkpoint after loading and raises, and it
was shown failing on exactly that pair before being kept.

## What made it visible, and it was luck

**An unrelated rename is what turned a wrong model into an exception.** The
two position paths were unified into one `Block` on 2026-09-26, which
renamed the module attribute from `rotary_blocks` to `blocks`, so the
checkpoint stopped loading at all. Without that, `tools/talk.py` would have
answered from a model whose embedding had been overwritten by its output
head, and nothing would have said so.

**No recorded measurement is contaminated, and the reason is that a crash
cannot produce a number.** Every tool that reads a checkpoint raised from
the moment of the rename, so anything that produced a figure ran before it,
when the loader and the checkpoint agreed. `docs/process/HANDOFF.md` lists
three measurements owed for unrelated reasons.

## The rule

**A serialised record must be able to say what it does not carry.** Where a
field is absent, the reader fills it from what it meant when the record was
written, never from what it defaults to now, and refuses where no historical
value exists. `LEGACY_MODEL_DEFAULTS` in `src/epagoge/pilot.py` is that
table for checkpoints, and adding a field to `ModelConfig` without adding it
there makes every checkpoint on disk refuse loudly rather than reload as
something else.
