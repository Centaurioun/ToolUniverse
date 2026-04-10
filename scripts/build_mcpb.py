#!/usr/bin/env python3
"""Build the ToolUniverse MCPB bundle for Claude Desktop."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from packaging_metadata import PackagingMetadata, load_packaging_metadata


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_NAME = "tooluniverse"
MANIFEST_VERSION = "0.4"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "dist" / "mcpb"


def _load_server_metadata() -> dict[str, object]:
    return json.loads((REPO_ROOT / "server.json").read_text("utf-8"))


def _bundle_manifest(
    metadata: PackagingMetadata, server: dict[str, object]
) -> dict[str, object]:
    return {
        "manifest_version": MANIFEST_VERSION,
        "name": metadata.package_name,
        "display_name": metadata.display_name,
        "version": metadata.version,
        "description": metadata.description,
        "long_description": (
            "ToolUniverse packages 1000+ scientific tools for AI scientists "
            "and exposes them through MCP for local desktop assistants."
        ),
        "author": {
            "name": metadata.author_name,
            "email": metadata.author_email,
            "url": metadata.author_url,
        },
        "repository": {
            "type": "git",
            "url": metadata.repository_url,
        },
        "homepage": metadata.homepage,
        "documentation": "https://zitniklab.hms.harvard.edu/ToolUniverse/",
        "support": f"{metadata.repository_url}/issues",
        "icon": "icon.png",
        "server": {
            "type": "uv",
            "entry_point": "src/run_stdio.py",
            "mcp_config": {
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    "${__dirname}",
                    "--with",
                    ".",
                    "--python",
                    "3.12",
                    "${__dirname}${/}src${/}run_stdio.py",
                ],
                "env": {
                    "PYTHONPATH": "${__dirname}${/}src",
                    "TOOLUNIVERSE_STDIO_MODE": "1",
                    "PYTHONIOENCODING": "utf-8",
                },
            },
        },
        "prompts_generated": True,
        "compatibility": {
            "platforms": ["darwin", "win32", "linux"],
            "runtimes": {"python": ">=3.10,<3.14"},
        },
        "keywords": ["science", "tooluniverse", "bioinformatics", "mcp"],
        "license": "MIT",
    }


def _bundle_pyproject(version: str) -> str:
    return f"""[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "tooluniverse"
version = "{version}"
description = "ToolUniverse MCP Server - 1000+ scientific tools (Bundled Source)"
requires-python = ">=3.10,<3.14"
dependencies = [
    "requests>=2.32.0",
    "numpy>=2.2.0",
    "sympy>=1.12.0",
    "graphql-core>=3.2.0",
    "fastapi>=0.116.0",
    "uvicorn>=0.36.0",
    "pydantic>=2.11.0",
    "epam.indigo>=1.34.0",
    "networkx>=3.4.0",
    "openai>=1.107.0",
    "pyyaml>=6.0.0",
    "google-genai>=1.36.0",
    "google-generativeai>=0.7.2",
    "mcp[cli]>=1.9.3",
    "fastmcp>=2.12.3,<4.0.0",
    "xmltodict>=1.0.0",
    "lxml>=6.0.0",
    "huggingface_hub>=0.34.0",
    "jsonpath-ng>=1.6.0",
    "rcsb-api>=1.4.0",
    "fitz>=0.0.1.dev2",
    "pandas>=2.2.3",
    "setuptools>=70.0.0,<81.0.0",
    "pdfplumber>=0.11.0",
    "playwright>=1.55.0",
    "faiss-cpu==1.12.0",
    "flask>=2.0.0",
    "aiohttp",
    "beautifulsoup4>=4.12.0",
    "python-dotenv>=1.0.0",
    "markitdown[all]>=0.1.0",
    "psutil>=5.9.0",
    "ddgs>=9.0.0",
    "pip>=25.3",
    "jsonschema>=4.23.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
tooluniverse = ["data/*", "data/packages/*"]
"""


def _bundle_readme(version: str) -> str:
    return f"""# ToolUniverse MCPB

This bundle packages ToolUniverse {version} as a Claude-installable MCPB archive.

## What is included

- Bundled Python source under `src/tooluniverse/`
- A `uv`-based stdio entrypoint in `src/run_stdio.py`
- A manifest compatible with MCPB manifest version `0.4`

## Install

Open the generated `tooluniverse.mcpb` file in Claude Desktop or copy the
release folder into Claude's extension directory if you are testing locally.

## Runtime

- Python 3.12
- `uv` manages the bundle environment
"""


def _bundle_env_template() -> str:
    return """# API Keys for ToolUniverse
# Copy this file to .env and fill in your actual API keys

At least one of: OPENAI_API_KEY, AZURE_OPENAI_API_KEY, HF_TOKEN=your_api_key_here

BOLTZ_MCP_SERVER_HOST=your_api_key_here

EXPERT_FEEDBACK_MCP_SERVER_URL=your_api_key_here

HF_TOKEN=your_api_key_here

TXAGENT_MCP_SERVER_HOST=your_api_key_here

USPTO_API_KEY=your_api_key_here

USPTO_MCP_SERVER_HOST=your_api_key_here
"""


def _bundle_run_stdio() -> str:
    return """#!/usr/bin/env python3
\"\"\"Entry point for ToolUniverse MCP Server (stdio transport for Claude Desktop).\"\"\"

import sys

sys.argv = [sys.argv[0], "--compact-mode"]

from tooluniverse.smcp_server import run_stdio_server


if __name__ == "__main__":
    run_stdio_server()
"""


def _bundle_plugin_stub(metadata: PackagingMetadata) -> str:
    return json.dumps(
        {
            "name": metadata.package_name,
            "version": metadata.version,
            "description": "ToolUniverse MCPB release bundle",
            "author": {
                "name": metadata.author_name,
                "url": metadata.author_url,
            },
            "mcpServers": "tooluniverse.mcpb",
        },
        indent=2,
    )


def _copy_source_tree(stage_dir: Path) -> None:
    source_root = REPO_ROOT / "src" / "tooluniverse"
    bundle_source_root = stage_dir / "src" / "tooluniverse"
    shutil.copytree(
        source_root,
        bundle_source_root,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            ".DS_Store",
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".venv",
            "dist",
            "build",
            "*.egg-info",
            ".env.template",
        ),
    )
    for path in bundle_source_root.rglob("*"):
        if path.is_file() and (
            path.name == ".DS_Store" or path.name == ".env.template"
        ):
            path.unlink()


def _stage_bundle(
    metadata: PackagingMetadata, server: dict[str, object], stage_dir: Path
) -> None:
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / "src").mkdir(parents=True, exist_ok=True)
    (stage_dir / "manifest.json").write_text(
        json.dumps(_bundle_manifest(metadata, server), indent=2), encoding="utf-8"
    )
    (stage_dir / "pyproject.toml").write_text(
        _bundle_pyproject(metadata.version), encoding="utf-8"
    )
    (stage_dir / "README.md").write_text(
        _bundle_readme(metadata.version), encoding="utf-8"
    )
    (stage_dir / ".env.template").write_text(
        _bundle_env_template(), encoding="utf-8"
    )
    (stage_dir / "src" / "run_stdio.py").write_text(
        _bundle_run_stdio(), encoding="utf-8"
    )
    icon_source = REPO_ROOT / "docs" / "_static" / "logo.png"
    if not icon_source.exists():
        raise FileNotFoundError(f"missing icon source: {icon_source}")
    shutil.copy2(icon_source, stage_dir / "icon.png")
    _copy_source_tree(stage_dir)


def _write_bundle_zip(stage_dir: Path, bundle_path: Path) -> Path:
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage_dir.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, path.relative_to(stage_dir))
    return bundle_path


def build_mcpb_bundle(output_root: Path | str | None = None) -> Path:
    """Build the ToolUniverse MCPB bundle and return the zip path."""

    metadata = load_packaging_metadata()
    server = _load_server_metadata()
    root = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    release_dir = root / BUNDLE_NAME
    bundle_path = release_dir / f"{BUNDLE_NAME}.mcpb"
    plugin_dir = release_dir / ".claude-plugin"

    if release_dir.exists():
        shutil.rmtree(release_dir)
    plugin_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="tooluniverse-mcpb-") as tmpdir:
        stage_dir = Path(tmpdir) / BUNDLE_NAME
        _stage_bundle(metadata, server, stage_dir)
        _write_bundle_zip(stage_dir, bundle_path)

    (plugin_dir / "plugin.json").write_text(
        _bundle_plugin_stub(metadata), encoding="utf-8"
    )
    return bundle_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the ToolUniverse MCPB bundle")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory that will contain the release folder",
    )
    args = parser.parse_args(argv)

    bundle_path = build_mcpb_bundle(args.output_root)
    print(f"Built MCPB bundle: {bundle_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
