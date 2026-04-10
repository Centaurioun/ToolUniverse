#!/usr/bin/env python3
"""Download OpenAI docs markdown pages listed in the local link files."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
REL_DOWNLOAD_ROOT = Path("tooluniverse-mcpb") / "openai-docs"
LINK_FILES = [
    REPO_ROOT / "tooluniverse-mcpb" / "openai-docs" / "openai-api-docs-md-links.md",
    REPO_ROOT / "tooluniverse-mcpb" / "openai-docs" / "openai-apps-sdk-docs-md-links.md",
]
DOWNLOAD_ROOT = REPO_ROOT / REL_DOWNLOAD_ROOT
USER_AGENT = "ToolUniverseOpenAIDocsDownloader/1.0"
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.5


class DownloadResult:
    """Outcome for a single attempted download."""

    def __init__(
        self,
        *,
        url: str,
        destination: Path,
        status: str,
        bytes_written: int = 0,
        error: str | None = None,
    ) -> None:
        self.url = url
        self.destination = destination
        self.status = status
        self.bytes_written = bytes_written
        self.error = error


def load_urls(link_file: Path) -> list[str]:
    """Return unique URLs in the order they appear in *link_file*."""

    seen: set[str] = set()
    urls: list[str] = []
    for line in link_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().strip("`")
        if not stripped.startswith("https://"):
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        urls.append(stripped)
    return urls


def destination_for_url(url: str, root: Path = REL_DOWNLOAD_ROOT) -> Path:
    """Map a docs URL to a location under the mirror root."""

    parsed = urlparse(url)
    if parsed.netloc not in {"developers.openai.com", "platform.openai.com"}:
        raise ValueError(f"unsupported host for docs mirror: {url}")
    relative = Path(parsed.path.lstrip("/"))
    return root / relative


def build_download_plan(urls: list[str]) -> dict[str, Path]:
    """Build a stable URL -> destination mapping."""

    return {url: destination_for_url(url) for url in urls}


def collect_all_urls() -> list[str]:
    """Read both link files and return a deduplicated URL list."""

    seen: set[str] = set()
    urls: list[str] = []
    for link_file in LINK_FILES:
        for url in load_urls(link_file):
            if url in seen:
                continue
            seen.add(url)
            urls.append(url)
    return urls


def fetch_markdown(url: str, timeout: float = 30.0) -> str:
    """Fetch a markdown page and decode it as text."""

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/markdown, text/plain, */*",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = response.read()
                encoding = response.headers.get_content_charset() or "utf-8"
                return payload.decode(encoding, errors="replace")
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt == MAX_RETRIES:
                break
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"failed to fetch {url}") from last_error


def write_markdown(destination: Path, content: str) -> int:
    """Write markdown content to *destination* and return the byte count."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return len(content.encode("utf-8"))


def download_one(
    url: str,
    *,
    root: Path = DOWNLOAD_ROOT,
    fetcher=fetch_markdown,
) -> DownloadResult:
    """Download one URL into the mirrored tree."""

    destination = destination_for_url(url, root=root)
    markdown = fetcher(url)
    bytes_written = write_markdown(destination, markdown)
    return DownloadResult(
        url=url,
        destination=destination,
        status="downloaded",
        bytes_written=bytes_written,
    )


def download_all(
    urls: list[str],
    *,
    root: Path = DOWNLOAD_ROOT,
    fetcher=fetch_markdown,
) -> list[DownloadResult]:
    """Download all URLs, collecting per-file success or failure results."""

    results: list[DownloadResult] = []
    for url in urls:
        try:
            result = download_one(url, root=root, fetcher=fetcher)
            results.append(result)
            print(f"downloaded {url} -> {result.destination}")
        except Exception as exc:  # noqa: BLE001
            result = DownloadResult(
                url=url,
                destination=destination_for_url(url, root=root),
                status="failed",
                error=str(exc),
            )
            results.append(result)
            print(f"failed {url}: {exc}", file=sys.stderr)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download OpenAI docs markdown pages into local folders"
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print the URL-to-path mapping and exit",
    )
    args = parser.parse_args(argv)

    urls = collect_all_urls()
    plan = build_download_plan(urls)
    if args.plan_only:
        for url, path in plan.items():
            print(f"{url} -> {path.as_posix()}")
        return 0

    results = download_all(urls)
    failures = [result for result in results if result.status == "failed"]
    if failures:
        print(f"{len(failures)} document(s) failed to download", file=sys.stderr)
        return 1
    print(f"downloaded {len(results)} document(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
