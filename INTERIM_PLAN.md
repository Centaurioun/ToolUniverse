# ToolUniverse Codex Plugin Interim Plan

This document is the execution companion to `PLAN.md`.

Use `PLAN.md` as the architectural source of truth.
Use this file as the practical workflow guide for what to do next, in what order,
and which skill or workflow to use at each step.

This plan assumes the decisions already made in `PLAN.md`:
- Codex plugin is the primary new deliverable
- Claude `.mcpb` remains supported
- v1 wraps the existing ToolUniverse MCP runtime instead of bundling a private runtime
- `tooluniverse-mcpb/codex-code-agent-system` is optional and deferred until later
- Gemini is out of scope

## Purpose

The goal of this interim plan is to reduce decision overhead during execution.

You should be able to follow this document step by step without having to
remember:
- which planning document matters
- which skill to use when
- when to ignore historical references
- when to start implementation
- when to adopt the optional orchestration system

## Ground Rules

1. `PLAN.md` stays the main plan document.
2. This file is the step-by-step workflow document.
3. Do not treat `tooluniverse-mcpb/MCP-creation-prompts/*Codex*` as current authority.
4. Current official Codex plugin docs override historical Codex prompt files.
5. Do not use Gemini.
6. Do not adopt `codex-code-agent-system` at the beginning.
7. Prefer repo-local assets, repo-local skills, and repo-local plugin scaffolding.
8. Keep changes incremental and verifiable.

## What To Ignore For Now

Ignore these until later unless they become directly necessary:
- `tooluniverse-mcpb/codex-code-agent-system/.plan-code-scripts/*`
- `tooluniverse-mcpb/MCP-creation-prompts/*Codex*`
- broad Copilot or multi-platform adaptation work
- private-runtime bundling for Codex
- any attempt to replace the existing Claude `.mcpb`

These are not banned forever. They are simply not first-step materials.

## Execution Order

### Step 1: Keep the current plan stable

Objective:
- Freeze the architectural decisions in `PLAN.md`
- Do not start implementation until the execution workflow is ready

Use:
- No new special skill needed beyond the normal planning workflow already completed

Exit criteria:
- `PLAN.md` remains the architecture source of truth
- this `INTERIM_PLAN.md` is present and accepted as the execution guide

### Step 2: Create the project-specific implementation skill

Objective:
- Create a repo-local skill dedicated to this project’s Codex plugin work

Target path:
- `skills/tooluniverse-codex-plugin/SKILL.md`

Companion metadata:
- `skills/tooluniverse-codex-plugin/agents/openai.yaml`

Primary skill to use while creating it:
- `skill-creator`

Secondary skill to use after the first draft exists:
- `writing-skills`

How to use them:
- Use `skill-creator` for structure, scope, references, and progressive disclosure
- Use `writing-skills` only as a review and tightening pass
- Do not let `writing-skills` redefine storage layout or force extra process docs

What this new skill must do:
- explain the ToolUniverse Codex plugin architecture
- point to current Codex plugin docs, not old OpenAI plugin docs
- point to current ToolUniverse runtime entrypoints and builders
- encode the chosen project decisions:
  - Codex plugin wraps MCP
  - Claude `.mcpb` stays
  - compact mode stays on by default
  - no private runtime bundling in v1

What this new skill must not do:
- it must not become a generic Codex plugin tutorial
- it must not duplicate `PLAN.md`
- it must not describe Claude `.mcpb` as the Codex target artifact
- it must not include unrelated Copilot guidance

Exit criteria:
- first draft of `skills/tooluniverse-codex-plugin/SKILL.md` exists
- first draft of `skills/tooluniverse-codex-plugin/agents/openai.yaml` exists
- the skill clearly matches this repo and this project only

### Step 3: Validate the new implementation skill

Objective:
- Confirm the new skill is usable before relying on it during implementation

Use:
- `writing-skills`

Validation focus:
- does the description trigger at the right moments
- is the skill too generic or too narrow
- does it point to the correct current docs and files
- does it avoid stale Codex assumptions
- does it help an implementer act correctly without rereading the whole repo

Do not:
- add large reference dumps unless clearly needed
- create extra documentation files that only restate the skill

Exit criteria:
- skill instructions are concise and specific
- `agents/openai.yaml` matches the final skill purpose
- the skill is ready to guide implementation work

### Step 4: Create the Codex plugin scaffold

Objective:
- Establish the actual plugin folder and manifest structure

Recommended target:
- `plugins/tooluniverse/`

Expected contents:
- `plugins/tooluniverse/.codex-plugin/plugin.json`
- `plugins/tooluniverse/.mcp.json`
- `plugins/tooluniverse/skills/`
- `plugins/tooluniverse/assets/`
- `plugins/tooluniverse/README.md`

Primary skill to use:
- `plugin-creator`

How to use it:
- use it for the initial Codex plugin skeleton only
- do not accept placeholder values as final
- immediately adapt the scaffold to match the decisions in `PLAN.md`

Important rule:
- the plugin is a Codex plugin that bundles MCP config
- it is not a Codex version of Claude’s `.mcpb`

Exit criteria:
- plugin scaffold exists in-repo
- manifest paths are valid
- the plugin is clearly separate from the Claude MCPB output

### Step 5: Build shared packaging helpers

Objective:
- remove metadata duplication between Claude and Codex packaging

Use:
- the new `tooluniverse-codex-plugin` implementation skill

Scope:
- shared version validation
- shared description/author/repository/homepage fields
- shared asset selection logic where practical
- shared runtime launch assumptions only where truly common

Do not:
- over-generalize early
- refactor unrelated runtime code
- attempt private-runtime packaging in this phase

Exit criteria:
- Codex and Claude builders can draw from shared metadata helpers
- no hardcoded version drift remains in new packaging logic

### Step 6: Implement the Codex plugin builder

Objective:
- add a dedicated builder for the Codex plugin artifact

Recommended builder:
- `scripts/build_codex_plugin.py`

Expected behavior:
- generate `.codex-plugin/plugin.json`
- generate `.mcp.json`
- stage required assets
- stage bundled ToolUniverse-specific skills
- write output to `dist/codex-plugin/tooluniverse/`
- optionally support generating repo-local marketplace wiring for testing

Use:
- the new `tooluniverse-codex-plugin` implementation skill

Do not:
- auto-install to home directories
- auto-edit user-level Codex config
- bundle a separate private ToolUniverse runtime yet

Exit criteria:
- a deterministic repo-local Codex plugin artifact is buildable

### Step 7: Keep the Claude builder working

Objective:
- protect the existing `.mcpb` release path while Codex support is added

Use:
- the new `tooluniverse-codex-plugin` implementation skill

Scope:
- keep `scripts/build_mcpb.py` working
- update it only where shared helper extraction requires it
- preserve current successful behavior

Do not:
- redesign the Claude bundle
- change its install model
- make Codex requirements drive Claude-specific regressions

Exit criteria:
- `tooluniverse.mcpb` still builds
- Codex plugin work has not broken Claude packaging

### Step 8: Add repo-local test and install wiring for Codex

Objective:
- make local Codex testing repeatable and repo-scoped

Recommended additions:
- repo-local marketplace entry in `.agents/plugins/marketplace.json`
- documentation for how to restart Codex and reinstall the local plugin

Use:
- `plugin-creator` only if it saves time for marketplace scaffolding
- otherwise use the project implementation skill

Important rule:
- keep testing repo-local
- do not rely on manual ad hoc home-directory edits as the primary workflow

Exit criteria:
- the plugin can appear in Codex through a local marketplace path
- install and re-install flow is documented and repeatable

### Step 9: Add tests and validation

Objective:
- verify both artifacts and the shared packaging rules

Use:
- `test-driven-development` if behavior changes are implemented in code
- `test-automation` if the work is mainly adding or organizing tests
- always finish with `verification-before-completion`

Validation categories:
- shared metadata validation
- Codex plugin manifest generation
- `.mcp.json` generation
- build output structure
- Codex plugin launch smoke tests
- Claude `.mcpb` regression coverage

Minimum required tests:
- version consistency across metadata sources
- Codex manifest path correctness
- `.mcp.json` contains the intended ToolUniverse server contract
- Claude bundle still emits expected files

Exit criteria:
- packaging changes are covered by automated checks where practical
- runtime smoke tests have been run for the Codex path

### Step 10: Manual Codex integration test

Objective:
- confirm that the built plugin works in real Codex UI

Use:
- no special skill required
- follow the repo-local marketplace test instructions

Checklist:
- build plugin
- restart Codex
- verify plugin appears under Plugins
- install it
- start a fresh thread
- confirm ToolUniverse-backed workflow is usable
- run one realistic scientific task end to end

Exit criteria:
- Codex plugin install works
- Codex can use ToolUniverse through the plugin-installed path

### Step 11: Only now decide whether to use `codex-code-agent-system`

Objective:
- decide whether the implementation is now large enough to benefit from file-driven orchestration

Use it only if:
- work is split into multiple independent tasks
- you want task-level run artifacts
- you want planner/worker separation
- you want structured `.plans/<change>/plan.json` execution

Do not use it if:
- implementation is still linear and manageable
- the plugin scaffold and builder work are still changing rapidly
- the overhead would be higher than the benefit

If we adopt parts of it, use only these first:
- `.plan-code-scripts/codex-orchestrate`
- `.plan-code-scripts/task_doctor.py`
- optionally `.plan-code-scripts/sync_plan.py`

Do not adopt first:
- Gemini review
- the full specflow process
- any workflow that replaces `PLAN.md`

Exit criteria:
- either we deliberately adopt selected orchestration pieces
- or we deliberately defer it and continue manually

## Which Skill To Use, In Plain Terms

Use this table as the simplest memory aid.

| Situation | Use |
|---|---|
| Creating the new project-specific implementation skill | `skill-creator` |
| Tightening and pressure-testing that skill | `writing-skills` |
| Creating the Codex plugin skeleton | `plugin-creator` |
| Implementing ToolUniverse-specific Codex plugin logic | `tooluniverse-codex-plugin` |
| Adding or adjusting tests | `test-driven-development` or `test-automation` |
| Final verification before claiming a stage is done | `verification-before-completion` |
| Optional multi-task execution later | selected parts of `codex-code-agent-system` |

## What You Should Do First

If you want the shortest possible instruction set, follow this order exactly:

1. Keep `PLAN.md` unchanged as the architecture source of truth.
2. Create `skills/tooluniverse-codex-plugin/SKILL.md` using `skill-creator`.
3. Create `skills/tooluniverse-codex-plugin/agents/openai.yaml`.
4. Review and tighten that skill using `writing-skills`.
5. Create `plugins/tooluniverse/` using `plugin-creator`.
6. Implement shared packaging helpers.
7. Implement `scripts/build_codex_plugin.py`.
8. Confirm `scripts/build_mcpb.py` still works.
9. Add tests.
10. Add repo-local marketplace install wiring.
11. Test in real Codex.
12. Only then decide whether to use parts of `codex-code-agent-system`.

## What We Are Explicitly Not Doing Yet

- no Gemini
- no Copilot adaptation
- no replacement of Claude `.mcpb`
- no attempt to make one artifact serve both Claude and Codex
- no private-runtime bundling for Codex v1
- no automatic home-directory installation during build

## Definition of Success For This Interim Plan

This interim plan has succeeded when:
- the new repo-local implementation skill exists and is validated
- the Codex plugin scaffold exists in the repo
- the Codex plugin builder exists
- Claude `.mcpb` still works
- local Codex plugin installation is testable through a repo-local workflow
- `PLAN.md` remains the stable architecture document
