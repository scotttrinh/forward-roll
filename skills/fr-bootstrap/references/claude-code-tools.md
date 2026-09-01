# Claude Code Tool Mapping

| Action | Claude Code Tool | Notes |
|---|---|---|
| **Dispatch Implementer** | `task` (role prompt describing slice contract and TDD instructions) | Operates on working tree. |
| **Dispatch Reviewer** | `task` (role prompt for read-only acceptance and spec verification) | Verifies diff vs slice criteria. |
| **Run `jj` History Surgery** | `bash` (`jj describe`, `jj squash`, etc.) | Orchestrator runs `jj` commands. Subagents do not touch `jj`. |
| **File Operations** | `View`, `Edit`, `Write` | Standard tools. |
