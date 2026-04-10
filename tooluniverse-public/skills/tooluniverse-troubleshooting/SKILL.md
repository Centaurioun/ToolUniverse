---
name: tooluniverse-troubleshooting
description: "Use when the ToolUniverse plugin-local MCP workflow fails, times out, or behaves unexpectedly."
---

# ToolUniverse Troubleshooting

Use this skill for plugin-local ToolUniverse failures.

## Check The Failure Type

- startup failure
- configuration failure
- timeout failure
- workflow failure
- compact-mode confusion

## Troubleshooting Order

1. Confirm the plugin-local contract.
2. Confirm environment variables and keys.
3. Confirm startup and tool timeouts.
4. Confirm discovery happened before execution.

## Important Reminder

Compact mode is not a defect. The plugin intentionally exposes a small discovery surface first.

## Do Not Use This Skill For

- generic debugging unrelated to the ToolUniverse plugin
- Claude-only MCPB issues
- plugin packaging decisions
