# Model architecture

**Specified 2026-09-23. Nothing is implemented.**

Two architectures, because the ablation subject and the deployment artifact
are separate artifacts. See `../decisions/OPEN_QUESTIONS.md` item 15a.

## Ablation model

Fully standard, with no deviation.

- Dense decoder-only transformer
- Pre-normalisation with root mean square normalisation
- Gated feedforward activation
- Rotary position embeddings
- Grouped-query attention
- No bias terms

Deviating here costs comparability against published curriculum-ordering
work, and that comparability is what the project's central experiment
depends on. The architecture is not the subject of the experiment and must
not become a second variable in it.

## Deployment model

The same, plus bounded attention. See the section below.

## Frontier divergences, evaluated against this project's constraints

The dominant 2026 frontier pattern is sparse mixture-of-experts, described
as the clearest capacity-scaling pattern because it decouples total
parameters from active per-token computation. Hybrid architectures
alternating attention with state-space layers are also shipping, Nemotron 3
alternating attention with Mamba-2 layers. Dense transformers nonetheless
remain the stated reference architecture for language and multimodal
reasoning. Verified 2026-09-23.

Those choices optimise against datacenter serving economics and
training-compute efficiency, where memory is abundant, power is purchased,
and the scarce resources are training arithmetic and serving throughput.
Those are not this project's constraints.

### Mixture of experts. Rejected, and the case is closed

Two independent decisive arguments.

**The bargain is inverted.** Mixture of experts buys compute efficiency by
spending memory. All experts must be resident while only a few activate per
token, so the full memory price is paid for a compute discount. The binding
constraint here is memory on the deployment target, which makes this
exactly the wrong trade. Streaming experts from slower storage would
restore the memory saving at the cost of unbounded latency, defeating the
worst-case execution bound.

**Routing is data-dependent control flow.** A corrupted activation reaching
a router selects a wrong expert rather than producing a slightly wrong
number. See `../decisions/MODEL_ARCHITECTURE_CONSTRAINTS.md`.

### State space and linear attention hybrids. Rejected, with regret

The appeal is real. These are attention-budgeting architectures that
replace a growing key-value cache with a fixed-size recurrent state, and
bounded memory regardless of sequence length is precisely what a worst-case
memory requirement wants.

**The objection is specific to the fault environment.** Recurrent state
is cumulative and persistent. A single bit flip in it contaminates every
subsequent output, because the corrupted state is carried forward into
every following update. Key-value cache corruption is bounded in blast
radius by comparison, distorting one token's contribution to attention
rather than poisoning a recurrence. Replacing a distributed fault surface
with a concentrated cumulative one is a bad trade even when it saves
memory.

A plain capability finding points the same way, in work titled
sliding-window beats linear attention.

### Long chain-of-thought reasoning. Deferred, with a flagged interaction

Relevant to the project's purpose and hostile to the deployment target.
Many autoregressive steps mean more cache, more time, more bit-flip exposure
exposure per answer, and more opportunity for a single corrupted token to
derail a chain that cannot be checked. This is a post-training concern and
is recorded here only so the interaction is not discovered late.

## The one deviation the constraints justify. Bounded attention

Sliding-window or hybrid local-global attention. Verified 2026-09-23, it
reduces key-value cache memory complexity from order N to order C, constant
in sequence length rather than growing with it, and per-token cost from
order S to order w.

**This is not an efficiency optimisation here.** It converts an unbounded
quantity into a statically bounded one, which is the property the adjacent
statically bounded execution work treats as the entire point. Frontier labs
adopt it to serve more users per accelerator. This project would adopt it
in order to be able to state a worst-case memory bound at all. Same
mechanism, different and better-motivated reason.

**The cost, stated rather than glossed.** Pure sliding-window attention
loses long-range dependency. The practical form interleaves a few
full-attention layers to recover it, and those layers reintroduce unbounded
cache growth. The choice is therefore a real trade between a complete
static bound and long-range capability.

**Unresolved.** Where to set that trade depends on how much context the
deployment task needs, and the deployment task is not specified. Recorded
as open question sixteen.

## On diverging from the frontier

Frontier architecture is specialised toward abundant memory, purchased
power, and serving throughput. This target has none of those. Divergence
under materially different constraints is correct specialisation rather
than a lag, and the frontier choice that diverges most, mixture of experts,
is the one whose bargain these constraints invert. Matching frontier
architecture on the deployment target would be the thing worth
questioning.

## Sources consulted 2026-09-23

- Emerging architecture trends in 2026 open-weight models,
  https://emredeveloper.medium.com/2026-open-weight-ai-models-new-architecture-trends-035c2c2bd659
- The evolution of mixture-of-experts architectures,
  https://arxiv.org/pdf/2608.08650
- Sliding-window beats linear attention,
  https://arxiv.org/pdf/2608.28444
- You Only Cache Once, decoder-decoder architectures,
  https://arxiv.org/pdf/2405.05254
