"""Regression tests for the repo-local Codex marketplace file."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


class CodexMarketplaceTest(unittest.TestCase):
    def test_repo_local_marketplace_exposes_tooluniverse_plugin(self):
        repo_root = Path(__file__).resolve().parents[2]
        marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"

        self.assertTrue(marketplace_path.exists(), f"missing marketplace: {marketplace_path}")

        marketplace = json.loads(marketplace_path.read_text("utf-8"))
        self.assertEqual(marketplace["name"], "tooluniverse-local")
        self.assertEqual(marketplace["interface"]["displayName"], "ToolUniverse Local")

        self.assertEqual(len(marketplace["plugins"]), 1)
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "tooluniverse")
        self.assertEqual(plugin["source"]["source"], "local")
        self.assertEqual(plugin["source"]["path"], "./plugins/tooluniverse")
        self.assertEqual(plugin["policy"]["installation"], "AVAILABLE")
        self.assertEqual(plugin["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(plugin["category"], "Research")
