---
name: tooluniverse-research-intake
description: "Use at the start of the ToolUniverse workflow to decide whether a request belongs in the biomedical research path."
---

# ToolUniverse Research Intake

Use this skill when you need to decide whether a request should enter ToolUniverse.

## Route Into ToolUniverse For

- drugs, compounds, targets, mechanisms, approvals, or safety
- genes, proteins, variants, pathways, or molecular function
- diseases, phenotypes, biomarkers, or indications
- papers, literature, citations, or biomedical evidence
- clinical trials or biomedical databases

## Do Not Route Into ToolUniverse For

- plugin packaging work
- generic writing or coding tasks
- requests where the exact tool is already known

## Intake Flow

1. Decide whether the question is really biomedical and lookup-oriented.
2. If yes, move into ToolUniverse instead of guessing.
3. Hand off to `tooluniverse-tool-discovery`.

## Handoff Rule

Start with the request, not the tool name. The job of intake is to decide whether ToolUniverse is the right system to use.
