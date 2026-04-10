# ToolUniverse for Codex: Plugin Wrapper Around Shared MCP Core

## Summary

Build a **Codex plugin** for ToolUniverse, not a Codex-flavored `.mcpb`. The plugin will package:
- a `.codex-plugin/plugin.json` manifest for Codex install surfaces
- a `.mcp.json` that defines the bundled ToolUniverse MCP server for Codex
- optional skills that help Codex discover and use ToolUniverse effectively
- shared metadata/build inputs reused with the existing Claude `.mcpb` pipeline

Keep the existing Claude `.mcpb` as a first-class artifact. The repo should produce two install targets from one shared source of truth:
- **Claude artifact:** `tooluniverse.mcpb`
- **Codex artifact:** a plugin directory suitable for repo or personal marketplace installation

## Phase 1: Architecture Reset and Source-of-Truth Cleanup

Lock the packaging model around current official surfaces, not the older prompt assumptions.
- Treat `tooluniverse-mcpb/MCP-creation-prompts/*Codex*` as historical reference only; they assume older “plugin vs MCP” boundaries and outdated OpenAI plugin docs.
- Define a single packaging truth table:
  - Claude uses `.mcpb`
  - Codex uses `.codex-plugin/plugin.json` plus `.mcp.json`
  - Both launch the same ToolUniverse MCP server entrypoint
- Introduce one shared metadata layer for:
  - package name
  - display name
  - version
  - description
  - author/homepage/repository/license
  - icon asset mapping
  - runtime launch contract
- Preserve `pyproject.toml` and `server.json` as version inputs, but add a packaging metadata helper so Claude and Codex builders stop duplicating manifest text independently.

Important interface decision:
- Codex plugin does **not** embed ToolUniverse as a separate non-MCP “native plugin API”.
- Codex plugin bundles **MCP server config** and optional skills; ToolUniverse remains an MCP server operationally.

## Phase 2: Codex Plugin Spec

Create a new Codex plugin package in-repo with this shape:
- `plugins/tooluniverse-codex/.codex-plugin/plugin.json`
- `plugins/tooluniverse-codex/.mcp.json`
- `plugins/tooluniverse-codex/skills/...`
- `plugins/tooluniverse-codex/assets/...`
- optional docs/readme for install and troubleshooting

### `.codex-plugin/plugin.json`
Define a production plugin manifest with:
- `name`: stable kebab-case plugin id
- `version`: derived from repo version
- `description`
- `author`, `homepage`, `repository`, `license`, `keywords`
- `mcpServers`: `./.mcp.json`
- `skills`: `./skills/`
- `interface` block:
  - `displayName`
  - `shortDescription`
  - `longDescription`
  - `developerName`
  - `category`
  - `capabilities`
  - `defaultPrompt`
  - `brandColor`
  - `composerIcon`
  - `logo`
  - legal links if available

### `.mcp.json`
Bundle ToolUniverse as a Codex-managed MCP server.
- Use a named server id such as `tooluniverse`
- Point the command at the same launch path the repo already supports
- Prefer the packaged local runtime path if the Codex plugin distribution includes one; otherwise explicitly document the runtime dependency
- Include env passthrough/config strategy for keys such as `NCBI_API_KEY`
- Set timeout defaults appropriate for ToolUniverse startup and long-running tools
- Keep tool exposure broad by default, with an option to restrict via `enabled_tools` later if performance requires it

### Bundled skills
Add a small skill layer for Codex usability, not to replace the MCP server.
Recommended initial skills:
- `tooluniverse-research-intake`: route biomedical/scientific database tasks toward ToolUniverse first
- `tooluniverse-tool-discovery`: guide Codex to use ToolUniverse search/discovery patterns when the correct scientific tool is not obvious
- `tooluniverse-troubleshooting`: handle missing keys, startup failures, and slow tool responses

These skills should reference ToolUniverse behavior and common workflows, but avoid inventing wrapper code that duplicates MCP tool functionality.

## Phase 3: Shared Builder and Artifact Generation

Refactor packaging so Claude and Codex outputs share core staging logic.
- Extract shared packaging helpers from [scripts/build_mcpb.py](/Users/centaurioun/Repos/ToolUniverse/scripts/build_mcpb.py):
  - metadata loading
  - version validation
  - source-tree staging
  - asset selection
  - stdio entrypoint generation
- Add a dedicated Codex builder, for example `scripts/build_codex_plugin.py`
- Keep builders separate at the top level, but share:
  - version resolution
  - long description text
  - author/repository metadata
  - icon/logo assets
  - source launch contract
- Output locations:
  - Claude: `dist/mcpb/tooluniverse/tooluniverse.mcpb`
  - Codex: `dist/codex-plugin/tooluniverse/`
- Do not package the Codex artifact as `.mcpb`
- Add optional generation of a local marketplace file for testing:
  - repo-scoped: `.agents/plugins/marketplace.json`
  - personal-scoped example in docs only, not auto-written by default

## Phase 4: Runtime and Credential Strategy

Make runtime behavior explicit so Codex installs are reliable.
- Decide whether the Codex plugin’s `.mcp.json` launches:
  1. bundled source via `uv run --directory ...`
  2. an already-installed `uvx tooluniverse`
- Default choice: **bundle and launch from plugin-local source/runtime contract**, because it matches the “self-contained installable package” goal more closely and avoids hidden machine drift.
- Reuse the current ToolUniverse stdio entrypoint behavior already used by the Claude builder.
- Define credential handling:
  - required vs optional API keys
  - env names preserved exactly from current ToolUniverse expectations
  - no secrets in plugin manifests
  - docs for Codex-side configuration and marketplace install flow
- Add startup diagnostics guidance for:
  - missing `uv`
  - missing Python
  - env propagation failures
  - long startup times
  - tool timeout issues

## Phase 5: Validation and Test Plan

### Static validation
- Verify shared metadata version matches across:
  - `pyproject.toml`
  - `server.json`
  - Claude manifest
  - Codex `plugin.json`
- Validate the generated Codex plugin structure:
  - `.codex-plugin/plugin.json` exists
  - `.mcp.json` exists
  - manifest paths are relative and valid
  - asset references resolve
- Validate the Claude `.mcpb` build still succeeds unchanged in behavior

### Unit and builder tests
Add tests for:
- shared metadata generation
- Codex plugin manifest generation
- `.mcp.json` server config generation
- output folder structure
- path correctness and version propagation
- no stale hardcoded version strings

### Local runtime checks
Non-mutating or disposable checks for the built artifact:
- run the generated Codex plugin MCP launch command directly
- confirm ToolUniverse stdio server starts successfully
- confirm `tu --help` and the stdio entrypoint agree on runtime environment
- smoke test one or two ToolUniverse discovery calls through the MCP server path

### Codex integration tests
Test the Codex plugin in the actual install surface:
1. Build the plugin into `dist/codex-plugin/tooluniverse/`
2. Add a local marketplace entry
3. Restart Codex
4. Verify the plugin appears under Plugins
5. Install it from the marketplace
6. Start a fresh thread
7. Confirm the plugin is invokable and the bundled MCP server is available
8. Validate one end-to-end scientific task where Codex should prefer ToolUniverse

### Regression matrix
Cover:
- Claude `.mcpb` install still works
- Codex plain MCP config still works during migration
- Codex plugin install works from local marketplace
- version bump updates both artifacts consistently

## Phase 6: Documentation and Migration

Update repo docs to remove the current ambiguity between:
- raw CLI usage
- plain MCP server setup
- Claude `.mcpb`
- Codex plugin packaging

Add one canonical comparison page or section:
- CLI: local shell utility
- MCP server: direct tool surface for MCP-capable clients
- Claude `.mcpb`: Claude install artifact
- Codex plugin: Codex install artifact that bundles MCP config

Update the prompt/reference material under `tooluniverse-mcpb/` only where it prevents future mistakes.
- Mark old Codex prompt docs as historical or superseded
- Add references to current Codex plugin docs
- Do not treat `openai.yaml` or legacy OpenAI plugin manifests as the target architecture unless a specific Codex skill still requires them

## Acceptance Criteria

The work is complete when:
- ToolUniverse appears in Codex as an installable **plugin**, not only as a raw MCP server entry
- installing the Codex plugin results in a working bundled ToolUniverse MCP configuration
- a fresh Codex thread can use ToolUniverse through the plugin-installed flow
- the existing Claude `.mcpb` still builds and installs
- both artifacts derive version and descriptive metadata from shared repo sources
- docs clearly explain which artifact is for Claude and which is for Codex

## Assumptions and Defaults

- Primary target is a **Codex plugin** that bundles MCP config, not a Codex-specific `.mcpb`
- Claude `.mcpb` remains supported and shares core packaging inputs
- ToolUniverse remains an MCP server operationally; the Codex plugin is a packaging and discovery layer around it
- Local marketplace installation is the first supported Codex test path
- Official Codex plugin docs supersede the older `tooluniverse-mcpb/MCP-creation-prompts` assumptions where they conflict
