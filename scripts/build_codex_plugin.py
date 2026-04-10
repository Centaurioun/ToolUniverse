#!/usr/bin/env python3
"""Build the repo-local ToolUniverse Codex plugin artifact."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from packaging_metadata import load_packaging_metadata


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "dist" / "codex-plugin"
SCAFFOLD_ROOT = REPO_ROOT / "plugins" / "tooluniverse"
SCAFFOLD_IGNORE = shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text("utf-8"))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _prepare_manifest() -> dict[str, object]:
    metadata = load_packaging_metadata()
    manifest = _load_json(SCAFFOLD_ROOT / ".codex-plugin" / "plugin.json")
    manifest["name"] = metadata.package_name
    manifest["version"] = metadata.version
    manifest["author"] = {
        "name": metadata.author_name,
        "email": metadata.author_email,
        "url": metadata.author_url,
    }
    manifest["homepage"] = metadata.homepage
    manifest["repository"] = metadata.repository_url
    manifest["mcpServers"] = "./.mcp.json"
    manifest["skills"] = "./skills/"
    interface = manifest.setdefault("interface", {})
    interface["displayName"] = metadata.display_name
    interface["developerName"] = metadata.author_name
    interface["websiteURL"] = metadata.homepage
    return manifest


def build_codex_plugin(output_root: Path | str | None = None) -> Path:
    """Build the repo-local Codex plugin artifact and return its directory."""

    root = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    plugin_dir = root / "tooluniverse"

    if not SCAFFOLD_ROOT.exists():
        raise FileNotFoundError(f"missing plugin scaffold: {SCAFFOLD_ROOT}")

    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    shutil.copytree(SCAFFOLD_ROOT, plugin_dir, ignore=SCAFFOLD_IGNORE)

    _write_json(plugin_dir / ".codex-plugin" / "plugin.json", _prepare_manifest())
    return plugin_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the ToolUniverse Codex plugin artifact"
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory that will contain the built plugin folder",
    )
    args = parser.parse_args(argv)

    plugin_dir = build_codex_plugin(args.output_root)
    print(f"Built Codex plugin: {plugin_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
