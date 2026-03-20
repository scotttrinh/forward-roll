# Git Translation

## Conceptual Translation

- Translate "staging area" into "move changes between commits".
- Translate "current branch" into "current working-copy change plus any relevant bookmarks".
- Translate "reflog" into "operation log" and sometimes "evolog".
- Translate "branch for collaboration" into "bookmark".

## Common Intent Mapping

| Git intent | Prefer in `jj` |
| --- | --- |
| `git status` | `jj st` |
| `git diff HEAD` | `jj diff` |
| `git show X` | `jj show X` |
| `git add <file>` | Edit the file; if moving it into the parent change, use `jj squash <file>` |
| `git add -p` | `jj squash -i` or interactive `jj split` |
| `git commit --amend` | `jj squash` |
| `git commit --fixup X` plus autosquash | `jj squash --into X` |
| `git checkout X` to keep editing | `jj edit X` |
| `git stash` | `jj new @-` and later `jj edit <old-change>` |
| `git rebase -i` | Combine `jj rebase`, `jj split`, `jj squash`, and `jj edit` |
| `git reset --hard` to discard a change | `jj abandon` or `jj restore`, depending on intent |
| `git branch` for remote-facing names | `jj bookmark ...` |
| `git fetch` | `jj git fetch` |
| `git push` | `jj git push` |

## Important Differences

- `jj squash` moves changes from one commit into another; it is broader than "amend".
- `jj split` replaces many index-driven workflows.
- `jj edit` changes which revision the working copy is rewriting.
- `jj new` creates a new working-copy change; it often replaces both "commit current work" and "start next thing".
- Bookmarks do not define where new commits go. `@` does.

## Remote And PR Workflow

- Push a named bookmark when you want a stable branch-like name on the remote.
- Use `jj git push -c @` when you want `jj` to create a push bookmark suitable for a PR workflow.
- Fetch first when remote state may have changed.
- Treat `jj git push` as closer to `git push --force-with-lease` than to an unchecked force push.

## When To Still Mention Git

- Mention Git when translating the user's mental model.
- Mention Git when an interoperability step is required, such as hosting service expectations.
- Return to `jj` immediately for local graph changes when possible.

## Additional Detail

- Read `references/docs/core/git-comparison.md` for the conceptual differences from Git.
- Read `references/docs/core/git-experts.md` for Git-oriented workflow framing.
- Read `references/docs/core/git-command-table.yml` for a broader intent-to-command mapping.
