---
name: tooluniverse-research-intake
description: "Use when Codex is working through the ToolUniverse plugin and must decide whether a user request belongs in the ToolUniverse biomedical workflow. Prefer this skill for questions about drugs, compounds, genes, proteins, diseases, phenotypes, papers, literature, biomedical evidence, clinical trials, or biomedical databases before any ToolUniverse tool has been selected."
---

# ToolUniverse Research Intake

Use this skill at the start of the bundled ToolUniverse Codex plugin workflow.

## Core Rule

Enter ToolUniverse when the user is asking for biomedical entities, biomedical evidence, or biomedical database lookups, and the request still needs the right ToolUniverse path chosen.

## Route Into ToolUniverse For

- drugs, compounds, targets, mechanisms, approvals, safety signals, or pharmacology
- genes, proteins, variants, pathways, or molecular function
- diseases, phenotypes, biomarkers, indications, or condition summaries
- papers, literature reviews, citations, or biomedical evidence gathering
- clinical-trial, registry, or biomedical-database questions

## Do Not Route Into ToolUniverse For

- Codex plugin packaging or builder work such as `.codex-plugin/plugin.json`, `.mcp.json`, or `scripts/build_codex_plugin.py`
- generic writing, planning, or coding tasks with no biomedical lookup need
- cases where the exact ToolUniverse tool is already chosen and intake is no longer the bottleneck

## Intake Workflow

1. Check whether the request is really biomedical and lookup-oriented.
2. If yes, move into the plugin-local ToolUniverse workflow instead of answering from guesswork.
3. Hand off to `$tooluniverse-tool-discovery` to search first, inspect if needed, and execute only after the right tool is justified.

## Handoff Pattern

Use this handoff when ToolUniverse is appropriate:

- recognize the request as a ToolUniverse candidate
- keep the preserved plugin constraints in mind:
  - Codex plugin wraps MCP
  - Claude `.mcpb` stays supported
  - compact mode stays on by default
  - v1 does not bundle a private runtime
- continue with discovery rather than guessing a database or tool name

## Quick Examples

- "Find recent clinical trials for KRAS inhibitors" -> route into ToolUniverse
- "What proteins interact with TP53?" -> route into ToolUniverse
- "Summarize evidence for a disease-gene association" -> route into ToolUniverse
- "Fix the plugin manifest version field" -> do not use this skill
