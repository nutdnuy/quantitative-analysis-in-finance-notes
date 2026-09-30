#!/usr/bin/env python3
"""Prepare source-faithful chapter PDFs, page images, and the printed TOC."""

from __future__ import annotations

import concurrent.futures
import json
import re
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
BOOK = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
SOURCE = ROOT / BOOK["source_pdf"]
PAGE_DIR = ROOT / "assets" / "pages"
CHAPTER_DIR = ROOT / "assets" / "chapters"
PARTS = [
    ("front-matter", BOOK["front_matter"]),
    *[(f"chapter-{chapter['number']:02d}", chapter) for chapter in BOOK["chapters"]],
    ("back-matter", BOOK["back_matter"]),
]

# The PDF's embedded Thai font uses presentation glyphs in Unicode's private
# area. This mapping is used for navigation text only. Page images and PDFs are
# rendered from the original file and are never reconstructed from extracted text.
THAI_PRESENTATION = str.maketrans({
    "\uf702": "ี", "\uf703": "ึ", "\uf704": "ื", "\uf706": "้",
    "\uf70a": "่", "\uf70b": "้", "\uf70e": "์", "\uf710": "ั", "\uf712": "็",
})


def normalize_heading(value: str) -> str:
    return value.translate(THAI_PRESENTATION).replace("ํา", "ำ").strip()


def extract_sections() -> None:
    toc = subprocess.check_output(
        ["pdftotext", "-f", "6", "-l", "8", "-layout", str(SOURCE), "-"],
        text=True,
    )
    sections: dict[str, list[dict[str, object]]] = {
        str(chapter["number"]): [] for chapter in BOOK["chapters"]
    }
    current = 0
    for line in toc.splitlines():
        chapter = re.match(r"^\s*บทที่\s+(\d+)\s+.+?\s+(\d+)\s*$", line)
        if chapter:
            current = int(chapter.group(1))
            continue
        match = re.match(r"^\s*(?:(\d+\.\d+)\s+)?(.+?)\s+(\d+)\s*$", line)
        if not match or not current:
            continue
        number, raw_title, printed = match.groups()
        if number and int(number.split(".")[0]) != current:
            continue
        if not number and "แบบฝ" not in raw_title:
            continue
        sections[str(current)].append({
            "number": number,
            "title": normalize_heading(raw_title),
            "printed_page": int(printed),
            "pdf_page": int(printed) + 9,
        })
    (ROOT / "sections.json").write_text(
        json.dumps(sections, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {sum(map(len, sections.values()))} section links")


def split_pdfs(reader: PdfReader) -> None:
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    for name, group in PARTS:
        target = CHAPTER_DIR / f"{name}.pdf"
        if target.exists():
            continue
        writer = PdfWriter()
        for page in range(group["first_page"], group["last_page"] + 1):
            writer.add_page(reader.pages[page - 1])
        with target.open("wb") as output:
            writer.write(output)
    print(f"Prepared {len(PARTS)} original-page PDF parts")


def render_part(part: tuple[str, dict]) -> None:
    name, group = part
    first, last = group["first_page"], group["last_page"]
    if all((PAGE_DIR / f"page-{page:03d}.webp").exists() for page in range(first, last + 1)):
        return
    part_pdf = CHAPTER_DIR / f"{name}.pdf"
    with tempfile.TemporaryDirectory() as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            ["pdftoppm", "-r", "140", "-png", str(part_pdf), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pngs = sorted(Path(temp_dir).glob("page-*.png"))
        if len(pngs) != last - first + 1:
            raise ValueError(f"{name}: expected {last - first + 1} renders, found {len(pngs)}")
        for page, png in enumerate(pngs, first):
            output = PAGE_DIR / f"page-{page:03d}.webp"
            if not output.exists():
                subprocess.run(
                    ["cwebp", "-quiet", "-lossless", str(png), "-o", str(output)],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
    print(f"Rendered {name}: PDF pages {first}–{last}", flush=True)


def main() -> None:
    reader = PdfReader(SOURCE)
    if len(reader.pages) != 407:
        raise ValueError(f"Expected 407 source pages, found {len(reader.pages)}")
    extract_sections()
    split_pdfs(reader)
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(render_part, PARTS))
    print(f"Prepared {len(list(PAGE_DIR.glob('page-*.webp')))} page images")


if __name__ == "__main__":
    main()
