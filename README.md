# Forward Roll

Forward Roll is a `jj`-first workflow for doing real software work with coding agents without letting the work dissolve into long chat transcripts, giant plans, or unreadable patch stacks.

The core idea is simple:

- keep durable project intent in specs
- plan one reviewable epic at a time
- break execution into bounded slices
- leave each slice in a clean, reviewable `jj` change
- feed review results back into specs, epics, or follow-up work

This repository currently contains the first plugin implementation of that workflow in [plugins/forward-roll](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll).

## What Problem This Solves

Most agent workflows fall apart in one of three ways:

- the agent keeps too much in transient chat context and loses the thread
- the planning system becomes heavier than the code change
- the resulting Git history is technically correct but unpleasant to review

Forward Roll is aimed at a narrower, more opinionated loop:

- personal or small-team use
- brownfield repos, not just greenfield demos
- work that benefits from durable planning artifacts
- developers who want the execution unit to stay small enough for real review
- developers using `jj`, where "one change per bounded piece of work" is a natural fit

It is intentionally not a full project-management system. It is a development loop.

## Workflow

Forward Roll uses seven Codex skills:

- `fr-bootstrap`: resolve the repo's runtime contract and artifact locations
- `fr-specify`: create or refine durable high-level specs
- `fr-plan-epic`: define one reviewable deliverable and its slice breakdown
- `fr-plan-slice`: carve the next small execution unit out of the epic
- `fr-do`: execute exactly one slice, validate it, and log the outcome
- `fr-review`: compare epic intent against the current implementation
- `fr-feedback`: turn review or operator feedback into one explicit durable outcome

The intended loop is:

1. Bootstrap the repo so the workflow knows where specs and plans live.
2. Write or sharpen durable specs.
3. Plan one epic with a concrete definition of done.
4. Plan one bounded slice from that epic.
5. Execute that slice and validate it.
6. Review the epic against implementation.
7. Feed findings back into specs, epic updates, slice updates, or queued follow-up work.

That loop produces durable artifacts under `.forward-roll/` rather than burying all reasoning in chat history.

## Why `jj` Matters

Forward Roll is not just "planning, but with different filenames." It is designed around `jj`'s model:

- the working copy is already a change
- local iteration can be folded into a single intended review unit
- you do not need to pretend the index is your planning boundary
- change-oriented review maps better to slices than branch-oriented sprawl

In practice, that means `fr-do` is opinionated about leaving work in a reviewable `jj` state, not just "files changed successfully."

GitHub users do not need to know any of that. Published history can still look like ordinary Git branches and commits. `jj` is the local ergonomics layer, not the public collaboration requirement.

## Repository Layout

The implementation currently lives under [plugins/forward-roll](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll).

Key paths:

- [plugins/forward-roll/.codex-plugin/plugin.json](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/.codex-plugin/plugin.json): plugin metadata
- [plugins/forward-roll/skills/fr-bootstrap/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-bootstrap/SKILL.md): bootstrap workflow
- [plugins/forward-roll/skills/fr-specify/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-specify/SKILL.md): spec workflow
- [plugins/forward-roll/skills/fr-plan-epic/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-plan-epic/SKILL.md): epic planning
- [plugins/forward-roll/skills/fr-plan-slice/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-plan-slice/SKILL.md): slice planning
- [plugins/forward-roll/skills/fr-do/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-do/SKILL.md): bounded execution
- [plugins/forward-roll/skills/fr-review/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-review/SKILL.md): review workflow
- [plugins/forward-roll/skills/fr-feedback/SKILL.md](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll/skills/fr-feedback/SKILL.md): feedback workflow

## How You Use It

The primary interface is not "run these Python scripts by hand." The primary interface is talking to Codex and invoking the workflow skills.

A typical operator flow looks more like:

1. Ask Codex to run `fr-bootstrap` for the current repo.
2. Ask Codex to run `fr-specify` to discover or sharpen project specs.
3. Ask Codex to run `fr-plan-epic` for the next meaningful deliverable.
4. Ask Codex to run `fr-plan-slice` for the next bounded piece of work.
5. Ask Codex to run `fr-do` on that slice.
6. Ask Codex to run `fr-review` when the epic is ready for comparison against implementation.
7. Ask Codex to run `fr-feedback` to turn review output into an explicit next state.

The scripts in [plugins/forward-roll](/Users/scotttrinh/github.com/scotttrinh/forward-roll/plugins/forward-roll) are the deterministic helpers inside that agent loop. They exist to make artifact creation and updates predictable, portable, and less dependent on free-form model output.

You can run those helpers directly during plugin development or testing, but that is an implementation detail, not the intended day-to-day user experience.

## Deterministic Helpers

For local plugin development, the skill-owned helpers can also be run directly:

```bash
python3 plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py
python3 plugins/forward-roll/skills/fr-specify/scripts/specify.py auth --mode discover --goal "Describe the current auth system"
python3 plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py 04 auth-session-hardening --goal "Harden session handling"
python3 plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py 04 02 cookie-rotation --goal "Implement cookie rotation"
python3 plugins/forward-roll/skills/fr-do/scripts/do.py --slice .forward-roll/plans/epics/04-auth-session-hardening/slices/02-cookie-rotation.md --summary "Implemented cookie rotation and updated tests"
python3 plugins/forward-roll/skills/fr-review/scripts/review.py --epic .forward-roll/plans/epics/04-auth-session-hardening/EPIC.md
python3 plugins/forward-roll/skills/fr-feedback/scripts/feedback.py 04 review-follow-up --scope epic --outcome adjust-epic
```

## How Forward Roll Compares

Forward Roll is not trying to replace every other agent workflow. It is a narrower bet on where structure helps most.

### 1. Compared to GSD

GSD is a much larger operating system for project execution. It has milestone and phase management, roadmap maintenance, requirement mapping, research agents, planning agents, execution agents, verification passes, gap-closure loops, state tracking, and archival workflows.

Forward Roll is deliberately smaller:

- GSD plans at the milestone and phase level; Forward Roll plans at the epic and slice level.
- GSD optimizes for broad project orchestration; Forward Roll optimizes for the next reviewable unit of engineering work.
- GSD carries more formal process state; Forward Roll keeps only the artifacts needed to preserve intent and guide the next slice.
- GSD is better when multiple moving parts, requirement coverage, and lifecycle governance matter.
- Forward Roll is better when the problem is "keep this change small, legible, and grounded in durable intent."

In short:

- use GSD when you want a full execution framework
- use Forward Roll when you want a tight development loop

### 2. Compared to Codex's Built-in ExecPlan

OpenAI's ExecPlan guidance is built around a living `PLANS.md` document for multi-hour work. The official model is strong on resumability and disciplined narration: maintain progress, discoveries, decisions, and retrospective sections as the work evolves.

Forward Roll agrees with the underlying principle but changes the unit of planning:

- ExecPlan centers one evolving plan document for a substantial task.
- Forward Roll centers a stack of smaller durable artifacts: specs, an epic, then one slice at a time.
- ExecPlan is an excellent format for "one big task that needs a living implementation plan."
- Forward Roll is better suited to repeated, bounded execution where the review unit should stay small and the plan should collapse naturally into `jj` changes.
- ExecPlan is tool-agnostic about source control shape.
- Forward Roll is explicitly designed to end each execution step in a coherent `jj` review state.

The practical difference is that ExecPlan asks, "How do we keep one long-running effort legible?" Forward Roll asks, "How do we keep turning intent into small reviewed changes without losing the broader thread?"

### 3. Compared to ACE/FCA

The ACE/FCA essay argues for "frequent intentional compaction": design the whole workflow around context management, keep context utilization well below saturation, and use a research -> plan -> implement rhythm with human review at the right checkpoints.

Forward Roll is philosophically close to that approach. The difference is where the structure lives.

- ACE/FCA is primarily a context-engineering pattern.
- Forward Roll is a repository workflow built around artifacts and `jj` review boundaries.
- ACE/FCA emphasizes compaction across research, planning, and implementation passes.
- Forward Roll operationalizes a similar instinct by storing durable specs, epic intent, slice boundaries, review outputs, and feedback outcomes directly in the repo.
- ACE/FCA is deliberately general and can fit many toolchains.
- Forward Roll is deliberately opinionated about artifact shape, execution boundaries, and local `jj` ergonomics.

Put differently: ACE/FCA explains why compaction matters. Forward Roll is one concrete answer to "what should the compacted artifacts and execution loop actually look like in a real repo?"

## Decision Boundary

Choose Forward Roll when:

- you want durable planning, but not full-blown project ceremony
- you want each unit of execution to stay small and reviewable
- you care about preserving project intent outside of chat logs
- you use `jj` and want planning boundaries to align with change boundaries

Choose something else when:

- you need roadmap-level orchestration and formal phase governance
- one large living implementation plan is more natural than epic-plus-slice decomposition
- your team is not willing to maintain durable planning artifacts in the repo

## Status

This repository is the first implementation pass. The plugin skeleton exists, the workflow shape is defined, and the repo is currently focused on making the specs, artifacts, and skill contracts coherent enough to use and iterate on.

## References

- GSD local skill and workflow material in `/Users/scotttrinh/.codex`
- OpenAI cookbook article: https://developers.openai.com/cookbook/articles/codex_exec_plans
- Humanlayer ACE/FCA essay: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
