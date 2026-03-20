# Source Material

All cited docs below are bundled verbatim inside this skill so it can be used outside the `jj` repo.

## Bundled Core Docs

- `references/docs/core/tutorial.md`: baseline tutorial for Git-familiar users
- `references/docs/core/git-comparison.md`: conceptual differences from Git
- `references/docs/core/git-experts.md`: migration framing for experienced Git users
- `references/docs/core/revsets.md`: authoritative revset language reference
- `references/docs/core/bookmarks.md`: bookmark, tracking, and remote semantics
- `references/docs/core/working-copy.md`: working-copy behavior, conflicts, stale workspaces
- `references/docs/core/operation-log.md`: undo, restore, and historical inspection
- `references/docs/core/git-command-table.yml`: Git-to-`jj` intent mapping

## Bundled Tutorial Docs

Use the tutorial chapters for worked examples and agent-friendly explanations.

- `references/docs/tutorial/real-world-workflows/the-squash-workflow.md`
- `references/docs/tutorial/real-world-workflows/the-edit-workflow.md`
- `references/docs/tutorial/branching-merging-and-conflicts/revsets.md`
- `references/docs/tutorial/branching-merging-and-conflicts/conflicts.md`
- `references/docs/tutorial/sharing-code/named-branches.md`
- `references/docs/tutorial/sharing-code/remotes.md`

## Optional Upstream Sources

Use the upstream repo and tutorial checkout only when you need implementation-level behavior or more surrounding context than the bundled docs provide.

- Command implementations: `cli/src/commands/`
- Revset and graph helpers: `cli/src/revset_util.rs`, `cli/src/graphlog.rs`
- Behavioral tests: `cli/tests/`

## Useful Search Patterns In The Upstream Repo

- `rg --files docs cli/src/commands cli/tests | rg 'rebase|squash|split|bookmark|undo|operation|restore|revset|log|status|git'`
- `rg -n 'allow-backwards|tracked|conflict|auto-track|working copy|evolog' docs cli/src cli/tests`
- `rg -n 'squash workflow|edit workflow|named branches|remotes|conflict' ~/github.com/scotttrinh/jujutsu-tutorial/src`
