# Squash Workflow

Use this when you want one described change plus a scratch working-copy commit above it.

## Loop

1. Describe the intended change with `jj describe -m "<message>"`.
2. Create a scratch child with `jj new`.
3. Make edits in `@`.
4. Move finished work into the described parent with `jj squash`.
5. Use `jj squash <path>` or `jj squash -i` for selective movement.
6. Repeat until the parent change is in the state you want.

## Why This Is Idiomatic

- It replaces Git staging plus amend habits with commit-to-commit movement.
- It keeps one clearly described change while preserving a scratch area above it.
- It makes partial movement straightforward through `jj squash -i`.

## Typical Commands

- `jj describe -m "message"`
- `jj new`
- `jj st`
- `jj diff`
- `jj squash`
- `jj squash <path>`
- `jj squash -i`

## Good Fits

- The user wants to "stage some of this" or "amend the commit below".
- The user has ongoing scratch work and wants to fold only selected parts down.
- The user is comfortable thinking in terms similar to staging, but you want an idiomatic `jj` answer.

## Additional Detail

- Read `references/docs/tutorial/real-world-workflows/the-squash-workflow.md` for the full tutorial walkthrough.
