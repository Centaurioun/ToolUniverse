"""Regression tests for the ToolUniverse MCPB builder."""

from __future__ import annotations

import importlib.util
import json
import tomllib
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import ModuleType


def _load_build_script() -> ModuleType:
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "build_mcpb.py"
    assert script_path.exists(), f"expected build script at {script_path}"

    spec = importlib.util.spec_from_file_location("build_mcpb", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildMcpbBundleTest(unittest.TestCase):
    def test_build_mcpb_bundle_emits_zip_and_plugin_stub(self):
        build_mcpb = _load_build_script()
        expected_version = tomllib.loads(
            (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text("utf-8")
        )["project"]["version"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "dist"
            bundle_path = build_mcpb.build_mcpb_bundle(output_root=output_root)

            self.assertEqual(bundle_path.name, "tooluniverse.mcpb")
            self.assertTrue(bundle_path.exists())

            release_dir = output_root / "tooluniverse"
            plugin_path = release_dir / ".claude-plugin" / "plugin.json"
            self.assertTrue(plugin_path.exists())

            plugin_data = json.loads(plugin_path.read_text())
            self.assertEqual(plugin_data["name"], "tooluniverse")
            self.assertEqual(plugin_data["version"], expected_version)
            self.assertEqual(plugin_data["mcpServers"], "tooluniverse.mcpb")

            with zipfile.ZipFile(bundle_path) as archive:
                names = set(archive.namelist())
                self.assertIn("manifest.json", names)
                self.assertIn("pyproject.toml", names)
                self.assertIn("README.md", names)
                self.assertIn(".env.template", names)
                self.assertIn("icon.png", names)
                self.assertIn("src/run_stdio.py", names)

                manifest = json.loads(archive.read("manifest.json").decode("utf-8"))

            self.assertEqual(manifest["manifest_version"], "0.4")
            self.assertEqual(manifest["name"], "tooluniverse")
            self.assertEqual(manifest["display_name"], "ToolUniverse")
            self.assertEqual(manifest["version"], expected_version)
            self.assertEqual(manifest["server"]["type"], "uv")
            self.assertEqual(manifest["server"]["entry_point"], "src/run_stdio.py")

            args = manifest["server"]["mcp_config"]["args"]
            self.assertEqual(args[:4], ["run", "--directory", "${__dirname}", "--with"])
            self.assertIn("--python", args)
            self.assertIn("3.12", args)
            self.assertTrue(args[-1].endswith("src${/}run_stdio.py"))
