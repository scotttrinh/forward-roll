# Revsets

## Selection Strategy

- Use a change ID when you already have the change in view.
- Use a bookmark name for shared tips such as `main`, `trunk`, or `feature`.
- Use a revset when the target is relative to graph position, author, description, or visibility.

## Everyday Symbols

- `@`: current working-copy commit
- `@-`: parent of `@`
- `@+`: child of `@`
- `<bookmark>@<remote>`: remembered remote bookmark position such as `main@origin`
- `root()`: virtual root commit
- `all()` or `::`: all visible commits

## Everyday Operators

- `x-`: parents of `x`
- `x+`: children of `x`
- `::x`: ancestors of `x`
- `x::`: descendants of `x`
- `x..y`: ancestors of `y` that are not ancestors of `x`
- `x::y`: ancestry path from `x` toward `y`
- `x & y`: intersection
- `x | y`: union
- `x ~ y`: set difference

## Useful Functions

- `trunk()`: inferred shared trunk bookmark
- `bookmarks()`: all bookmarks
- `remote_bookmarks()`: all remembered remote bookmarks
- `mine()`: commits authored by the current user
- `description(substring:text)`: commits whose description contains text
- `ancestors(x, n)`: ancestors of `x` limited to depth `n`
- `heads(x)`: heads within set `x`
- `commit_id(x)`: force commit-ID interpretation

## Common Expressions

- `jj log -r ::@`: ancestors of the current working-copy commit
- `jj log -r '@ | trunk()'`: current work plus trunk
- `jj log -r 'bookmarks() | @'`: current work plus named refs
- `jj log -r 'author("Name") & description(substring:foo)'`: author and message filter
- `jj log -r '@ | ancestors(remote_bookmarks().., 2) | trunk()'`: a practical large-repo view from the tutorial

## Ambiguity And Quoting

- Symbol resolution prefers tags, then bookmarks, then Git refs, then commit or change IDs.
- Use `commit_id(x)` or another explicit revset function in scripts when ambiguity is risky.
- Quote revsets in the shell when they contain operators such as `|`, `&`, `~`, or parentheses.
- Quote literal symbols like `"x-"` if they would otherwise parse as expressions.

## Practical Advice

- Use short unique prefixes interactively.
- Use full or explicit handles in scripts and automation.
- If a revset unexpectedly returns more than one revision, narrow it before running edit or rewrite commands.

## Additional Detail

- Read `references/docs/core/revsets.md` for the authoritative language reference.
- Read `references/docs/tutorial/branching-merging-and-conflicts/revsets.md` for a worked tutorial explanation.
