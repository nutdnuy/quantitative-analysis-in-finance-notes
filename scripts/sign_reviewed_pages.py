#!/usr/bin/env python3
"""Atomically record pages that a second reader checked against the source PDF.

Only pass page numbers after independent visual proof. The lock and atomic
replacement prevent concurrent reviewers from dropping each other's entries.

Example:
    python3 scripts/sign_reviewed_pages.py --pages 33-46 48-55
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "transcripts" / "reviewed-pages.json"
LOCK = ROOT / "transcripts" / ".reviewed-pages.lock"
PDF = ROOT / "assets" / "QAF-completed-handbook.pdf"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_pages(values: list[str]) -> list[int]:
    pages: set[int] = set()
    for value in values:
        if "-" in value:
            first, last = map(int, value.split("-", 1))
            if first > last:
                raise ValueError(f"Invalid page range: {value}")
            pages.update(range(first, last + 1))
        else:
            pages.add(int(value))
    if not pages or min(pages) < 1 or max(pages) > 407:
        raise ValueError("Page numbers must be between 1 and 407")
    return sorted(pages)


def manual_path(page: int, current: dict) -> Path:
    listed = current.get("manual_file")
    if listed:
        path = ROOT / listed
        if path.is_file():
            return path
    for suffix in ("html", "md"):
        path = ROOT / "transcripts" / "manual" / f"page-{page:03}.{suffix}"
        if path.is_file():
            return path
    raise FileNotFoundError(f"No manual transcript for PDF page {page}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", nargs="+", required=True, metavar="PAGE_OR_RANGE")
    args = parser.parse_args()
    pages = parse_pages(args.pages)

    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a+") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest["source_pdf_sha256"] != sha256(PDF):
            raise RuntimeError("Source PDF hash changed; recheck pages against this PDF")
        entries = manifest.setdefault("pages", {})
        for page in pages:
            path = manual_path(page, entries.get(str(page), {}))
            entries[str(page)] = {
                "manual_file": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
            }
        manifest["pages"] = dict(sorted(entries.items(), key=lambda item: int(item[0])))
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=MANIFEST.parent,
            prefix=".reviewed-pages-", suffix=".json", delete=False,
        ) as temp:
            json.dump(manifest, temp, ensure_ascii=False, indent=2)
            temp.write("\n")
            temp.flush()
            os.fsync(temp.fileno())
            temp_name = temp.name
        os.replace(temp_name, MANIFEST)
        fcntl.flock(guard, fcntl.LOCK_UN)
    print(f"Recorded {len(pages)} independently checked pages; {len(manifest['pages'])} total")


if __name__ == "__main__":
    main()
