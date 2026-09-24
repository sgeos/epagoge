# Python interpreter version

**Resolved 2026-09-23 by measurement.** The floor stays at `>=3.12` in
`pyproject.toml`. Python 3.14 is not a blocker, so the system interpreter
at 3.14.7 may be used.

## Measurement

Queried against the Python Package Index on 2026-09-23.

| Package | Version | requires-python | CPython wheels published |
| --- | --- | --- | --- |
| torch | 2.14.0 | >=3.10 | cp310 cp311 cp312 cp313 cp314 |
| jax | 0.11.2 | >=3.12 | source distribution |
| jaxlib | 0.11.2 | >=3.12 | cp312 cp313 cp314 cp315 |
| mlx | 0.32.2 | >=3.10 | cp310 cp311 cp312 cp313 cp314 |

## Conclusion

The concern that prompted this record, namely that machine learning wheel
availability would lag the 3.14 release, did not materialise. Both
candidate framework stacks publish 3.14 wheels.

The floor remains 3.12 rather than 3.14 because nothing requires 3.14 and a
lower floor costs nothing.

## Residual flag

Flax 0.12.9 advertises only 3.12 in its trove classifiers. Classifiers are
declarative and frequently stale, so this is weak evidence rather than a
demonstrated incompatibility. Verify by resolution rather than by
classifier if the JAX path is taken.

## Supersedes

The earlier open state of this record, which set the floor at 3.12 pending
verification and blocked the first dependency addition. That block is
lifted.
