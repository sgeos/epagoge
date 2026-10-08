# AGENTS.md

Guidance for automated agents working in this repository.

The authoritative instructions live in [`CLAUDE.md`](CLAUDE.md). Read that
file first. It is agent-agnostic in content despite its name.

## Starting a session in Codex or Grok Build

**Current state is in [`docs/process/HANDOFF.md`](docs/process/HANDOFF.md)**,
and [`docs/process/RESUME_PROMPT.md`](docs/process/RESUME_PROMPT.md) is the
prompt a new session should be given. Both are written for any agent.

Checked on 2026-10-07 against the help output of the installed tools, Codex
CLI 0.160.1 and Grok Build 1.0.46. Codex reads this file. Grok Build's
bundled documentation says it reads this file and `CLAUDE.md`. Recheck the
flags if either tool has been upgraded.

    codex --cd /Users/bsechter/projects/python/epagoge \
      --sandbox workspace-write --ask-for-approval on-request \
      "Read docs/process/RESUME_PROMPT.md and carry out its instructions."

    grok --cwd /Users/bsechter/projects/python/epagoge --sandbox workspace \
      "Read docs/process/RESUME_PROMPT.md and carry out its instructions."

### What a sandboxed agent needs

**Network access is not needed for normal work.** Measured on 2026-10-08,
the full gate passes inside Codex's `workspace-write` sandbox, whose network
is off, and inside Grok Build's `workspace` sandbox. Use the most restrictive profile that allows writes to this
directory: `workspace-write` in Codex and `workspace` in Grok Build.

| Need | Used by | Grant it when |
| --- | --- | --- |
| Write the workspace | All work | Always |
| Loopback `127.0.0.1:11434` | Teacher, every generator | Only for a session that generates |
| Network and git credentials | `git push`, `gh` | Only to publish, or leave it to the operator |

**The gate falls back to an offline environment check inside a sandbox.**
uv 0.9.5 cannot run where writes are confined to the workspace. It fails to
write its cache marker in the home directory, and with a cache inside the
workspace it panics reading the macOS proxy configuration. `tools/check.sh`
therefore falls back to `tools/check_environment.py`, which checks the
installed environment against `uv.lock` by reading files, but only for those
two failures. Any other uv failure, such as a stale lock, still stops the
gate. The gate also keeps its scratch files under the ignored `tmp/`, since
the default macOS temporary directory is outside the workspace. Continuous
integration always runs the real `uv sync`.

**Observed in trial sessions on 2026-10-08.** Codex loaded `AGENTS.md` at
startup. Grok Build loaded `AGENTS.md` and `CLAUDE.md`. Neither loaded
`HANDOFF.md` without being asked, which is why the resume prompt names it.
Both ran the handoff validity checks and the full gate successfully and made
no edits.

`.codex/` holds host-specific Codex settings and is ignored rather than
tracked.

## What runs in a fresh clone, and what needs the authoring host

**Added 2026-09-28 for a handoff to a different agent.** Four things this
project uses are deliberately not in version control, so a clone has the
repository and not the workshop.

| Absent from a clone | Why | What it blocks |
| --- | --- | --- |
| `evals/pilot/*.pt` | Reproducible from the corpus and a seed | `talk.py`, `elenchos.py`, `retention.py` until a checkpoint is trained |
| `tmp/` | Scratch, including the vendored scan sources | `scan_lexicon.py` until the sources are re-fetched |
| `corpus/` | Derived, rebuilt by `build_corpus.py` | Nothing. Rebuild it |
| `secret/` | Never tracked | The disclosure scan, which then skips loudly |

**The teacher model is local and is not a dependency a clone can install.** It
is named in `generators/TEACHER.md` and served over Ollama on the authoring
host. **Every generator needs it** and none of them will run without it.

**Training needs the optional dependency group** and a device. The figures in
`evals/pilot/` were measured on Apple Metal; a run elsewhere will not reproduce
them bitwise, which `CLAUDE.md` already states as a standing obligation rather
than a surprise.

### What this leaves fully available

**The gate, and everything it checks.** Lint, formatting, strict type checking,
the tests, the coverage floor, and every graph, corpus, schedule, book, closure
and thesaurus validation. **Continuous integration runs exactly this and is
green**, which is the proof that the tree validates without the workshop.

**All lexicon and curriculum work that does not need the teacher**: judgement
on candidates, concept assignment, schedules, specifications and decision
records.

### One obligation a clone cannot discharge

**`CLAUDE.md` requires reading the code-name discipline before writing tracked
prose, and that document is inside `secret/`.** An agent without it cannot
check its own writing against the rule it is being asked to follow, and the
disclosure scan that would catch a mistake skips for the same reason.

**This is the operator's call and is flagged rather than worked around.** The
options are to supply `secret/` to the environment, to leave tracked prose to
an agent that has it, or to accept the exposure knowingly.

## Summary of the obligations that matter most here

- The curriculum-ordering benefit is a hypothesis under test, never a
  premise. A flat-order control is required before attributing any gain to
  ordering.
- Disagreeableness is not a proxy for correctness. The target property is
  evidence-conditioned assent.
- Teacher-model output is untrusted input. Validate at the generator
  boundary and reject loudly.
- Run-to-run determinism is not available on graphics processing units
  under either candidate framework. The ordering ablation needs multiple
  seeds per condition and a declared effect threshold. A single-run
  comparison establishes nothing.
- The training framework is undecided. Do not assert PyTorch or JAX as
  chosen.
- Unmeasured claims are marked as unmeasured, in the same sentence.
- The specification is incomplete. See
  [`docs/decisions/OPEN_QUESTIONS.md`](docs/decisions/OPEN_QUESTIONS.md)
  before writing pipeline code.
