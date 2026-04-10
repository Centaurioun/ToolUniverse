---
name: tooluniverse-tool-discovery
description: "Use when ToolUniverse is already the right path and you need to choose the correct tool before execution."
---

# ToolUniverse Tool Discovery

Use this skill once a request has already been routed into ToolUniverse.

## Rule

Do not jump straight to execution when the tool choice is still ambiguous.

## Sequence

1. Search for the right tool.
2. Inspect tool details when needed.
3. Execute only after the choice is justified.

## Good Practice

- search first when the request is broad
- inspect when the name or parameters are unclear
- prefer the most specific tool that fits the task

## Why This Matters

Compact mode is expected behavior in the plugin. Discovery is what bridges user intent to the correct scientific tool.
