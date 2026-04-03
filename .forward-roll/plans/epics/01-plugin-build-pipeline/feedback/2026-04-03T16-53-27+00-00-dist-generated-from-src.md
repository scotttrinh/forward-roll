# Feedback: dist-generated-from-src

## Metadata

- created_at: 2026-04-03T16:53:27+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- scope: spec
- outcome: adjust-spec

## Input

- Operator wants the plugin distribution to be post-build output under dist/ rather than checked-in generated roots.
- plugins/forward-roll/src/ must contain everything needed to rebuild the distribution directory from scratch.

## Required Next Action

- Update specs and Epic 01 planning artifacts so src is authoritative and dist is the generated CI/local build artifact.
