# Antigravity CLI (`agy`) Tool Mapping

Forward Roll skills speak in terms of general actions ("dispatch subagent", "read file", "run command", "maintain task progress"). On Antigravity (`agy`), these map to:

| Action | Antigravity CLI Tool | Notes |
|---|---|---|
| **Dispatch Implementer (`fr-impl`)** | `invoke_subagent` (`TypeName: "self"`, `Workspace: "inherit"`) | Uses `Workspace: "inherit"` so edits land directly in the working copy change `@`. |
| **Dispatch Reviewer (`fr-review`)** | `invoke_subagent` (`TypeName: "research"`) | Read-only reviewer verifying implementation against spec/epic criteria. |
| **Run `jj` History Surgery** | `run_command` (`CommandLine: "jj describe ..."` / `"jj squash"`) | Orchestrator (`fr-do`) directly executes `jj` commands. Subagents never run `jj`. |
| **Inspect / Edit Files** | `view_file`, `write_to_file`, `replace_file_content` | Standard file manipulation. |
| **Track Task Progress** | Task artifact via `write_to_file` / `replace_file_content` | Main session maintains progress in `.forward-roll/` artifacts. |
