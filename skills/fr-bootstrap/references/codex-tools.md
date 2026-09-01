# Codex Tool Mapping

## Multi-Agent Configuration

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

Role files can be registered under `~/.codex/agents/` (or repository `.codex/agents/`):
- `fr-impl.toml`
- `fr-review.toml`

## Tool Equivalents

| Action | Codex Tool | Notes |
|---|---|---|
| **Dispatch Implementer** | `spawn_agent` (`agent_type: "fr-impl"`, `sandbox_mode: "workspace-write"`, `fork_turns: "none"`) | Edits land directly in the workspace. |
| **Dispatch Reviewer** | `spawn_agent` (`agent_type: "fr-review"`, `sandbox_mode: "read-only"`, `fork_turns: "none"`) | Spec compliance and acceptance criteria check. |
| **Run `jj` History Surgery** | `run_command` (`CommandLine: "jj describe ..."` / `"jj squash"`) | Orchestrator runs `jj` commands. Subagents never run `jj`. |
| **File Operations** | `file_read`, `file_edit`, `create_file` | Standard tools. |
| **Task Progress** | Maintained in `.forward-roll/` artifacts | Epics, slices, ledgers. |
