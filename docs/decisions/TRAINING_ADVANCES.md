# Training and architecture advances, and which of them reach this project

**Recorded 2026-09-27 after a literature spike, on operator direction.** The
question was what published work has moved the state of the art in training
machinery and architecture, and which of it is relevant here.

**Sources are vendored into ignored `tmp/references/papers/` under the rule
in `REFERENCE_SOURCES.md`, and listed at the end with checksums.** This
project's own measurements are marked as such; everything else is cited.

**This is a different spike from `CURRICULUM_LITERATURE.md`**, which asked
whether curriculum ordering works, and from `STRUCTURAL_TOKENS.md`, which
asked how a corpus announces its structure.

## The regime this project is actually in, which decides what transfers

**357,000 training tokens and 4.3 million parameters.** That is not a small
version of frontier pretraining. It is a different regime, and naming it is
what makes the literature searchable.

| | Frontier pretraining | This project |
| --- | --- | --- |
| Tokens | 10^12 to 10^13 | **3.6 × 10^5** |
| Parameters | 10^9 to 10^12 | **4.3 × 10^6** |
| Binding constraint | compute | **data** |
| Passes over the corpus | about one | **many** |

**The name for it is data-constrained, compute-abundant pretraining**, and
2026 has two papers on exactly it. That is the most useful thing this spike
found, and it was not what was searched for first.

## What reaches this project, in order of how cheaply

### 1. Weight decay, which was never chosen here

**`torch.optim.AdamW` was constructed with a learning rate and nothing
else**, so weight decay was 0.01 by inheritance. Nothing in the repository
said what it was, and no record chose it.

**Two independent sources say that is the wrong end of the range.**

A benchmark of optimizers across standardised pretraining scenarios reports
that a large decoupled term, 0.5 and above, significantly changes the final
loss and the ranking of optimizers, and that a moderate 0.1 is robust for
extended horizons. It singles out, by name, frameworks that omit weight
decay as a default non-zero hyperparameter, which is what happened here.

A study of the data-constrained regime finds optima far above standard
practice of 0.1, rising with model size: 0.4 at 72M parameters, 0.8 at
140M, 1.6 at 257M and 664M, and 3.2 at 1.4B. **At 257M on 100M tokens it
reports validation loss falling from 3.88 to 3.42.**

**This project has the symptom those papers treat, but only sometimes, and
that was measured rather than assumed.** On the 400-book corpus at 800 steps
and width 256 the training-to-held-out gap is 0.127, which is not
overfitting at all. At width 512 and 3,200 steps it is 1.366, and held-out
loss has turned upward. **The symptom is a function of width and duration,
not a property of the project**, and the sweep below is what established
that.

### 2. The learning-rate floor, which sits exactly on the boundary

**`min_lr_fraction` is 0.1** and the benchmark's eighth takeaway is that
decaying further than 10 percent of the maximal significantly improves
results, with the best final rate differing by scheduler. This project is
sitting on the value the finding says to go below.

### 3. Augmentation for many passes over a fixed corpus

A 2026 study trains a 150M model for **100 epochs on 75M tokens**, about 40
times below the Chinchilla-optimal budget, which is the closest published
setting to this project's and still 200 times more data.

**The baseline overfits exactly as this project does**, reaching minimum
validation loss 4.015 at epoch 16 and degrading monotonically after it.

| Intervention | Minimum validation loss |
| --- | --- |
| Baseline | 4.015 |
| Random token replacement, 15 percent | **3.841** |
| Exponential target offset, i at most 5 | 3.870 |
| Right-to-left, 50 percent | 3.910 |
| Masking | 3.910 to 3.923 |
| Fill-in-the-middle, 50 percent | 3.947, no benefit |
| **Random 5 percent, right-to-left 50, exponential offset** | **3.805** |

The best combination is 0.210 absolute and 5.2 percent relative below
baseline. **Random replacement beats masking** because a replaced token is
plausible but wrong, which forces harder disambiguation. Fill-in-the-middle
diverges too far from the evaluation distribution to help.

### 4. Masked-input regularisation

An auxiliary next-token loss on a randomly masked copy of the input, added
to the ordinary loss. It costs a second forward pass and changes nothing at
inference. Reported gains are small in loss, 0.006 at 72M to 0.03 at 1.4B,
and the authors convert them to **about 1.3 times more unique data** under
their own scaling law.

## What does not reach this project, and why that is worth writing down

**Muon and its descendants.** `TRAINING_TECHNIQUES.md` already adopted Muon
and none of it is implemented, and the 2026 literature has moved on to
variants. But the benchmark above finds **AdEMAMix consistently ahead**, and
finds that several methods beat AdamW only at large batch sizes. This
project trains at batch 8 to 16. **A large-batch result does not transfer to
a small-batch setting**, and the benchmark says so directly.

**Newton-Schulz attention** is parameter-free, reduces leading-eigenvalue
concentration and increases effective rank, which is the quantity
`JACOBIAN_SPACE.md` sets a floor on. **It is measured on vision only**, ViT
and Swin over CIFAR-10 and CIFAR-100, with mean gains of 0.25 to 0.83
percentage points of accuracy and an inference latency cost. There is no
language-model result. It is recorded because it is the first thing found
that targets this project's own stated architectural quantity, and it is not
adopted because nothing has shown it does anything for language.

**Grouped-query attention** reduces the key-value cache, which is an
inference-memory problem this project does not have.

**Mamba-style architectures** are reported to outperform transformers of
similar size at lower cost. **The ablation forbids following that**, because
`MODEL_ARCHITECTURE_CONSTRAINTS.md` requires comparability with published
work and the curriculum experiment needs the architecture held fixed. Noted
and not pursued.

**SoftQ**, a five-parameter scaling law proposed to replace Chinchilla in
data-constrained settings. Relevant in principle and unusable here, because
fitting a scaling law needs a grid this project has not run.

## What the spike did not find, which is itself a result

**Nothing was found that measures any of this below about 70M parameters.**
The closest settings are 72M and 150M parameters, against 4.3M here. Every
number above is therefore an indication of direction and not a prediction of
magnitude, and adopting any of it on the strength of the citation alone
would be the failure this project records elsewhere as elegance not being
evidence.

**So each item is implemented as an option at its current value and
measured**, which is the same discipline `dropout`, `norm`, `feed` and
`positions` are already held to.

## What was changed

1. **`TrainConfig.weight_decay` exists and is passed to the optimizer.** It
   was previously inherited from torch and invisible. The default is
   unchanged at 0.01 so that the measurement, not this record, decides.
2. **`min_lr_fraction` carries the finding in its docstring**, unchanged.
3. **`tools/diagnose_level.py` takes `--weight-decay` and
   `--min-lr-fraction`**, so both can be swept on the real corpus.

**Not implemented, and each would be a real change rather than an option**:
token-replacement augmentation, right-to-left and offset objectives,
masked-input regularisation, and any optimizer other than AdamW.

## Measured here

**A weight-decay sweep on the 400-book corpus at rotary positions**, over
two widths, three durations and two values, then three paired seeds at the
one cell that mattered. Full figures are in
`../../evals/pilot/LEVEL_ONE_REGULARISATION.md` rather than here, so this
record stays a statement about the literature and that one stays a statement
about this tree.

**The literature's claim is conditional and the condition is measurable.**
Raising weight decay from 0.01 to 0.5 **lost in five of six cells and won in
the sixth**, and the sixth is the only cell where the model was overfitting.
At width 512, held-out loss under the inherited default goes 3.311, 3.059,
then 3.066, turning upward between 1,600 and 3,200 steps. Under 0.5 the same
points are 3.331, 3.079, 3.009, still falling. At that cell weight decay
wins in three of three paired seeds by a mean of 0.055 nats.

**So a recommendation to raise weight decay by default would have made this
project worse**, at the setting it actually trains at, and better at the
setting it would reach by training wider or longer. **The default is
therefore unchanged and the flag exists.** The decisive cell was chosen
after seeing the first sweep, which the evaluation record states as a
weakness of the design rather than leaving to be noticed.

## Sources, fetched 2026-09-27

| File | SHA-256 | Source |
| --- | --- | --- |
| `optbench_2509.01440.pdf` | see `tmp/references/papers/SHA256SUMS` | `https://arxiv.org/abs/2509.01440` |
| `dataconstrained_2606.06888.pdf` | same | `https://arxiv.org/abs/2606.06888` |
| `augmentation_2606.16246.pdf` | same | `https://arxiv.org/abs/2606.16246` |

- Semenov and others, *Benchmarking Optimizers for Large Language Model
  Pretraining*, 2025.
- *Data-Constrained Language Model Pretraining: Improved Regularization and
  Scaling Laws*, 2026.
- *Demystifying Training-Time Augmentation for Data-Constrained Language
  Model Pretraining*, 2026.
- *NS-Attention: Newton-Schulz Transformations of Attention Outputs in
  Vision Transformers*, 2026, `https://arxiv.org/abs/2609.27735`.
- Liu and others, *Muon is Scalable for LLM Training*, 2025,
  `https://arxiv.org/abs/2502.16982`.
