---
name: tooluniverse-tool-discovery
description: "Use when Codex is working through the ToolUniverse plugin and needs to decide which ToolUniverse MCP tool to use for a scientific or biomedical task. Prefer this skill when the task starts with tool selection, tool lookup, parameter inspection, or choosing between search and execution inside the bundled ToolUniverse workflow."
---

# ToolUniverse Tool Discovery

Use this skill inside the bundled ToolUniverse Codex plugin workflow.

## Core Rule

Do not jump straight to execution when the correct ToolUniverse tool is not already obvious.

Use this sequence:

1. Search for the right tool first.
2. Inspect tool details when the name or parameters are still uncertain.
3. Execute only after the tool choice is justified.

## Workflow

### 1. Search

Start with ToolUniverse discovery tools to narrow the candidate set.

- Use natural-language search when the user describes a task or domain.
- Use text or prefix search when you already suspect a tool family or database.
- Keep compact mode in mind: the plugin exposes a small MCP surface by design, so discovery is part of the normal workflow, not a fallback.

### 2. Inspect

Before execution, inspect the selected tool when any of these are true:

- the tool name is similar to other candidates
- required parameters are unclear
- the expected output shape matters for the next step
- the user’s request could map to multiple databases or evidence sources

### 3. Execute

Execute only after discovery has reduced ambiguity.

- Prefer the most specific tool that matches the user’s task.
- If the request is still ambiguous, keep searching or inspect another candidate instead of guessing.
- Preserve the plugin design constraints: Codex plugin wraps MCP, Claude `.mcpb` remains separate, compact mode stays on, and v1 does not bundle a private runtime.

## Do Not Use This Skill For

- generic scientific analysis after the correct ToolUniverse tool is already selected
- Codex plugin packaging work such as `.codex-plugin/plugin.json` or `.mcp.json`
- Claude-only MCPB tasks

## Quick Check

Before moving on, confirm:

- discovery happened before execution
- the chosen tool matches the actual user task
- parameters were inspected if there was any ambiguity
