# Project Map

Git commit: `4d668698`

## Directory Structure

- `src/tooluniverse/`: main package, CLI, MCP/SMCP server code, bundled data and runtime behavior.
- `scripts/`: repo utilities and release/build scripts, including the existing Claude MCPB builder.
- `skills/`: repo-local ToolUniverse skills; the new Codex plugin implementation skill lives here.
- `docs/`: user and developer documentation, including Claude/MCPB guides that must stay accurate.
- `tests/`: unit, integration, and example-driven regression coverage.
- `tooluniverse-mcpb/`: supporting research material, MCPB references, OpenAI docs mirror, and optional orchestration assets.
- `dist/`: generated artifacts; already contains MCPB output and will later hold the Codex plugin artifact.

## Key Files

- [`PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/PLAN.md): approved architecture and delivery plan.
- [`INTERIM_PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/INTERIM_PLAN.md): execution companion with step-by-step workflow.
- [`pyproject.toml`](/Users/centaurioun/Repos/ToolUniverse/pyproject.toml): package metadata and canonical package version.
- [`server.json`](/Users/centaurioun/Repos/ToolUniverse/server.json): MCP-facing metadata, compact-mode defaults, env var contract.
- [`src/tooluniverse/smcp_server.py`](/Users/centaurioun/Repos/ToolUniverse/src/tooluniverse/smcp_server.py): current stdio/http entrypoints and compact-mode behavior.
- [`scripts/build_mcpb.py`](/Users/centaurioun/Repos/ToolUniverse/scripts/build_mcpb.py): current Claude MCPB builder that must remain supported.
- [`skills/tooluniverse-codex-plugin/SKILL.md`](/Users/centaurioun/Repos/ToolUniverse/skills/tooluniverse-codex-plugin/SKILL.md): new project-specific implementation skill.

## Critical Constraints

- Codex target is a native plugin with `.codex-plugin/plugin.json` and `.mcp.json`, not a Codex-specific `.mcpb`.
- Claude `.mcpb` remains a supported artifact and cannot regress while adding Codex packaging.
- Version and descriptive metadata must stay aligned between `pyproject.toml`, `server.json`, and generated packaging outputs.
- Codex v1 wraps the existing ToolUniverse MCP launch contract; do not introduce private runtime bundling unless validation proves it is necessary.
- Compact mode stays enabled by default for Codex-facing MCP launch paths.
- Historical Codex prompt files under `tooluniverse-mcpb/MCP-creation-prompts/` are reference-only, not architecture authority.

## Hot Files

- [`PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/PLAN.md)
- [`INTERIM_PLAN.md`](/Users/centaurioun/Repos/ToolUniverse/INTERIM_PLAN.md)
- [`scripts/build_mcpb.py`](/Users/centaurioun/Repos/ToolUniverse/scripts/build_mcpb.py)
- [`src/tooluniverse/smcp_server.py`](/Users/centaurioun/Repos/ToolUniverse/src/tooluniverse/smcp_server.py)
- [`server.json`](/Users/centaurioun/Repos/ToolUniverse/server.json)
- [`pyproject.toml`](/Users/centaurioun/Repos/ToolUniverse/pyproject.toml)
- [`skills/tooluniverse-codex-plugin/SKILL.md`](/Users/centaurioun/Repos/ToolUniverse/skills/tooluniverse-codex-plugin/SKILL.md)
