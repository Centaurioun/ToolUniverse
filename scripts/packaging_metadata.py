"""Shared packaging metadata helpers for ToolUniverse release artifacts."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import NamedTuple


REPO_ROOT = Path(__file__).resolve().parents[1]


class PackagingMetadata(NamedTuple):
    package_name: str
    display_name: str
    version: str
    description: str
    homepage: str
    repository_url: str
    author_name: str
    author_email: str
    author_url: str


def load_packaging_metadata(
    *,
    pyproject_path: Path | None = None,
    server_json_path: Path | None = None,
) -> PackagingMetadata:
    """Load the shared packaging metadata from repo sources."""

    pyproject_path = pyproject_path or (REPO_ROOT / "pyproject.toml")
    server_json_path = server_json_path or (REPO_ROOT / "server.json")

    pyproject = tomllib.loads(pyproject_path.read_text("utf-8"))
    server = json.loads(server_json_path.read_text("utf-8"))

    version = pyproject["project"]["version"]
    if version != server["version"]:
        raise ValueError(
            "pyproject.toml version and server.json version must match "
            f"(got {version!r} and {server['version']!r})"
        )

    return PackagingMetadata(
        package_name="tooluniverse",
        display_name="ToolUniverse",
        version=version,
        description=server["description"],
        homepage=server["websiteUrl"],
        repository_url=server["repository"]["url"],
        author_name="MIMS Harvard",
        author_email="shanghuagao@gmail.com",
        author_url="https://aiscientist.tools",
    )
