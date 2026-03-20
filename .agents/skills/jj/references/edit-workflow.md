# Edit Workflow

Use this when you need to resume editing a specific change or insert work before it.

## Loop

1. Jump into an existing change with `jj edit <rev>`.
2. Keep working; file changes rewrite that change directly.
3. Move through the stack with `jj next --edit` or `jj prev --edit` if available in the environment.
4. Insert a precursor change with `jj new -B <rev> -m "<message>"`.
5. Let `jj` rebase descendants automatically.

## Why This Is Idiomatic

- It is the most direct way to continue shaping an existing patch stack.
- It matches requests like "go back to that change and keep editing it".
- It makes insert-before workflows natural without needing Git-style interactive rebase choreography.

## Typical Commands

- `jj edit <rev>`
- `jj next --edit`
- `jj prev --edit`
- `jj new -B <rev> -m "message"`
- `jj log`
- `jj diff -r <rev>`

## Good Fits

- The user wants to resume an older change.
- The user wants to insert a new dependency or precursor change before an existing one.
- The user is doing patch-stack surgery rather than scratch-to-parent movement.

## Additional Detail

- Read `references/docs/tutorial/real-world-workflows/the-edit-workflow.md` for the full tutorial walkthrough.
