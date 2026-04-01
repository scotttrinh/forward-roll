This directory defines the forward-looking product specs for Forward Roll.

- [[architecture]] defines the plugin boundary, runtime contract, packaging model, and script constraints.
- [[workflow]] defines the operator-facing command loop, epic and slice planning flow, and jj-first execution model.
- [[context]] defines the durable artifact model for specs, epics, slices, logs, feedback, and reviews.
- [[testing]] defines Forward Roll's testing posture and TDD guidance.

## Product Direction

Forward Roll is a personal, Codex-first workflow plugin.

It should help one developer bootstrap a working context, define or discover high-level specs, plan reviewable epics, break those epics into good-commit-sized slices, execute them with good context, and refine quickly from feedback. It should feel fluid to use while still being opinionated about context quality, review boundaries, jj-native workflow, and validation.

## Authoring

Treat these specs as the source of truth for the plugin we want to use to keep evolving Forward Roll itself.

The goal is not a heavyweight process framework. The goal is to define the workflow and assets clearly enough that we can build one useful pass of skills and scripts, start using them, and refine the workflow from real use.
