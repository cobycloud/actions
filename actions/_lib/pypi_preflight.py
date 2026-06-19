#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def normalize_project(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def project_from_dist(path: Path) -> str:
    name = path.name
    if name.endswith(".whl"):
        return normalize_project(name.split("-", 1)[0])
    if name.endswith(".tar.gz"):
        return normalize_project(name[:-7].split("-", 1)[0])
    if name.endswith(".zip"):
        return normalize_project(name[:-4].split("-", 1)[0])
    raise ValueError(f"Unsupported Python distribution file: {path}")


def simple_base(repository_url: str) -> str:
    if "test.pypi.org" in repository_url:
        return "https://test.pypi.org/simple/"
    return "https://pypi.org/simple/"


def published_files(project: str, base_url: str) -> str:
    url = urllib.parse.urljoin(base_url, f"{project}/")
    request = urllib.request.Request(url, headers={"Accept": "text/html"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return html.unescape(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return ""
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Find Python distributions not already present on PyPI.")
    parser.add_argument("--packages-dir", required=True)
    parser.add_argument("--repository-url", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    packages_dir = Path(args.packages_dir)
    dists = sorted(path for path in packages_dir.iterdir() if path.is_file())
    if not dists:
        print(f"No Python distributions found in {packages_dir}.", file=sys.stderr)
        return 1

    base_url = simple_base(args.repository_url)
    pages: dict[str, str] = {}
    pending: list[Path] = []
    for dist in dists:
        project = project_from_dist(dist)
        page = pages.setdefault(project, published_files(project, base_url))
        filename = dist.name
        quoted = urllib.parse.quote(filename)
        if filename in page or quoted in page:
            print(f"::warning title=PyPI distribution already published::{filename} already exists for {project}; skipping")
            continue
        pending.append(dist)

    Path(args.output).write_text("\n".join(str(path) for path in pending), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
