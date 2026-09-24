# Positioning for recruitment into collaborative groups

**Decided 2026-09-23.** The model class is positioned to be attractive for
recruitment into multi-agent groups, as the falsifier and verifier
specialist.

## The mechanism is deployed, not speculative

Verified 2026-09-23.

- Multi-agent frameworks name **recruitment as an explicit agent role**
  alongside decision-making and evaluation, with at least one framework
  focused specifically on adaptive agent recruitment.
- Emergent collaboration frameworks operate with low human supervision,
  where developers define high-level goals and agents coordinate in natural
  language from the bottom up.
- The Agent2Agent protocol provides **Agent Cards**, JSON documents
  advertising an agent's skills, which a client agent uses to identify and
  negotiate with the most appropriate remote agent for a task. Cards are
  published to registries queried by skill, tag, or capability.
- The dominant pattern is orchestrator-plus-specialists, where an
  orchestrator polls a registry and integrates newly discovered agents
  automatically without configuration changes.

Recruitment by a model, of a model, through a machine-readable capability
advertisement, is therefore a protocol with an installed base.

## This is repositioning, not a new direction

The properties that make the model attractive for recruitment are the ones
already decided for other reasons. The mapping is close to one-to-one.

| Existing property | Recruitment value |
| --- | --- |
| Evidence-conditioned assent | Fills the verifier seat generalists cannot fill |
| Measured residual error rate, question two | A credential an orchestrator can select on |
| Structured output schema, question nine | Exactly what Agent Cards and A2A consume |
| Auditable provenance | Contributions are checkable by the group |
| Small and resource-bounded | Cheap to include in an ensemble |

**The role is the falsifier seat in a group of generalists.** Multi-agent
systems have a documented weakness in consensus collapse, where members
converge on agreement including when wrong. A member that resists consensus
pressure is the complement to that failure rather than a nuisance within
it.

## The objection, and the mitigation

**Selection pressure may run against the property.** If a recruiting
orchestrator is itself agreeable and optimises for smooth collaboration, a
disagreeable specialist is plausibly dispreferred. Recruitment follows only
where selection is outcome-driven rather than affinity-driven.

**Mitigation. Advertise outcomes, never disposition.** The Agent Card
states a measurable contribution, such as the rate at which unsupported
claims are flagged, evidenced by the expert-audited residual error rate. It
does not describe the model as disagreeable, sceptical, or contrarian.

This gives the measured error rate a second job. It was scientific hygiene.
It is now also the recruitment credential, and it is a number an
orchestrator can select on.

## THE GUARD. Never train toward being selected

Recruitment attractiveness is a **positioning and interface concern, not a
training objective.**

Optimising for selection means optimising for whatever current
orchestrators favour, and what they currently favour is agreeableness. That
would destroy the property the model exists to have, by the most direct
route available.

This is the same discipline as measurement-not-intervention in
`JACOBIAN_SPACE.md` and carries the same force. Positioning may change the
Agent Card, the output schema, and the documentation. It may not change the
loss.

## Requirement this adds

**Input from other agents is untrusted.** Agent protocols are a live attack
surface, with published work on prompt injection and protocol exploits in
agent workflows. The project already treats teacher-model output as
untrusted at the generator boundary. The same standard applies to anything
arriving from a collaborating agent, and it is not optional for a model
class intended to be recruited by parties it did not choose.

Trust-boundary treatment belongs in the output-schema specification
alongside the structured format from question nine.

## Consistency with the headline framing

The verifier-specialist framing is a good public face. It is true, it is
the valuable thing, and it is what the Agent Card should say. It satisfies
the project's headline-framing rule rather than straining against it.

## Open

- Whether to publish an Agent Card and to which registries. Downstream of
  the gated follow-on, since there is no model yet.
- What measurable contribution the card advertises, which depends on the
  elenchos suite and the audited error rate both existing.

## Sources consulted 2026-09-23

- Agent2Agent protocol, agent discovery,
  https://a2a-protocol.org/v0.2.5/topics/agent-discovery/
- Agent2Agent protocol repository,
  https://github.com/a2aproject/A2A
- Multi-Agent Collaboration Mechanisms, a survey,
  https://arxiv.org/pdf/2501.06322
- Emergent Intelligence in Multi-Agent and LLM Systems,
  https://www.techrxiv.org/doi/10.36227/techrxiv.177092236.62657640
- From Prompt Injections to Protocol Exploits, threats in LLM-powered
  agent workflows, https://arxiv.org/pdf/2506.23260
