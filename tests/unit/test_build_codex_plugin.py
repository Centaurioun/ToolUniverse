"""Regression tests for the ToolUniverse Codex plugin builder."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import ModuleType


def _load_build_script() -> ModuleType:
    script_path = (
        Path(__file__).resolve().parents[2] / "scripts" / "build_codex_plugin.py"
    )
    assert script_path.exists(), f"expected build script at {script_path}"

    spec = importlib.util.spec_from_file_location("build_codex_plugin", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildCodexPluginTest(unittest.TestCase):
    def test_build_codex_plugin_emits_expected_repo_local_artifact(self):
        build_codex_plugin = _load_build_script()
        repo_root = Path(__file__).resolve().parents[2]
        expected_version = tomllib.loads((repo_root / "pyproject.toml").read_text("utf-8"))[
            "project"
        ]["version"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "dist"
            plugin_dir = build_codex_plugin.build_codex_plugin(output_root=output_root)

            self.assertEqual(plugin_dir, output_root / "tooluniverse")
            self.assertTrue(plugin_dir.exists())

            manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
            mcp_path = plugin_dir / ".mcp.json"
            readme_path = plugin_dir / "README.md"
            skills_dir = plugin_dir / "skills"
            assets_dir = plugin_dir / "assets"
            logo_path = assets_dir / "tooluniverse-logo.png"

            self.assertTrue(manifest_path.exists())
            self.assertTrue(mcp_path.exists())
            self.assertTrue(readme_path.exists())
            self.assertTrue(skills_dir.exists())
            self.assertTrue(assets_dir.exists())
            self.assertTrue(logo_path.exists())

            manifest = json.loads(manifest_path.read_text("utf-8"))
            mcp_config = json.loads(mcp_path.read_text("utf-8"))

            self.assertEqual(manifest["name"], "tooluniverse")
            self.assertEqual(manifest["version"], expected_version)
            self.assertEqual(manifest["mcpServers"], "./.mcp.json")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["author"]["name"], "MIMS Harvard")
            self.assertEqual(
                manifest["repository"], "https://github.com/mims-harvard/ToolUniverse"
            )
            self.assertEqual(manifest["interface"]["displayName"], "ToolUniverse")
            self.assertEqual(
                manifest["interface"]["composerIcon"], "./assets/tooluniverse-logo.png"
            )
            self.assertEqual(
                manifest["interface"]["logo"], "./assets/tooluniverse-logo.png"
            )

            server = mcp_config["mcpServers"]["tooluniverse"]
            self.assertEqual(server["command"], "uvx")
            self.assertIn("tooluniverse-smcp-stdio", server["args"])
            self.assertEqual(server["args"][-1], "--compact-mode")
            self.assertEqual(server["env"]["PYTHONIOENCODING"], "utf-8")
            self.assertIn("NCBI_API_KEY", server["env_vars"])
