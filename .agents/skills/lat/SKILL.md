---
name: lat
description: Use the repository lat.md workflow correctly. Trigger this skill when working in this repo on code, tests, docs, architecture, behavior, or any task that should be grounded in `lat.md/`; when a prompt may contain `[[refs]]`; or when you need to run `lat search`, `lat locate`, `lat expand`, `lat refs`, or `lat check`.
---

# LAT

Use `lat.md/` as the source of project intent before changing code or docs, and keep it consistent after the change.

## Start Every Task

Run `lat search "<task terms>"` before writing code to find relevant sections. Read the matching sections to understand the design intent.

Run `lat expand "<user prompt>"` to resolve any `[[refs]]` in the request before acting on them.

If `lat search` fails because semantic search is unavailable, explain that it requires one of `LAT_LLM_KEY`, `LAT_LLM_KEY_FILE`, or `LAT_LLM_KEY_HELPER`, with a supported `sk-...` or `vck_...` key. If the user does not want to configure that, fall back to `lat locate` and direct file reads.

## Use lat.md Deliberately

Use `lat locate "Section Name"` for direct or fuzzy section lookup when you know roughly what you need.

Use `lat refs "file#Section"` to find cross-references before changing a concept that may be used elsewhere.

Treat `lat.md/` as the explanation of what the system does and why. Do not guess when the knowledge graph already documents the behavior.

## Maintain lat.md After Changes

Update `lat.md/` whenever you change functionality, architecture, tests, or behavior.

Keep each heading’s first paragraph immediately under the heading and no longer than 250 characters, excluding wiki-link text.

When documenting tests in `lat.md/`, ensure every section has a real description. If the file uses `lat.require-code-mention`, place exactly one nearby `@lat:` code reference on the test that covers each leaf section.

## Validate Before Finishing

Run `lat check` after editing code or `lat.md/`. Do not consider the task complete until it passes.

When `lat check` reports broken wiki links, missing code references, or invalid section structure, fix those issues before responding.
