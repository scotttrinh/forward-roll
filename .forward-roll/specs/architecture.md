# Architecture

This document defines Forward Roll's package boundary, runtime contract, and implementation constraints.

## Product Boundary

Forward Roll should ship as a Codex plugin.

The product is not an installable application framework and not a repository-owned process requirement. It is a personal workflow tool that one developer can point at a repository, plus optional spec and planning roots, and use immediately.

## Plugin Shape

The shipped package should be explainable as static plugin assets plus deterministic scripts.

That means the plugin may contain:

- static `SKILL.md` files
- deterministic helper scripts bundled inside each skill's `scripts/` directory
- generated skill assets produced from repository-local source templates or shared source files
- optional prompt assets
- plugin metadata

The plugin should not depend on heavy install-time mutation, hidden daemon state, a large shared runtime package, or repository-global runtime modules.

Each skill should remain a self-contained bundle:

- `SKILL.md` defines the workflow surface
- `scripts/` contains only the deterministic helpers that skill needs
- skill scripts do not import code from other skills
- the plugin runtime does not rely on a shared helper library across skills

The repository used to author the plugin may still contain a shared source tree and a build step.

- shared code, templates, and prompt fragments may live under a repository-local source root such as `src/`
- build tooling may render templates, inline shared logic, and copy common assets into multiple skill bundles
- the build output must preserve the distributed plugin contract: each shipped skill remains self-contained and runnable without cross-skill imports or a plugin-global runtime package
- source-time sharing is allowed specifically to reduce duplication in the authored repository, not to reintroduce runtime coupling inside the distributed plugin

For the Forward Roll repository itself, the authoring/build contract is:

- `src/` is the source-of-truth root for all version-controlled plugin inputs needed to build the distributable plugin from scratch
- `plugins/forward-roll/` is the generated distribution root for the plugin bundle, including `.codex-plugin/` metadata and self-contained `skills/` output
- the build manifest and repository-local build entrypoint should live under `src/` or another authoring-side path rather than inside the generated distribution tree
- `plugins/forward-roll/` should be safe to regenerate entirely from `src/` in CI or locally
- the repository should treat top-level `src/` as the long-term source of truth and `plugins/forward-roll/` as generated distribution output

## Runtime Contract

Before the workflow begins, Forward Roll should resolve a machine-readable runtime contract.

That contract should capture:

- `project_name`
- `repo_root`
- `specs_root`
- `plans_root`
- the planning layout conventions used inside `plans_root`, including epic directories, nested slice files, and review or feedback locations
- whether those roots are in-repo, out-of-repo, or gitignored
- jj availability and any workflow conventions the plugin depends on
- testing posture defaults when they differ from the common Forward Roll defaults

## Personal Tooling Model

Forward Roll should assume that many repositories will never adopt its artifact layout directly.

Specs and plans may:

- live inside the repository
- live outside the repository
- be gitignored
- be maintained only by the operator

Bootstrap must treat those cases as normal. The plugin should adapt to the operator's preferred layout rather than assuming the repository itself has adopted a mandated structure.

Planning artifacts should follow one coherent layout rooted at `plans_root`. If the operator keeps plans in a private or out-of-repo location, epic directories, nested slices, feedback notes, and reviews should all live there as well.

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
- third-party runtime dependencies
- hidden cross-script state
- imports between skill bundles
- long-lived service processes
- broad implicit assumptions about repository layout

Repository-local development and build tooling may be richer than the shipped runtime when needed to assemble the final plugin layout. That tooling should remain a development concern, produce deterministic outputs, and leave the distributed plugin compatible with constrained execution environments.

Forward Roll may still use repository-local development tooling for authoring and validation, but that tooling should remain outside the distributed plugin runtime. Development helpers may lint and type-check the skill scripts, while the shipped skill scripts themselves remain stdlib-only.

## Review Boundary

Forward Roll should stop at reviewable boundaries rather than trying to automate an entire project lifecycle in one pass.

The core planning units are:

- specs as durable project truth
- epics as reviewable deliverables
- slices as bounded execution units

Those units should be legible in planning state, jj history, and reviewer-facing summaries.

## Future Extension Points

After the first useful version is working, the most likely extension points are:

1. richer bootstrap helpers
2. better specification and codebase discovery support
3. more structured epic planning
4. stronger slice planning and resume support
5. deeper review and feedback automation

Those extensions should fit inside the existing plugin boundary instead of reintroducing a large orchestration framework.
