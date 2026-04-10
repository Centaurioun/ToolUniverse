# ToolUniverse Codex Plugin

This directory contains the repo-local Codex plugin for ToolUniverse.

## What This Plugin Is

This plugin wraps the existing ToolUniverse MCP stdio runtime for Codex.

Preserved project constraints:

- Codex plugin wraps MCP
- Claude `.mcpb` remains supported as a separate artifact
- compact mode stays on by default
- v1 does not bundle a private runtime

## Included Files

- `.codex-plugin/plugin.json`: Codex plugin manifest
- `.mcp.json`: bundled MCP server configuration
- `skills/`: bundled ToolUniverse-specific Codex skills
- `assets/`: reserved plugin assets

## Build The Repo-Local Plugin Artifact

From the repository root:

```bash
python3 scripts/build_codex_plugin.py
```

Default output:

```text
dist/codex-plugin/tooluniverse/
```

To build into a temporary location:

```bash
python3 scripts/build_codex_plugin.py --output-root /tmp/tooluniverse-codex-plugin
```

## Expose The Plugin Through The Repo-Local Marketplace

This repository includes a repo-local marketplace file:

```text
.agents/plugins/marketplace.json
```

It exposes the plugin from this repo-relative path:

```text
./plugins/tooluniverse
```

This setup is repo-local. It does not modify home-directory Codex config or home-directory marketplace files.

## Supported Personal Local Install Path

For a user-local Codex plugin install, use the supported personal marketplace flow from the Codex plugin docs:

- copy the plugin bundle into `~/.codex/plugins/tooluniverse`
- add a personal marketplace entry in `~/.agents/plugins/marketplace.json`
- enable the plugin in `~/.codex/config.toml`
- allow Codex to load the installed local copy from:

```text
~/.codex/plugins/cache/<marketplace-name>/tooluniverse/local/
```

Validated local install used during this MVP:

- marketplace: `personal-local`
- source: `~/.codex/plugins/tooluniverse`
- installed copy: `~/.codex/plugins/cache/personal-local/tooluniverse/local`

## Expected MCP Launch Contract

The plugin uses this stdio launch path through `.mcp.json`:

```text
uvx --from tooluniverse tooluniverse-smcp-stdio --compact-mode
```

Expected properties:

- compact mode enabled
- explicit startup and tool timeouts
- API keys passed through by environment-variable name

## Bundled Skills

The bundled skills define the intended ToolUniverse workflow inside Codex:

- `tooluniverse-research-intake`
- `tooluniverse-tool-discovery`
- `tooluniverse-troubleshooting`

Expected flow:

1. recognize that the request belongs in ToolUniverse
2. search for the right tool first
3. inspect if the tool choice is still ambiguous
4. execute only after the tool selection is justified

## Install And Smoke Test In Codex

If the Codex product UI is available on the local machine:

1. Build the plugin artifact or use the repo-local plugin scaffold directly.
2. Either expose it through the repo-local marketplace or install it through the supported personal-local marketplace flow above.
3. Open Codex and navigate to Plugins.
4. Confirm `ToolUniverse` appears in the Plugins surface.
5. Enable or install the plugin if needed.
6. Start a fresh Codex thread.
7. Try a ToolUniverse-appropriate biomedical request such as:
   - `Find recent clinical trials for KRAS inhibitors.`
   - `What proteins interact with TP53?`
   - `Summarize biomedical evidence for a disease-gene association involving BRCA1.`
8. Confirm Codex follows the intended bundled-skill flow:
   - intake first
   - discovery before execution
   - compact-mode ToolUniverse workflow rather than direct exposure of all tools

Validated in this project:

- ToolUniverse appeared in the Plugins section
- Codex reported `ToolUniverse` as an available plugin alongside `GitHub`
- a direct Codex run used the installed ToolUniverse plugin path to:
  - discover the right TP53 interaction tool
  - inspect the tool definition
  - execute the tool successfully

## What Can Be Validated Without The Product UI

From the repository alone, you can validate:

- the plugin manifest exists and is version-aligned
- `.mcp.json` preserves the ToolUniverse compact-mode launch contract
- bundled skills exist and validate
- the builder emits a deterministic repo-local artifact
- the Claude `.mcpb` builder still works

Validated runtime path used in this MVP:

```bash
uvx --from tooluniverse tooluniverse-smcp-stdio --help
uvx --from tooluniverse tu find 'clinical trials KRAS inhibitors' --limit 5
uvx --from tooluniverse tu run search_clinical_trials query='KRAS inhibitor'
```

What may still be worth a final manual spot-check in the UI:

- open a fresh interactive Codex chat after restart
- run one biomedical request from the Plugins-enabled UI
- confirm the visible UX matches expectations for your local setup

## Known Limits For This MVP

- repo-local marketplace wiring is for local testing, not marketplace publication
- install visibility and install UX still require the Codex product UI
- v1 intentionally relies on the existing ToolUniverse runtime instead of a bundled private runtime
- local `uv run` execution from the repository may fail on macOS x86_64 because some transitive wheels are unavailable for that platform; the plugin contract itself uses the published `uvx --from tooluniverse ...` path instead

## Release Readiness Checklist

Before commit or review, confirm:

- the plugin builder succeeds
- the Claude `.mcpb` builder still succeeds
- the bundled skills validate
- the repo-local marketplace still points to `./plugins/tooluniverse`
- any remaining UI-only spot-check is explicitly tracked as optional follow-up
