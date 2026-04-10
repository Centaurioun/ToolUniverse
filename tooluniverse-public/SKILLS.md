# Skills Used For ToolUniverse

This bundle preserves the skills that mattered during the ToolUniverse MCPB and Codex plugin work.

## Public Skill Copies

The `skills/` folder contains public, relative-path copies of the most relevant ToolUniverse-specific skills:

- `tooluniverse-codex-plugin`
- `tooluniverse-research-intake`
- `tooluniverse-tool-discovery`
- `tooluniverse-troubleshooting`

These copies are written so they can be shared outside the repository without absolute repo paths.

## How They Were Used

- `tooluniverse-codex-plugin` kept the Codex plugin track focused on the plugin manifest, bundled MCP runtime, marketplace wiring, and build verification.
- `tooluniverse-research-intake` helped decide whether a request belonged in ToolUniverse before any tool was chosen.
- `tooluniverse-tool-discovery` enforced search-first, inspect-when-needed, execute-last behavior.
- `tooluniverse-troubleshooting` handled startup, timeout, config, and compact-mode failures without turning compact mode into a bug.

## Why They Matter In Future Projects

These skills are reusable patterns for any future ToolUniverse-style integration:

- they separate intent detection from tool execution
- they make compact mode a workflow feature instead of a limitation
- they keep plugin packaging and MCP runtime work from drifting apart
- they give future maintainers a documented path for debugging and validation

## Related System Skills Used During The Work

The following system skills were part of the process even though they are not copied here:

- `tooluniverse-codex-plugin`
- `test-driven-development`
- `writing-skills`
- `skill-creator`

In practice, they were used to:

- keep the plugin work on the Codex-plugin track
- write failing tests before behavior changes
- draft and tighten the bundled skills and docs
- bootstrap the first versions of the skill files

## Notes

If you only need a quick summary, start with `README.md` and `INSTALLATION.md`.
