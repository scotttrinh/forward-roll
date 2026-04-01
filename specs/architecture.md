# Architecture

This document defines Forward Roll's product boundary, runtime constraints, and shipped asset model.

## System Shape

Forward Roll should ship as one Codex plugin made of static skills and deterministic runtime scripts.

The product is not a shared Python application with installable dependencies. It is a plugin package whose behavior comes from bundled `SKILL.md` files, bundled scripts, explicit config, planning artifacts, and Codex-native execution features.

Related:

- [[workflow#Plugin-First Self-Hosting]]
- [[workflow#Phase Review Loop]]

## Core Product Model

Forward Roll manages software work through specs, planning artifacts, jj-aware execution, explicit review boundaries, and operator-facing skills.

The core product idea is not "run an app." It is "ship a plugin that can read specs, read and update plans, execute bounded work, and keep review state legible inside Codex."

## Runtime Contract

Each Forward Roll installation should resolve a stable runtime contract before planning or execution begins.

That contract should capture project identity, `repo_root`, `specs_root`, `plans_root`, and any stable workflow conventions the shipped skills depend on. It should live in explicit machine-readable config rather than hidden process state.

## Plugin Boundary

Forward Roll should integrate with Codex first as a static plugin.

The shipped product should be one Codex plugin rooted at `plugins/forward-roll/` with a required `.codex-plugin/plugin.json`, bundled `fr-*` skills, plugin-local scripts, and any plugin-scoped metadata needed for marketplace installation. Repository-local tooling may help build or validate that package, but the installed runtime should be explainable from the plugin files plus operator-managed config.

Related:

- [[workflow#Plugin-First Self-Hosting]]
- [[workflow#Workflow Prompt Templates]]

## Application Layer

The application layer is the workflow contract shared across shipped skills, not a required shared runtime package.

This layer defines the operator-facing commands, the planning and review boundaries they enforce, the runtime bundle each command must assemble, and the reproducible outcomes expected from bootstrap, planning, execution, feedback, and review flows. If multiple scripts implement that contract, they should do so through copied or repeated logic only when Codex plugin constraints leave no safer shared mechanism.

## Adapter Layer

The adapter layer turns local filesystem, config, planning docs, and Codex runtime context into the command contracts the skills need.

In the plugin-shaped product, adapters are mostly script-level concerns: reading config, locating roots, discovering planning artifacts, collecting jj state, and normalizing runtime inputs. They should prefer explicit files and stable conventions over hidden process state or environment-specific heuristics.

## CLI Adapter

A CLI may remain as repo-local tooling, but it is not the product boundary.

If local CLI commands continue to exist in this repository, they should be treated as development helpers, migration aids, or validation tools for the plugin package. They should not define the core user experience or be required to make the shipped plugin usable inside Codex.

## Host Asset Responsibilities

Shipped skills, bundled scripts, and aspirational subagents should have different jobs.

Skills should own command entry, operator-facing stop conditions, shared-context assembly, and final reporting. Bundled scripts should own deterministic config resolution, filesystem reads and writes, and other repeatable runtime work that fits inside plugin execution limits. Subagents, if Codex plugin support becomes available, should own specialized planning, execution, review, or classification work after the calling skill has assembled a complete handoff bundle.

## Workflow Prompt Assets

Workflow prompt assets should be shipped as stable plugin assets rather than generated per run.

Prompt instructions, role definitions, and any reusable text assets should live with the plugin, keep stable names, and accept runtime context through explicit inputs. Runtime variation belongs in config, planning docs, operator inputs, and workspace state, not in rewritten prompt assets.

## Planning Storage

Planning artifacts are a product boundary and should remain distinct from the plugin package itself.

Forward Roll should support a `plans_root` that may live outside the repository and a `specs_root` that may be governed separately from plans. The plugin should read and update those roots through config rather than assuming they live next to the plugin or inside a shared monolithic workspace.

## Runtime Configuration Responsibilities

Runtime config should drive installed behavior instead of install-time mutation.

The plugin should include a bootstrap skill that creates or refreshes config, explains the resolved roots, and leaves later skills with a deterministic runtime contract to read. Other skills should treat config as the source of installation-specific paths and conventions, while keeping the shipped plugin assets themselves static.

## Bootstrap Mutation Boundary

Bootstrap may create config and deterministic derived files, but it must not rewrite the shipped plugin.

Allowed bootstrap outputs include config files, discovered root summaries, cached derived context, and other deterministic runtime artifacts. Disallowed bootstrap behavior includes rewriting bundled `SKILL.md`, rewriting `.codex-plugin/plugin.json` for one installation, installing dependencies, or materializing a second copied set of host-visible skills as the normal runtime path.

## Script Runtime Constraints

Bundled scripts should be written for a hostile runtime with very few guarantees.

Assume no dependency installation, no shared utility package, no persistent daemon, and no guarantee that multiple scripts can import one another safely through a packaged Python module. Prefer the Python standard library, plain-text or JSON file contracts, explicit arguments, deterministic outputs, and small scripts with narrow responsibilities. Shared behavior should be duplicated only with care, and only when plugin constraints make normal code sharing unavailable.

## Subagent Boundary

Forward Roll should define subagent roles even before plugin support is guaranteed.

The aspirational product should describe specialized planning, execution, review, and feedback-classification subagents as part of the workflow contract so the skill boundaries are ready if Codex plugins gain subagent support. Until then, the skills and scripts should preserve the same handoff boundaries in a form that can run without those subagents.

## Knowledge and Planning Boundary

Specs and planning artifacts should remain adjacent but distinct layers of truth.

The spec layer should describe the aspirational product model, workflow ideas, and rationale in whatever document system the operator maintains. Planning artifacts should describe the next concrete work needed to move the product toward that model. Forward Roll should consume both layers together without assuming a specific spec tool at runtime.

## Type Posture

Forward Roll should prefer explicit contracts, but not a heavy shared type system at runtime.

The product should use simple, legible data shapes for config, planning bundles, and script outputs so the runtime stays robust under plugin constraints. Strong typing may still be useful in repo-local tooling or tests, but shipped plugin behavior should not depend on a rich shared Python type layer.
