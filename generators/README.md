# generators/

The corpus synthesis pipeline. Executable stages that produce records for
`corpus/` from the specifications in `curriculum/`.

**Status.** Empty. No generator has been written.

## Trust boundary

This directory is where untrusted input enters the system. Output from a
teacher model is untrusted by the same standard as any external input.
Every record must be validated against a declared schema before it reaches
`corpus/`, and a record that fails validation must be rejected loudly
rather than repaired silently.

A synthetic corpus inherits the errors and the dispositional biases of
whatever model generated it. The verification layer is the only thing
standing between a teacher model's confident error and the trained model's
confident error, so it is a primary component rather than a convenience.

## Teacher

Chosen and pulled 2026-09-24. See `TEACHER.md`.

## A prompt must carry the concept boundary

Established by the first two generations attempted. Asked to teach that
repeated use wears things out, the model returned sentences about things
breaking and chains snapping, which is sudden failure and a different
concept that the graph deliberately separates.

One negative constraint fixed it.

**A generation prompt therefore supplies the concept, its grounding
primitive and observation, and its nearest graph neighbours as explicit
exclusions.** The graph holds the neighbours already, so exclusions are
derived rather than authored.

The failure this prevents is the expensive kind. Fluent text that blurs the
distinction the curriculum exists to draw, passing schema validation and
reading well, catchable only by a human reading one record at a time.

## Open constraint

The verification layer that rejects unsupported claims is specified in
`docs/decisions/OPEN_QUESTIONS.md` item two and is not yet implemented.
