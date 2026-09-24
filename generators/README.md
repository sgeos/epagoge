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

## Open constraint

The teacher model has not been chosen, and the verification layer that
rejects its unsupported claims has not been designed. Both are recorded in
`docs/decisions/OPEN_QUESTIONS.md`.
