# Teacher model

**Pulled 2026-09-24.** `qwen3:30b-a3b-instruct-2507-q4_K_M`, run locally
through Ollama.

| Property | Value |
| --- | --- |
| Architecture | Sparse mixture of experts, 30.5B total |
| Licence | **Apache 2.0**, confirmed from the shipped licence |
| Quantisation | Q4_K_M |
| Context | 262,144 |
| Resident size | 21 GB, 100 percent on GPU |
| Warm throughput | ~37 words per second, roughly 50 tokens per second |

**Text-only rather than the vision variant**, because corpus generation
uses no vision and the parameters would be dead weight. **Instruct rather
than thinking**, because reasoning traces are wasted tokens for bulk
generation.

Selected under the rule in open question two: a specifically named MIT or
Apache checkpoint, run locally so that nothing leaves the machine. See that
entry for why hosted interfaces are excluded, which is disclosure rather
than licensing or cost.

## Generation budget, revised

At roughly fifty tokens per second single-stream, one million tokens is
about five and a half hours, improving several-fold under concurrency. Level
one at one to ten million tokens is therefore a few hours to a day or so,
better than the earlier estimate of up to eighty hours.

## The finding from the first two prompts, which shapes the generator

**A prompt must carry the concept boundary, including what the concept is
not.** Adjacent concepts are conflated otherwise.

Asked to teach that repeated use wears things out, the first attempt
returned three sentences of which two taught the wrong thing.

> When you use a toy over and over, it gets broken.
> If you keep pushing the swing too hard, the chain will snap.
> Things get old and stop working if you use them too much.

Breaking and snapping are **sudden failure**. The concept graph separates
`wearing_out` from `things_break` precisely because they differ, and level
one is where that distinction has to be established rather than blurred.

Adding one negative constraint, that the content is not about sudden
breaking, produced three sentences of which all three were correct.

> When you draw with a crayon a lot, the crayon gets shorter.
> If you push the swing every day, the rope gets a little looser.
> Little changes happen each time you use something, and soon it's
> different.

**Requirement this establishes.** A generation prompt supplies the concept,
its grounding primitive and observation, **and its nearest neighbours in the
graph as explicit exclusions.** The graph already holds the neighbours, so
the exclusions are derived rather than authored.

Without that, the generator produces fluent text that blurs exactly the
distinctions the curriculum exists to draw, and it does so in a form that
passes schema validation and reads well. That is the failure a human
reviewer would have to catch one record at a time, which is the expensive
way to catch it.
