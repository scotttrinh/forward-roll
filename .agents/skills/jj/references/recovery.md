# Recovery And Safety

## First Response

1. Stop issuing more rewrite commands.
2. Inspect `jj st` and `jj log`.
3. Inspect `jj op log` if the mistake involved history editing or bookmark movement.
4. Inspect `jj evolog <rev>` if one change was rewritten repeatedly and you need an earlier version.

## Fast Recovery Tools

- Use `jj undo` to reverse the most recent operation.
- Use repeated `jj undo` if you need to walk back multiple operations.
- Use `jj op revert <op>` to invert a specific older operation.
- Use `jj op restore <op>` to restore the whole repo view to an earlier operation.
- Use `jj --at-op <op> log` or `jj --at-op <op> st` to inspect historical state safely.

## Recovering A Change

- Use `jj evolog <rev>` to see prior incarnations of a rewritten change.
- Use `jj restore` or targeted squashes after locating the version you need.
- Prefer recovering by intention, not by brute-force reset.

## Resolving Conflicts

- Conflicted commits are normal `jj` state, not a failure mode by themselves.
- Create a child working-copy change with `jj new <conflicted-rev>` when you want to inspect the resolution before folding it back.
- Use `jj edit <conflicted-rev>` when direct editing is simpler.
- Use `jj resolve` for supported merge-tool flows.
- Use `jj squash` to fold a separately prepared resolution back into the conflicted revision.

## Bookmark Problems

- Use `jj bookmark list --all` to inspect local and remote bookmark state.
- If a bookmark is conflicted, move it intentionally with `jj bookmark move` or rebase/merge the underlying commits first.
- Fetch before pushing if remote state may be stale.

## Workspace Problems

- Use `jj workspace update-stale` when a workspace says it is stale.
- Expect this after rewriting the working-copy commit from another workspace.

## Safety Principles

- Prefer `jj` recovery tools over `git reset --hard` or raw ref surgery.
- Re-run `jj log` after each recovery step so you do not compound the problem.
- If you are unsure which operation caused the issue, inspect `jj op log` before changing more state.

## Additional Detail

- Read `references/docs/core/operation-log.md` for whole-repo undo, revert, restore, and `--at-op`.
- Read `references/docs/core/working-copy.md` for conflict materialization and stale workspace behavior.
- Read `references/docs/tutorial/branching-merging-and-conflicts/conflicts.md` for a narrative conflict-resolution example.
