---
name: tooluniverse-codex-plugin
description: "Use when working on this repository's Codex plugin track: `.codex-plugin/plugin.json`, `.mcp.json`, `scripts/build_codex_plugin.py`, shared packaging metadata, local Codex marketplace wiring, or validation that the Codex plugin still wraps the existing ToolUniverse MCP runtime. Do not use for generic ToolUniverse development, generic Codex plugin tutorials, or Claude-only MCPB work."
---

# ToolUniverse Codex Plugin

Follow the Codex plugin track defined in [`PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/PLAN.md) and sequenced in [`INTERIM_PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/INTERIM_PLAN.md).

## Use This Skill When

- creating or editing the repo-local Codex plugin scaffold under `plugins/tooluniverse/`
- generating or validating `.codex-plugin/plugin.json`
- generating or validating `.mcp.json`
- adding `scripts/build_codex_plugin.py`
- extracting shared metadata/helpers used by both Codex and Claude packaging
- wiring repo-local Codex marketplace installation and test flow
- checking that Codex packaging changes do not break the Claude `.mcpb` builder

## Do Not Use This Skill When

- the task is normal ToolUniverse runtime or scientific-tool development unrelated to Codex packaging
- the task is only about the Claude `.mcpb` bundle
- the task is a generic Codex plugin tutorial not tied to this repo
- the task depends on historical guidance under `tooluniverse-mcpb/MCP-creation-prompts/*Codex*`

## Project Decisions To Preserve

- Codex uses a native plugin wrapper around MCP, not a Codex-flavored `.mcpb`.
- Claude `.mcpb` remains supported and must keep building.
- Codex v1 wraps the existing ToolUniverse MCP launch contract instead of bundling a private runtime.
- Compact mode stays on by default for Codex-facing ToolUniverse MCP launches.
- Official Codex plugin docs override historical prompt files when they conflict.

## Canonical Inputs

Read these first and keep them aligned:

- [`PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/PLAN.md)
- [`INTERIM_PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/INTERIM_PLAN.md)
- [`pyproject.toml`](/Users/centaurioun/Repos/ToolUniverse/pyproject.toml)
- [`server.json`](/Users/centaurioun/Repos/ToolUniverse/server.json)
- [`src/tooluniverse/smcp_server.py`](/Users/centaurioun/Repos/ToolUniverse/src/tooluniverse/smcp_server.py)
- [`scripts/build_mcpb.py`](/Users/centaurioun/Repos/ToolUniverse/scripts/build_mcpb.py)

Treat current official Codex docs as the external authority:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/config-reference`

If details are unclear, use the `openai-docs` skill or the OpenAI docs MCP tools instead of memory.

## Working Method

1. Reconfirm the current step in [`INTERIM_PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/INTERIM_PLAN.md) before editing.
2. Keep Codex plugin work repo-local and deterministic.
3. Reuse the existing ToolUniverse stdio/MCP launch behavior instead of inventing a new runtime path.
4. Prefer shared metadata helpers only where they remove real duplication between Codex and Claude artifacts.
5. Avoid broad refactors. Touch only the files needed for the current plan step.
6. Verify each nontrivial change with the smallest meaningful command or test before moving on.

## Expected File Targets

During implementation, the main files will usually be:

- `plugins/tooluniverse/.codex-plugin/plugin.json`
- `plugins/tooluniverse/.mcp.json`
- `plugins/tooluniverse/skills/`
- `plugins/tooluniverse/assets/`
- `plugins/tooluniverse/README.md`
- `scripts/build_codex_plugin.py`
- shared packaging helpers if extracted
- tests covering Codex plugin generation and version alignment

## Validation Checks

Before calling a step complete, verify the relevant subset of:

- generated Codex plugin manifest paths are valid
- `.mcp.json` still launches ToolUniverse in compact mode
- version and descriptive metadata match `pyproject.toml` and `server.json`
- Claude `scripts/build_mcpb.py` behavior still passes its existing checks
- any new Codex plugin builder output is deterministic and repo-local

## Out of Scope for v1

- private runtime bundling for Codex
- replacing the Claude `.mcpb`
- migrating Codex to historical OpenAI plugin formats
- adopting `tooluniverse-mcpb/codex-code-agent-system` as the mandatory workflow

Use selected pieces of `codex-code-agent-system` only later if execution needs extra orchestration. Keep [`PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/PLAN.md) as the source of truth.
