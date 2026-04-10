# ToolUniverse Prompt Archive

This is a merged archive of the prompts used during the ToolUniverse MCPB and Codex plugin work.

Short, repeated prompts were combined into larger phases so the history is easier to read.

## 1. MCPB Discovery And Rebuild

This prompt combines the early exploration, unpacking, and packaging work that led to the MCPB route.

```text
Inspect the ToolUniverse MCPB artifacts, compare the bundle layout with the repository source tree, and determine whether ToolUniverse can be rebuilt as an Anthropic-style .mcpb bundle. Prefer a test-first implementation if the bundle shape can be reproduced, and leave the older unpacked-extension route as a fallback only.
```

## 2. Codex Plugin Implementation

This prompt combines the plugin architecture work, bundled skill creation, and repo-local marketplace setup.

```text
Use the ToolUniverse Codex plugin track to create the repo-local plugin bundle, add the bundled ToolUniverse-specific skills, wire the repo-local marketplace entry, and keep the Codex plugin wrapping the existing ToolUniverse MCP runtime instead of introducing a private runtime. Add regression tests before any behavior change and keep the plugin artifact deterministic.
```

## 3. Plugin Validation And Install Path

This prompt combines the plugin-only install work, local marketplace validation, and smoke testing.

```text
Verify the ToolUniverse plugin through the supported local Codex marketplace path, confirm it appears in the Plugins surface, and run a real biomedical smoke test through Codex using discovery-first behavior. If the UI cannot be driven directly, reduce the remaining manual steps to a short exact checklist and document the validated local install path.
```

## 4. Final Validation And Cleanup

This prompt combines the release cleanup, documentation polish, and final review pass.

```text
Polish the ToolUniverse Codex plugin docs and metadata, keep the release scope tightly focused on organization and clarity, and verify the plugin build, MCPB build, bundled skills, and local install path still work after cleanup. Summarize the final state clearly and call out any remaining manual UI-only check.
```

## 5. Public Release Kit

This prompt reflects the current request to create a shareable public bundle and a separate porting guide.

```text
Create a ToolUniverse-only public documentation bundle, copy the relevant skills into it with relative paths, include the logo asset where appropriate, write a beginner-friendly installation guide for macOS, Windows, Codex in VS Code, and the Codex app, and create a separate guide outside the repository that explains how to port ToolUniverse to other AI platforms.
```

## Notes

- The original long-form context still lives in `tooluniverse-mcpb/Chat with Codex about making ToolUniv.md`.
- The detailed prompt transcripts in the working chat were intentionally merged here to remove repetition.
