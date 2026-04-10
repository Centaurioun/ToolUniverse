"""Tests for the OpenAI docs download script."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


def _load_script() -> ModuleType:
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "download_openai_docs.py"
    assert script_path.exists(), f"expected script at {script_path}"

    spec = importlib.util.spec_from_file_location("download_openai_docs", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DownloadOpenAiDocsTest(unittest.TestCase):
    def test_destination_for_url_mirrors_remote_path(self):
        script = _load_script()
        url = "https://developers.openai.com/api/docs/guides/agents/quickstart.md"

        destination = script.destination_for_url(url)

        self.assertEqual(
            destination.as_posix(),
            "tooluniverse-mcpb/openai-docs/api/docs/guides/agents/quickstart.md",
        )

    def test_load_urls_dedupes_and_preserves_order(self):
        script = _load_script()

        with tempfile.TemporaryDirectory() as tmpdir:
            links_file = Path(tmpdir) / "links.md"
            links_file.write_text(
                "\n".join(
                    [
                        "`https://developers.openai.com/api/docs/quickstart.md`",
                        "`https://developers.openai.com/api/docs/models.md`",
                        "`https://developers.openai.com/api/docs/quickstart.md`",
                    ]
                ),
                encoding="utf-8",
            )

            urls = script.load_urls(links_file)

        self.assertEqual(
            urls,
            [
                "https://developers.openai.com/api/docs/quickstart.md",
                "https://developers.openai.com/api/docs/models.md",
            ],
        )

    def test_download_one_writes_markdown_into_mirrored_location(self):
        script = _load_script()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "mirror"

            def fake_fetcher(url: str) -> str:
                self.assertEqual(url, "https://developers.openai.com/api/docs/quickstart.md")
                return "# Quickstart\n"

            result = script.download_one(
                "https://developers.openai.com/api/docs/quickstart.md",
                root=root,
                fetcher=fake_fetcher,
            )

            expected = root / "api/docs/quickstart.md"
            self.assertEqual(result.status, "downloaded")
            self.assertEqual(result.destination, expected)
            self.assertTrue(expected.exists())
            self.assertEqual(expected.read_text(encoding="utf-8"), "# Quickstart\n")

    def test_download_all_continues_after_a_failure(self):
        script = _load_script()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "mirror"

            def fake_fetcher(url: str) -> str:
                if url.endswith("quickstart.md"):
                    return "# Quickstart\n"
                raise RuntimeError("boom")

            results = script.download_all(
                [
                    "https://developers.openai.com/api/docs/quickstart.md",
                    "https://developers.openai.com/api/docs/models.md",
                ],
                root=root,
                fetcher=fake_fetcher,
            )

            self.assertEqual([result.status for result in results], ["downloaded", "failed"])
            self.assertTrue((root / "api/docs/quickstart.md").exists())
            self.assertFalse((root / "api/docs/models.md").exists())

