# ToolUniverse Codex Plugin Plan, Revised

## Summary

Build a **Codex-native plugin** for ToolUniverse that bundles MCP configuration and ToolUniverse-specific skills, while keeping the existing Claude `.mcpb` build intact and supported.

Key decisions:
- **Primary target:** Codex plugin, not a Codex `.mcpb`
- **Claude support:** keep the existing `.mcpb` and share metadata/build logic where practical
- **Runtime strategy for v1:** wrap the existing ToolUniverse MCP launch path instead of embedding a separate private runtime
- **Tool exposure strategy:** keep ToolUniverse in `--compact-mode` by default and rely on search/execute flows instead of exposing 1000+ tools directly in Codex UI

## Why This Is the Best Design

- Codex plugins and Claude `.mcpb` bundles are different packaging systems. Trying to unify them into one artifact would create friction instead of reducing it.
- You already proved ToolUniverse works in Codex as a plain MCP server. The missing piece is Codex-native plugin packaging and install/discovery UX.
- The existing Claude `.mcpb` is already valuable and stable. Removing it would throw away working functionality for no gain.
- A plugin wrapper around the current MCP server is the fastest path to an integrated Codex experience with the lowest regression risk.
- A fully self-contained Codex runtime bundle should be deferred until after plugin install and usage are validated.

## Phase 1: Stabilize the Packaging Model

Create a single packaging architecture with two artifacts:
- **Claude artifact:** `tooluniverse.mcpb`
- **Codex artifact:** plugin folder with `.codex-plugin/plugin.json` and `.mcp.json`

Refactor packaging around shared metadata:
- Use `pyproject.toml` and `server.json` as the canonical version and descriptive inputs
- Add shared helper logic for version validation, description text, author/repository/homepage metadata, and asset selection
- Stop treating `tooluniverse-mcpb/MCP-creation-prompts/*Codex*` as active source material; mark them as historical references because they assume an older Codex model

## Phase 2: Codex Plugin MVP

Create a plugin under a repo-local path such as `plugins/tooluniverse/` with:
- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/`
- `assets/`
- `README.md`

### Plugin manifest
The plugin manifest should include:
- stable `name`
- repo-derived `version`
- `description`, `author`, `homepage`, `repository`, `license`, `keywords`
- `mcpServers: "./.mcp.json"`
- `skills: "./skills/"`
- `interface` metadata for Codex install surfaces

### MCP config
The plugin’s `.mcp.json` should define the ToolUniverse MCP server using the existing supported launch path.
Default v1 launch contract:
- use `uvx` or `uv run` with the current ToolUniverse stdio entrypoint
- pass `--compact-mode`
- preserve current env var names exactly
- set explicit startup and tool timeouts

Do **not** try to expose all ToolUniverse tools as first-class Codex plugin objects. Keep the server compact and let Codex use ToolUniverse’s own discovery/execution flow.

### Bundled skills
Add a small, high-signal skill layer:
- `tooluniverse-research-intake`
- `tooluniverse-tool-discovery`
- `tooluniverse-troubleshooting`

Purpose:
- help Codex recognize when ToolUniverse should be preferred
- teach the search → inspect → execute workflow
- reduce friction around missing keys, category loading, and startup failures

## Phase 3: Build and Install Workflow

Add a dedicated Codex plugin builder, separate from the Claude MCPB builder.
Recommended outputs:
- `dist/codex-plugin/tooluniverse/`
- `dist/mcpb/tooluniverse/tooluniverse.mcpb`

Builder responsibilities:
- generate `.codex-plugin/plugin.json`
- generate `.mcp.json`
- copy required assets and bundled skills
- derive version and metadata from shared helpers
- optionally generate a repo-local `.agents/plugins/marketplace.json` entry for testing

Do not auto-install into the user’s home directories during the build. Keep the builder deterministic and repo-scoped.

## Phase 4: New Agent and Skill for Implementation

When implementation starts, create a dedicated **repo-local Codex plugin development skill** and companion agent metadata for this work.

Recommended new skill:
- `skills/tooluniverse-codex-plugin/SKILL.md`

Recommended purpose:
- own the ToolUniverse Codex plugin architecture
- reference the shared packaging helpers, Codex plugin docs, Claude MCPB builder, and ToolUniverse MCP launch contract
- enforce the chosen design constraints:
  - plugin wrapper over MCP
  - Claude `.mcpb` retained
  - compact-mode default
  - no private runtime bundling in v1

Recommended companion agent metadata:
- `skills/tooluniverse-codex-plugin/agents/openai.yaml`

Recommended role guidance:
- plugin packaging specialist for Codex
- prefers Codex plugin docs over historical prompt files
- preserves shared metadata and avoids divergence between Codex and Claude packaging
- treats ToolUniverse runtime changes as out of scope unless required by validation failures

This is the right “new agent” to create for implementation. It should be focused on Codex packaging and install surfaces, not general ToolUniverse development.

## Phase 5: Validation

### Builder validation
- Codex plugin folder contains valid `.codex-plugin/plugin.json`
- `.mcp.json` exists and points at the intended MCP launch contract
- plugin version matches `pyproject.toml` and `server.json`
- Claude `.mcpb` build still passes

### Runtime validation
- launch the generated `.mcp.json` command directly
- confirm ToolUniverse stdio starts successfully in compact mode
- smoke test ToolUniverse discovery and execution through the MCP path

### Codex integration validation
- add repo-local marketplace entry
- restart Codex
- verify ToolUniverse appears under Plugins
- install the plugin from the marketplace
- start a fresh Codex thread
- confirm Codex can use ToolUniverse through the plugin-installed path
- validate one real scientific workflow end to end

### Regression validation
- existing plain MCP setup still works during migration
- Claude `.mcpb` still installs and runs
- Codex plugin build and install remain version-aligned with Claude artifact

## Phase 6: Documentation

Update docs to clearly separate:
- CLI usage
- plain MCP server setup
- Claude `.mcpb`
- Codex plugin

Add one canonical explanation:
- **CLI** is the local shell interface
- **MCP server** is the protocol/runtime interface
- **Claude `.mcpb`** is Claude’s install artifact
- **Codex plugin** is Codex’s install artifact and may bundle MCP config

Update the old Codex prompt/reference files only enough to mark them as superseded where they conflict with current official Codex plugin docs.

## Test Cases

- version mismatch between `pyproject.toml` and `server.json` fails build
- plugin manifest paths are all valid relative paths
- `.mcp.json` launches ToolUniverse with compact mode
- missing API keys still allow startup but degrade gracefully
- marketplace install shows ToolUniverse under Plugins
- Codex can invoke the plugin-installed ToolUniverse flow in a fresh thread
- Claude `.mcpb` remains buildable and installable

## Assumptions and Defaults

- Codex plugin is the primary new deliverable
- Claude `.mcpb` remains supported and is not removed
- v1 uses the existing ToolUniverse MCP launch path instead of bundling a private runtime
- compact mode stays enabled by default for Codex
- historical Codex prompt files are not authoritative where they conflict with current Codex docs
- if Codex plugin validation exposes runtime portability problems, runtime bundling becomes a phase-2 enhancement, not a phase-1 requirement
