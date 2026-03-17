This directory defines the high-level concepts, business logic, and architecture of this project using markdown. It is managed by [lat.md](https://www.npmjs.com/package/lat.md) — a tool that anchors source code to these definitions. Install the `lat` command with `npm i -g lat.md` and run `lat --help`.

- [[architecture]] documents system layers, planning storage, and type posture.
- [[domain]] documents the bootstrap domain model and testing philosophy.
- [[workflow]] documents bootstrap flow, review boundaries, and jj-oriented workflow intent.

## Agent Workflow

Repository agent instructions delegate detailed `lat.md` usage to the local `$lat` skill so the workflow stays reusable and does not bloat `AGENTS.md`.
