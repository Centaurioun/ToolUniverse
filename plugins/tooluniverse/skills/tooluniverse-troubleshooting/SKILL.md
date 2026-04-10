---
name: tooluniverse-troubleshooting
description: "Use when Codex is troubleshooting the plugin-local ToolUniverse MCP workflow inside this repository. Prefer this skill for startup failures, missing or misconfigured API keys, timeout issues, compact-mode confusion, or cases where ToolUniverse execution went wrong because discovery was skipped or the wrong tool was selected."
---

# ToolUniverse Troubleshooting

Use this skill for failures inside the bundled ToolUniverse Codex plugin workflow.

## Check the Failure Type First

Classify the problem before changing anything:

- startup failure: the ToolUniverse MCP server does not launch cleanly
- configuration failure: required environment variables or API keys are missing or wrong
- timeout failure: the server starts but tool calls stall or time out
- workflow failure: the wrong ToolUniverse tool was chosen because discovery was skipped
- compact-mode confusion: the user expects direct access to more tools than the compact MCP surface exposes

## Troubleshooting Order

1. Confirm the plugin-local contract.
2. Confirm environment and keys.
3. Confirm timeouts and startup behavior.
4. Confirm discovery happened before execution.

Do not jump to runtime redesign. The preserved project constraints still apply:

- Codex plugin wraps MCP
- Claude `.mcpb` stays supported
- compact mode stays on by default
- v1 does not bundle a private runtime

## 1. Confirm the Plugin-Local Contract

Check the local plugin files first:

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `scripts/build_codex_plugin.py`

Verify that `.mcp.json` still launches ToolUniverse through the expected stdio path and still includes `--compact-mode`.

## 2. Confirm Environment and Keys

If startup succeeds but tool behavior is incomplete or degraded:

- check whether the relevant API key is actually present in the MCP environment
- prefer fixing the missing or incorrect key before changing code
- remember that many ToolUniverse capabilities are optional and degrade gracefully without all keys

Do not treat a missing optional key as proof that the plugin packaging is broken.

## 3. Confirm Timeouts

If the server starts but calls stall:

- inspect the startup timeout and tool timeout values in `.mcp.json`
- distinguish slow tool behavior from failed startup
- avoid increasing timeouts blindly before checking whether the wrong tool or wrong parameters were used

## 4. Confirm Discovery Before Execution

If the wrong result came back:

- check whether discovery happened before execution
- use the plugin’s discovery workflow instead of guessing a tool name
- inspect tool details when multiple candidates exist

Wrong tool choice is often a workflow error, not a runtime error.

## Compact-Mode Reminder

Compact mode is expected behavior, not a defect.

- the plugin intentionally exposes a small MCP surface
- discovery tools are supposed to bridge from user intent to the correct ToolUniverse tool
- do not “fix” compact mode by treating it as accidental reduction of capability

## Do Not Use This Skill For

- generic debugging unrelated to the ToolUniverse plugin
- Codex plugin packaging design decisions
- Claude-only MCPB failures
