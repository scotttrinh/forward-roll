# Architecture

This document defines Forward Roll's package boundary, runtime contract, and implementation constraints.

## Product Boundary

Forward Roll should ship as a Codex plugin.

The product is not an installable application framework and not a repository-owned process requirement. It is a personal workflow tool that one developer can point at a repository, plus optional spec and planning roots, and use immediately.

## Plugin Shape

The shipped package should be explainable as static plugin assets plus deterministic scripts.

That means the plugin may contain:

- static `SKILL.md` files
- deterministic helper scripts
- optional prompt assets
- plugin metadata

The plugin should not depend on heavy install-time mutation, hidden daemon state, or a large shared runtime package.

## Runtime Contract

Before the workflow begins, Forward Roll should resolve a machine-readable runtime contract.

That contract should capture:

- `project_name`
- `repo_root`
- `specs_root`
- `plans_root`
- `research_root`
- whether those roots are in-repo, out-of-repo, or gitignored
- jj availability and any workflow conventions the plugin depends on
- testing posture defaults when they differ from the common Forward Roll defaults

## Personal Tooling Model

Forward Roll should assume that many repositories will never adopt its artifact layout directly.

Specs, plans, and research artifacts may:

- live inside the repository
- live outside the repository
- be gitignored
- be maintained only by the operator

Bootstrap must treat those cases as normal. The plugin should adapt to the operator's preferred layout rather than assuming the repository itself has adopted a mandated structure.

## jj-First Version Control Model

Forward Roll should treat `jj` as the primary version-control interface.

Git may still be the backing store or remote transport, but the workflow should talk in jj-native terms such as changes, revisions, stacks, squashing, splitting, and reviewable history.

The architecture should optimize for:

- a small number of meaningful revisions
- human-readable change narratives
- revision boundaries that match the bounded work slice
- easy reshaping of history before final review

It should avoid encouraging a trail of tiny commits that reflect local agent iteration instead of meaningful review units.

## Script Constraints

Bundled scripts should assume a constrained execution environment.

Prefer:

- standard library tooling
- explicit arguments
- plain JSON or markdown contracts
- deterministic outputs
- narrow responsibilities

Avoid:

- dependency installation as a normal runtime requirement
- hidden cross-script state
- long-lived service processes
- broad implicit assumptions about repository layout

## Review Boundary

Forward Roll should stop at reviewable boundaries rather than trying to automate an entire project lifecycle in one pass.

The core architectural unit is a bounded work slice that can be:

- shaped
- executed
- reviewed
- refined

That unit should be legible in planning state, jj history, and reviewer-facing summaries.

## Research As Infrastructure

Research is not optional decoration. It is a core part of the context pipeline.

The architecture should treat research artifacts as execution infrastructure: compact, high-signal, and explicitly designed to reduce context noise before shaping or execution work begins.

## Future Extension Points

After the first useful version is working, the most likely extension points are:

1. richer bootstrap helpers
2. better research generation and summarization
3. more structured plan shaping
4. stronger review summaries
5. optional subagent handoff boundaries

Those extensions should fit inside the existing plugin boundary instead of reintroducing a large orchestration framework.
