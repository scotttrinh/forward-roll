# Forward Roll

Forward Roll is a `jj`-first development workflow for coding agents. It helps developers and agents build software with discipline without letting work dissolve into sprawling chat transcripts, giant plans, or messy commit histories.

## Core Design Principles

1. **Jujutsu (`jj`) Over Git**: The working copy `@` accumulates local iteration, which is described (`jj describe`) and folded (`jj squash`) into clean, single-change review boundaries.
2. **Unversioned Planning Artifacts**: Specs, epics, slices, ledgers, and task briefs live in `.forward-roll/` (ignored by VCS), keeping git/jj history clean of transient planning clutter.
3. **External & Explicit Configuration**: Environment and runtime contracts are stored explicitly in `.forward-roll/runtime.json`.
4. **Structured Development Phases**:
   - **`fr-bootstrap`**: Resolve repo environment and runtime contracts.
   - **`fr-specify`**: Create or refine durable high-level specifications.
   - **`fr-plan-epic`**: Define one reviewable deliverable and its slice breakdown.
   - **`fr-plan-slice`**: Carve out the next bounded execution slice.
   - **`fr-do`**: Orchestrate the slice via `fr-impl` (TDD implementer) and `fr-review` (spec reviewer), gating the `jj` changeset on clean review.
   - **`fr-review`**: Review the assembled epic stack against the definition of done.
   - **`fr-feedback`**: Record review or operator feedback as an explicit next state.

---

## Installation

### Claude Code

- Install from the plugin repository:
  ```bash
  /plugin install https://github.com/scotttrinh/forward-roll
  ```
- Claude Code runs the SessionStart hook automatically.

### Antigravity (`agy`)

- Install as a plugin:
  ```bash
  agy plugin install https://github.com/scotttrinh/forward-roll
  ```

### Codex CLI / App

- Open the plugins interface:
  ```bash
  /plugins
  ```
- Or register the repository in your plugin catalog.
- Enable multi-agent support in `~/.codex/config.toml`:
  ```toml
  [features]
  multi_agent = true
  ```

### OMP

- Add to your OMP marketplace or load locally:
  ```bash
  omp plugin install ./
  ```
- Ensure `.omp/config.yml` has non-isolated task mode enabled:
  ```yaml
  task:
    isolation:
      mode: none
  ```

### Cursor

- Install via Cursor plugin manager or add plugin from repository URL:
  ```text
  /add-plugin https://github.com/scotttrinh/forward-roll
  ```

---

## Repository Layout

```text
forward-roll/
├── .agents/                    # Antigravity marketplace registry & skills
├── .claude-plugin/             # Claude Code manifest & marketplace config
├── .codex-plugin/              # Codex plugin manifest
├── .cursor-plugin/             # Cursor plugin manifest
├── .omp-plugin/                # OMP catalog config
├── .omp/                       # OMP environment configuration
├── agents/                     # Subagent definitions (OMP / Codex)
│   ├── fr-impl.md
│   └── fr-review.md
├── hooks/                      # SessionStart lifecycle hooks
│   ├── hooks.json
│   ├── hooks-cursor.json
│   ├── run-hook.cmd
│   └── session-start
├── skills/                     # Canonical skill definitions
│   ├── fr-bootstrap/
│   ├── fr-specify/
│   ├── fr-plan-epic/
│   ├── fr-plan-slice/
│   ├── fr-do/
│   ├── fr-review/
│   └── fr-feedback/
├── gemini-extension.json       # Gemini / Antigravity manifest
├── package.json                # Pi / OpenCode package metadata
├── AGENTS.md                   # Agent guidelines
├── CLAUDE.md                   # Claude Code instructions
├── GEMINI.md                   # Gemini context include
└── README.md
```

---

## License

MIT
