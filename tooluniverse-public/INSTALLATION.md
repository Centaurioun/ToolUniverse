# ToolUniverse Installation And Setup Guide

This guide covers ToolUniverse on macOS, Windows, the Codex VS Code extension, and the Codex app.

## What ToolUniverse Is

ToolUniverse is a biomedical tool platform for drugs, genes, proteins, diseases, literature, clinical trials, and related databases.

For Codex users, the important part is:

- ToolUniverse can run as a normal MCP server
- ToolUniverse can also be installed as a Codex plugin
- the Codex plugin wraps the same MCP launch contract and keeps compact mode on by default

## Before You Start

You will usually need:

- Python 3.10 or newer
- `uv`
- Git
- one or more API keys if you want the richer databases and models to work
- Codex installed if you want the plugin path

If you only want to use ToolUniverse from the terminal, the plugin steps are optional.

## Safety And Warnings

Before you sync or install anything, check these points:

- do not commit real API keys, tokens, passwords, or `.env` files
- if Codex warns about missing marketplace entries or plugin visibility, refresh the app before changing code
- if Codex warns that ToolUniverse is only in `MCPs`, that means the standalone MCP path is active, not necessarily the plugin install path
- if a database-specific tool complains about a missing key, that is usually a configuration issue rather than a packaging bug
- if you see a path warning, confirm that the marketplace points at the correct local plugin folder

## macOS

### 1. Install prerequisites

```bash
brew install git uv
```

If you do not use Homebrew, install `uv` from the official installer and make sure `python3` is available.

### 2. Get the repository

Clone the repository and open it in Terminal:

```bash
git clone https://github.com/mims-harvard/ToolUniverse.git
cd ToolUniverse
```

### 3. Confirm the runtime works

```bash
uvx --from tooluniverse tooluniverse-smcp-stdio --help
```

If that command starts, the published runtime path is available.

### 4. Install API keys

Set the keys you need in your shell environment or in the Codex configuration you use.

At minimum, many users will want:

- `OPENAI_API_KEY`
- `NCBI_API_KEY`

Other keys are optional and depend on the tools you use.

### 5. Install ToolUniverse in Codex

If you want the Codex plugin experience, use the plugin install path:

1. Build or stage the plugin from `plugins/tooluniverse/`.
2. Make sure Codex can read the marketplace entry.
3. Open Codex and go to `Plugins`.
4. Enable `ToolUniverse`.
5. Start a fresh chat and try a biomedical question.

If you want the user-local install path that was validated in this project, the important locations are:

- `~/.agents/plugins/marketplace.json`
- `~/.codex/config.toml`
- `~/.codex/plugins/tooluniverse`
- `~/.codex/plugins/cache/personal-local/tooluniverse/local`

### 6. Troubleshooting on macOS

- If ToolUniverse does not show up in `Plugins`, restart Codex and check the marketplace entry again.
- If it shows up in `MCPs` but not `Plugins`, you are likely looking at a standalone MCP registration instead of the plugin install.
- If `uvx` fails, make sure `uv` is installed and on your `PATH`.
- If some databases fail, check the corresponding API keys.
- If Codex shows a warning about missing keys, keep the guide open and compare the key name exactly against the troubleshooting checklist.

## Windows

### 1. Install prerequisites

Open PowerShell and install the basics:

```powershell
winget install Git.Git
winget install Astral.uv
```

If you already have Git or `uv`, keep your existing install.

### 2. Get the repository

```powershell
git clone https://github.com/mims-harvard/ToolUniverse.git
cd ToolUniverse
```

### 3. Confirm the runtime works

```powershell
uvx --from tooluniverse tooluniverse-smcp-stdio --help
```

### 4. Configure Codex paths

On Windows, the user-local paths usually live under:

- `%USERPROFILE%\.agents\plugins\marketplace.json`
- `%USERPROFILE%\.codex\config.toml`
- `%USERPROFILE%\.codex\plugins\`

### 5. Install the plugin

Use the same plugin workflow as macOS:

1. Make sure the local marketplace points at `./plugins/tooluniverse` or the personal-local install path.
2. Open Codex.
3. Go to `Plugins`.
4. Enable `ToolUniverse`.
5. Restart Codex if needed.
6. Test with a biomedical query.

### 6. Troubleshooting on Windows

- If `uvx` is not recognized, reopen PowerShell after installing `uv`.
- If Codex does not refresh the plugin list, close and reopen the app.
- If the plugin appears but cannot run, check the environment variables first.
- If file paths look wrong, remember to use backslashes in PowerShell commands and the Windows user profile path.
- If Codex warns about personal info or secrets, remove them from the config or environment before syncing.

## Codex In VS Code

This is the main path if you use the Codex VS Code extension.

### 1. Open the repository

Open the ToolUniverse repository in VS Code.

### 2. Check the Plugins pane

Open Codex in VS Code and go to `Plugins`.

### 3. Confirm ToolUniverse is available

You should see `ToolUniverse` as a plugin if the local marketplace and personal install are wired correctly.

### 4. Enable it

If it is disabled, turn it on.

### 5. Start a fresh chat

Use a biomedical prompt such as:

- `Find recent clinical trials for KRAS inhibitors.`
- `What proteins interact with TP53?`
- `Summarize evidence for a disease-gene association involving BRCA1.`

### 6. What success looks like

Codex should:

- recognize the request as biomedical
- use ToolUniverse rather than guessing
- search for the right tool first
- inspect the tool if the choice is unclear
- execute only after the tool selection is justified

### 7. Troubleshooting in VS Code

- If ToolUniverse only appears in `MCPs`, you probably installed the standalone MCP server but not the plugin path.
- If the plugin is installed but not visible, reload the VS Code window.
- If the plugin is visible but fails on the first call, check the required API keys.
- If Codex warns about a missing plugin entry, verify the marketplace file and then restart VS Code.

## Codex App

The Codex app uses the same plugin concept, but the UI is separate from VS Code.

### 1. Open Codex

Start the Codex app and open `Plugins`.

### 2. Find ToolUniverse

Look for `ToolUniverse` in the plugin list or marketplace view.

### 3. Enable or install it

Turn it on if it is disabled, or install it if it is offered as available.

### 4. Test it

Start a new thread and use one of the sample biomedical prompts above.

### 5. Troubleshooting in the app

- Restart the app after changing local marketplace files.
- If the plugin still does not appear, verify the personal marketplace path and the local cache path.
- If the plugin works but the UI looks confusing, remember that `Plugins` is the install surface and `MCPs` may still show the bundled MCP server.
- If the app warns about secrets or private files, stop and move those values out of the repo before sharing it.

## What To Check If Something Feels Wrong

Use this short checklist:

1. Is `uvx --from tooluniverse tooluniverse-smcp-stdio --help` working?
2. Is the plugin visible in `Plugins`?
3. Is the correct marketplace file pointing to `./plugins/tooluniverse`?
4. Is the personal install path present under `~/.codex/plugins/cache/.../tooluniverse/local`?
5. Are the API keys available to the server?
6. Did you restart Codex after changing config?
7. Did Codex warn about secrets, and did you confirm the repo contains none before syncing?

## Recommended First Smoke Test

Try this prompt after install:

```text
What proteins interact with TP53?
```

If the plugin is healthy, Codex should use ToolUniverse discovery first and then call the appropriate biology tool.
