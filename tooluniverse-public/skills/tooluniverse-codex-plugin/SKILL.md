---
name: tooluniverse-codex-plugin
description: "Use when working on the ToolUniverse Codex plugin track: plugin manifest, MCP config, build scripts, marketplace wiring, or validation that the plugin still wraps the existing ToolUniverse MCP runtime."
---

# ToolUniverse Codex Plugin

Use this skill for the Codex plugin track that keeps ToolUniverse plugin-native while preserving the MCP-backed runtime.

## Use This Skill When

- editing the ToolUniverse plugin manifest
- editing the bundled MCP config
- validating the local marketplace path
- checking the bundled skills and plugin assets
- verifying the plugin build output

## Do Not Use This Skill When

- you are only working on the Claude MCPB bundle
- you are writing generic ToolUniverse runtime code
- you are not touching the plugin packaging path

## Preserve These Decisions

- Codex uses a native plugin wrapper around MCP
- Claude `.mcpb` remains supported
- compact mode stays on by default
- v1 does not bundle a private runtime

## Workflow

1. Confirm the current step in the plan or release notes.
2. Keep the plugin repo-local and deterministic.
3. Reuse the existing ToolUniverse stdio/MCP launch behavior.
4. Verify the smallest meaningful change first.

## Good Outcomes

- the plugin manifest is valid
- the bundled MCP path still launches ToolUniverse in compact mode
- the repo-local marketplace points at the plugin bundle
- the built artifact is reproducible
