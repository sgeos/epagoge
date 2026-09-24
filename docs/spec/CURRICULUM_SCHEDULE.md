# Curriculum schedule

What gets written at a level, in which domain, against which concepts, and
under what token budget. Implemented in `../../src/epagoge/schedule.py` and
gated by `../../tools/validate_schedule.py`.

## What it is for

**The schedule is where a concept gets its level.**

Before it existed the assignment was implicit in whichever records happened
to be written, so an ordering mistake could only be found after generating
the record that contained it. The schedule applies the same prerequisite
rule the corpus validator applies to records, lifted from written records
to the plan, which makes an ordering mistake cheap to find rather than
expensive.

It is also the artifact a generator reads. It is data, not prose.

## Shape

A level is one file. `curriculum/schedule/level_NN.json`.

```
level          the level this file schedules
token_budget   low, high, and the basis for the range
covers         the domains this level schedules
domains        a plan per covered domain, each holding units
notes          why this level is shaped as it is
```

A unit is one teaching target.

```
id             stable identifier
form           the level-appropriate register, in one or two sentences
teaches        concepts already in the graph
introduces     concepts this unit will create, not yet in the graph
primitives     register entries the unit grounds in
```

## Teaches against introduces

**This split is what lets a schedule plan ahead without breaking the rule
that the graph follows content.**

A concept in `introduces` is a plan. It is visible as a plan, it is checked
for not already existing, and it does not become a node until a record
teaches it. A concept in `teaches` already exists and is checked for
belonging to the domain it is scheduled under.

Without the split the choice would be between a graph full of concepts no
record teaches, or a schedule that cannot mention anything new.

## Rules the validator enforces

1. Every covered domain is declared in the graph and has a plan, and every
   plan is for a covered domain.
2. A `teaches` concept exists in the graph and belongs to its plan's domain.
3. An `introduces` concept does **not** exist in the graph.
4. No concept is scheduled twice, in any unit of any domain.
5. Every cited primitive is in the register.
6. **Every prerequisite of a taught concept is scheduled at this level or an
   earlier one.** Levels are therefore validated in sequence, since a level
   cannot be checked alone.

## Budget shares are derived, never authored

The per-domain share is computed from scheduled concept count. There is no
share field to maintain, so there is no number that can drift out of
agreement with the units it describes.

**Level one allocates by what must be grounded, not by subject weighting.**
The level seeds primitives that all later content presupposes, and what has
to be grounded is a different question from what the corpus emphasises.
Subject weighting arrives at level three, where breadth of topics starts to
matter, and it will need its own decision at that point.

## A level may be partial

`covers` names the domains a level schedules and need not name all of them.
Level two schedules only the two ablation domains, because the ordering
experiment needs those two at depth and nothing else at level two is on the
critical path.

A partial level is a declared gap rather than an oversight, which is the
same reason domains are declared rather than inferred in the concept graph.

## Token budgets are ranges

`token_budget` carries a low and a high and the basis for both. The source
is word counts rather than measurement, so a point value would imply a
precision nobody has. `CURRICULUM_LEVELS.md` holds the per-level table.

## What the schedule does not contain

**Records.** It says what to write, not what was written. A generator reads
the schedule and emits records that the corpus validator then checks
independently.

**Ordering within a level.** Unit order in the file is not a teaching
order. Within-level ordering is the ablation's subject and must not be
fixed by the artifact the ablation reads.

**Concept definitions.** Those are the graph's. A unit names concepts; it
does not describe them.
