"""Tests for shared packaging metadata helpers."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import ModuleType


def _load_packaging_metadata_module() -> ModuleType:
    module_path = Path(__file__).resolve().parents[2] / "scripts" / "packaging_metadata.py"
    assert module_path.exists(), f"expected helper module at {module_path}"

    spec = importlib.util.spec_from_file_location("packaging_metadata", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackagingMetadataTest(unittest.TestCase):
    def test_load_shared_metadata_matches_repo_sources(self):
        packaging_metadata = _load_packaging_metadata_module()
        metadata = packaging_metadata.load_packaging_metadata()

        pyproject = tomllib.loads(
            (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text("utf-8")
        )
        server = json.loads(
            (Path(__file__).resolve().parents[2] / "server.json").read_text("utf-8")
        )

        self.assertEqual(metadata.version, pyproject["project"]["version"])
        self.assertEqual(metadata.version, server["version"])
        self.assertEqual(metadata.package_name, "tooluniverse")
        self.assertEqual(metadata.display_name, "ToolUniverse")
        self.assertEqual(metadata.description, server["description"])
        self.assertEqual(metadata.homepage, server["websiteUrl"])
        self.assertEqual(metadata.repository_url, server["repository"]["url"])
        self.assertEqual(metadata.author_name, "MIMS Harvard")
        self.assertEqual(metadata.author_email, "shanghuagao@gmail.com")
        self.assertEqual(metadata.author_url, "https://aiscientist.tools")

    def test_load_shared_metadata_rejects_version_mismatch(self):
        packaging_metadata = _load_packaging_metadata_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "pyproject.toml").write_text(
                "[project]\nname = 'tooluniverse'\nversion = '1.2.3'\n",
                encoding="utf-8",
            )
            (root / "server.json").write_text(
                json.dumps(
                    {
                        "version": "9.9.9",
                        "description": "desc",
                        "websiteUrl": "https://example.com",
                        "repository": {"url": "https://example.com/repo"},
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                packaging_metadata.load_packaging_metadata(
                    pyproject_path=root / "pyproject.toml",
                    server_json_path=root / "server.json",
                )
