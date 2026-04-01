This directory defines the forward-looking product specs for Forward Roll.

- [[architecture]] defines the plugin boundary, runtime contract, packaging model, and script constraints.
- [[workflow]] defines the operator-facing skill loop, feedback flow, and jj-first execution model.
- [[context]] defines the durable artifact model, research expectations, and context-shaping rules.
- [[testing]] defines Forward Roll's testing posture and TDD guidance.

## Product Direction

Forward Roll is a personal, Codex-first workflow plugin.

It should help one developer bootstrap a working context, shape the next bounded slice of work, execute it with good context, review the result, and refine quickly from feedback. It should feel fluid to use while still being opinionated about context quality, review boundaries, jj-native workflow, and validation.

## Authoring

Treat these specs as the source of truth for the plugin we want to try in practice soon.

The goal is not a large implementation roadmap. The goal is to define the workflow and assets clearly enough that we can build one useful pass of skills and scripts, start using them, and refine the workflow from real use.
