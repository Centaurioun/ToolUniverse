"""Regression tests for bundled ToolUniverse Codex plugin skills."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_build_codex_plugin import _load_build_script


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SKILLS_ROOT = REPO_ROOT / "plugins" / "tooluniverse" / "skills"
SKILL_VALIDATOR = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)


class BundledCodexPluginSkillsTest(unittest.TestCase):
    def test_bundled_plugin_skills_exist_and_validate(self):
        skill_dirs = [
            PLUGIN_SKILLS_ROOT / "tooluniverse-research-intake",
            PLUGIN_SKILLS_ROOT / "tooluniverse-tool-discovery",
            PLUGIN_SKILLS_ROOT / "tooluniverse-troubleshooting",
        ]

        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                self.assertTrue((skill_dir / "SKILL.md").exists())
                self.assertTrue((skill_dir / "agents" / "openai.yaml").exists())
                result = subprocess.run(
                    ["python3", str(SKILL_VALIDATOR), str(skill_dir)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=result.stdout + result.stderr,
                )
                self.assertIn("Skill is valid!", result.stdout)

    def test_builder_copies_bundled_skill_directories(self):
        build_codex_plugin = _load_build_script()

        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = build_codex_plugin.build_codex_plugin(
                output_root=Path(tmpdir) / "dist"
            )

            for skill_name in (
                "tooluniverse-research-intake",
                "tooluniverse-tool-discovery",
                "tooluniverse-troubleshooting",
            ):
                with self.subTest(skill=skill_name):
                    built_skill_dir = plugin_dir / "skills" / skill_name
                    self.assertTrue((built_skill_dir / "SKILL.md").exists())
                    self.assertTrue((built_skill_dir / "agents" / "openai.yaml").exists())

            self.assertFalse((plugin_dir / ".DS_Store").exists())


if __name__ == "__main__":
    unittest.main()
