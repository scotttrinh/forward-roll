---
name: jj
description: Teach and apply effective, idiomatic Jujutsu (`jj`) workflows in Git-backed repositories. Use when Codex needs to work with `jj` commands or concepts, translate Git intent into `jj`, manipulate history safely, choose between `jj` workflows such as `squash` versus `edit`, work with change IDs, revsets, bookmarks, remotes, the operation log, or conflict resolution, or when a repository is managed with `jj` and `git` should only be used for interoperability.
---

# Jujutsu (jj)

## Overview

Use `jj` as the primary interface for local history, patch-stack editing, and recovery.
Think in terms of changes, revsets, and bookmarks, not the Git index or a checked-out branch.

## Start Here

1. Inspect the current state with `jj st`, `jj log`, and `jj diff` as needed.
2. Identify the target revision by change ID, bookmark, or revset.
3. Choose the simplest `jj` primitive that matches the intent.
4. Re-run `jj log` and `jj st` after any rewrite, rebase, squash, or bookmark move.
5. Reach for `jj undo`, `jj op log`, and `jj evolog` before attempting destructive recovery.

## Core Rules

- Prefer change IDs over commit IDs in interactive work because change IDs stay stable across rewrites.
- Prefer `jj` history-editing commands over `git add`, `git commit --amend`, `git rebase -i`, `git stash`, or `git reset --hard`.
- Treat bookmarks as named pointers for collaboration, not as a "current branch" concept.
- Expect descendants to rebase automatically when a commit is rewritten.
- Expect conflicts to be representable in commits; rebases do not have to block the rest of the stack.
- Use Git directly only for gaps in `jj` support or external tooling expectations.

## Mental Model

- The working copy is itself a commit. Most `jj` commands snapshot file changes into the working-copy commit.
- There is no index. If the user wants staging, think in terms of moving changes between commits with `jj squash` or `jj split`.
- There is no checked-out branch. `@` determines where local editing happens; bookmarks are separate named pointers.
- A change ID is the stable handle for evolving work. A commit ID is one exact rewritten instance of that change.
- Rewriting a commit usually rebases descendants automatically, so expect downstream commit IDs to change.
- Conflicted commits are valid repository state. Resolve them intentionally instead of treating them as a failed rebase.

## Choose A Workflow

- Use the squash workflow when you want a stable described change plus a scratch commit on top. Read [references/squash-workflow.md](references/squash-workflow.md).
- Use the edit workflow when you need to jump back into an existing change or insert a precursor change before it. Read [references/edit-workflow.md](references/edit-workflow.md).
- Use revsets when the target is better described by graph position than by a literal ID. Read [references/revsets.md](references/revsets.md).
- Translate Git-oriented requests into `jj` intent first, then select the `jj` command. Read [references/git-translation.md](references/git-translation.md).
- Recover with operation-log tools and evolution history instead of raw Git reset/reflog patterns. Read [references/recovery.md](references/recovery.md).

## Load References Deliberately

- Read [references/squash-workflow.md](references/squash-workflow.md) for the described-parent plus scratch-child workflow.
- Read [references/edit-workflow.md](references/edit-workflow.md) for direct editing and insert-before flows.
- Read [references/revsets.md](references/revsets.md) for selection syntax and common expressions.
- Read [references/git-translation.md](references/git-translation.md) when the request is phrased in Git terms.
- Read [references/recovery.md](references/recovery.md) when something went wrong or the safest command is unclear.
- Read [references/sources.md](references/sources.md) when you need to consult the authoritative docs, tutorial chapters, or implementation/tests.

## Idiomatic Defaults

- Start with `jj describe` once you know the intent of a change.
- Use `jj new` to create the next scratch change.
- Use `jj squash` to move finished work from the working-copy change into its parent.
- Use `jj edit <rev>` or `jj next --edit` to resume editing an existing change.
- Use `jj new -B <rev>` to insert a change before another change.
- Use `jj bookmark set` intentionally before pushing, instead of assuming bookmarks move because `@` moved.
- Use `jj git push -c @` or explicit bookmarks for PR-shaped remote workflows.

## Pitfalls To Avoid

- Do not assume an index exists. If the user wants partial staging, think `jj squash -i` or `jj split`.
- Do not assume a current branch exists. If the user wants "the branch I am on", inspect bookmarks and `@`.
- Do not assume commit hashes are the best handle. Prefer change IDs unless scripting or disambiguation requires commit IDs.
- Do not panic when `jj` reports conflicts after a rebase. Inspect the conflicted change and resolve it intentionally.
- Do not use raw Git history surgery as the first answer inside a `jj` repo unless interoperability requires it.
