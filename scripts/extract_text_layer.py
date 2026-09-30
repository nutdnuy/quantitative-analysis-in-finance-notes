#!/usr/bin/env python3
"""Prototype selectable chapter HTML from the supplied PDF's text runs.

The source PDF remains authoritative. This converter changes only legacy Thai
presentation glyph code points to their equivalent Unicode Thai characters.
Other private-use glyphs, especially in equations, are retained and reported
for review. It does not reword, translate, OCR, or reconstruct mathematics.

Usage:
    python3 scripts/extract_text_layer.py --output /private/tmp/qaf-text-layer
    python3 scripts/extract_text_layer.py --pages 10 11 200 --output /private/tmp/qaf-sample
    python3 scripts/extract_text_layer.py --text-only --output transcripts/source-drafts

Requires Poppler's ``pdftohtml`` command.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
PDF = ROOT / BOOK["source_pdf"]

# Windows Thai PUA presentation glyphs and their semantic Unicode characters.
# Source: https://linux.thai.net/~thep/th-otf/shaping.html#pua
THAI_PUA = {
    0xF700: 0x0E10,  # descenderless THO THAN
    0xF701: 0x0E34,  # SARA I
    0xF702: 0x0E35,  # SARA II
    0xF703: 0x0E36,  # SARA UE
    0xF704: 0x0E37,  # SARA UEE
    0xF705: 0x0E48,  # low-left MAI EK
    0xF706: 0x0E49,  # low-left MAI THO
    0xF707: 0x0E4A,
    0xF708: 0x0E4B,
    0xF709: 0x0E4C,
    0xF70A: 0x0E48,  # low MAI EK
    0xF70B: 0x0E49,  # low MAI THO
    0xF70C: 0x0E4A,
    0xF70D: 0x0E4B,
    0xF70E: 0x0E4C,
    0xF70F: 0x0E0D,  # descenderless YO YING
    0xF710: 0x0E31,  # left MAI HAN-AKAT
    0xF711: 0x0E4D,
    0xF712: 0x0E47,  # left MAITAIKHU
    0xF713: 0x0E48,
    0xF714: 0x0E49,
    0xF715: 0x0E4A,
    0xF716: 0x0E4B,
    0xF717: 0x0E4C,
    0xF718: 0x0E38,
    0xF719: 0x0E39,
    0xF71A: 0x0E3A,
}
THAI_TRANSLATION = str.maketrans(THAI_PUA)
MATH_FONT = re.compile(r"symbol|cambria.?math|euclid|mt-extra", re.I)


def normalize_thai(text: str) -> str:
    return text.translate(THAI_TRANSLATION)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inline_html(element: ET.Element) -> str:
    """Keep the source run's bold and italic tags while escaping its text."""
    result = html.escape(normalize_thai(element.text or ""), quote=False)
    for child in element:
        inner = inline_html(child)
        result += f"<{child.tag}>{inner}</{child.tag}>" if child.tag in {"b", "i", "u"} else inner
        result += html.escape(normalize_thai(child.tail or ""), quote=False)
    return result


def font_stack(family: str) -> str:
    family = family.lower()
    if "thai" in family or "sarabun" in family or "angsana" in family or "cordia" in family:
        return '"Noto Sans Thai", Tahoma, sans-serif'
    if "symbol" in family:
        return 'Symbol, "Times New Roman", serif'
    if "math" in family or "euclid" in family or "times" in family:
        return '"Times New Roman", serif'
    return 'Arial, sans-serif'


def is_pua(character: str) -> bool:
    return 0xE000 <= ord(character) <= 0xF8FF


def get_xml(first_page: int, last_page: int) -> ET.Element:
    command = [
        "pdftohtml", "-f", str(first_page), "-l", str(last_page),
        "-xml", "-stdout", "-i", str(PDF),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return ET.fromstring(completed.stdout)


def get_raw_page_text(page_number: int) -> str:
    command = [
        "pdftotext", "-f", str(page_number), "-l", str(page_number),
        "-raw", str(PDF), "-",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def math_regions(runs: list[dict]) -> list[dict]:
    """Return candidate symbol clusters; these need visual source review."""
    seeds = [run for run in runs if run["math_candidate"]]
    groups: list[list[dict]] = []
    for run in sorted(seeds, key=lambda item: (item["top"], item["left"])):
        matching = None
        for group in groups:
            right = max(member["left"] + member["width"] for member in group)
            bottom = max(member["top"] + member["height"] for member in group)
            left = min(member["left"] for member in group)
            top = min(member["top"] for member in group)
            if run["left"] <= right + 28 and run["left"] + run["width"] >= left - 28 and run["top"] <= bottom + 20 and run["top"] + run["height"] >= top - 20:
                matching = group
                break
        if matching is None:
            groups.append([run])
        else:
            matching.append(run)
    regions = []
    for group in groups:
        seed_count = len(group)
        # Include adjacent variables, subscripts, and numerals around a symbol.
        # These often use Times rather than a math-specific font in this PDF.
        selected = {run["index"] for run in group}
        changed = True
        while changed:
            changed = False
            left = min(run["left"] for run in group)
            top = min(run["top"] for run in group)
            right = max(run["left"] + run["width"] for run in group)
            bottom = max(run["top"] + run["height"] for run in group)
            middle = (top + bottom) / 2
            for run in runs:
                if run["index"] in selected or not run["text"].strip():
                    continue
                horizontal_gap = max(left - (run["left"] + run["width"]), run["left"] - right, 0)
                vertical_gap = abs(run["top"] + run["height"] / 2 - middle)
                if horizontal_gap <= 12 and vertical_gap <= 28:
                    group.append(run)
                    selected.add(run["index"])
                    changed = True
        left = min(run["left"] for run in group)
        top = min(run["top"] for run in group)
        right = max(run["left"] + run["width"] for run in group)
        bottom = max(run["top"] + run["height"] for run in group)
        regions.append({
            "left": left, "top": top, "width": right - left,
            "height": bottom - top, "seed_runs": seed_count,
            "candidate_runs": len(group),
        })
    unique = {}
    for region in regions:
        key = tuple(region[field] for field in ("left", "top", "width", "height"))
        if key not in unique:
            unique[key] = region
        else:
            unique[key]["seed_runs"] += region["seed_runs"]
    return list(unique.values())


def render_page(
    page: ET.Element, fonts: dict[str, dict[str, str]], counts: collections.Counter[int]
) -> tuple[str, dict]:
    page_number = int(page.attrib["number"])
    width = int(page.attrib["width"])
    height = int(page.attrib["height"])
    before_parts = []
    after_parts = []
    spans = []
    runs = []
    for index, element in enumerate(page.findall("text")):
        original = "".join(element.itertext())
        normalized = normalize_thai(original)
        before_parts.append(original)
        after_parts.append(normalized)
        for character in original:
            if is_pua(character):
                counts[ord(character)] += 1
        font = fonts[element.attrib["font"]]
        left = int(element.attrib["left"])
        top = int(element.attrib["top"])
        run_width = int(element.attrib["width"])
        run_height = int(element.attrib["height"])
        remaining_pua = any(is_pua(character) for character in normalized)
        math_candidate = bool(MATH_FONT.search(font.get("family", ""))) or remaining_pua
        run = {
            "index": index, "left": left, "top": top, "width": run_width,
            "height": run_height, "font": font.get("family", ""),
            "text": normalized,
            "math_candidate": math_candidate,
            "remaining_pua": remaining_pua,
        }
        runs.append(run)
        style = (
            f"left:{left}px;top:{top}px;width:{run_width}px;height:{run_height}px;"
            f"font-size:{int(font['size'])}px;font-family:{font_stack(font.get('family', ''))};"
            f"color:{font.get('color', '#111')};"
        )
        classes = "text-run" + (" math-candidate" if math_candidate else "")
        spans.append(
            f'<span class="{classes}" data-run="{index}" '
            f'data-bbox="{left},{top},{run_width},{run_height}" '
            f'style="{style}">{inline_html(element)}</span>'
        )
    before = "".join(before_parts)
    after = "".join(after_parts)
    if after != normalize_thai(before):
        raise ValueError(f"Text changed beyond Thai PUA mapping on PDF page {page_number}")
    regions = math_regions(runs)
    html_page = (
        f'<div class="page-scroll"><section class="pdf-page" id="pdf-page-{page_number}" '
        f'aria-label="PDF page {page_number}" data-source-page="{page_number}" '
        f'style="width:{width}px;height:{height}px">'
        + "\n".join(spans)
        + "</section></div>"
    )
    report = {
        "pdf_page": page_number,
        "page_size": {"width": width, "height": height},
        "text_runs": len(runs),
        "characters_before": len(before),
        "characters_after": len(after),
        "thai_pua_replaced": sum(character in THAI_PUA for character in map(ord, before)),
        "remaining_pua": sum(is_pua(character) for character in after),
        "original_text_sha256": digest(before),
        "normalized_text_sha256": digest(after),
        "math_candidate_regions": regions,
        "runs": runs,
    }
    return html_page, report


def document(chapter: dict, pages: list[str], source_hash: str) -> str:
    number = chapter["number"]
    title = f"บทที่ {number} {chapter['title']}"
    return f"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="source-pdf-sha256" content="{source_hash}">
  <title>{html.escape(title)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 24px; color: #1a1a1a; background: #e9e9e9; }}
    h1 {{ max-width: 774px; margin: 0 auto 24px; font: 600 26px/1.4 Tahoma,sans-serif; }}
    .page-scroll {{ max-width: 100%; overflow-x: auto; margin: 0 auto 24px; }}
    .pdf-page {{ position: relative; margin: 0 auto; background: white; box-shadow: 0 4px 18px #0002; }}
    .text-run {{ position: absolute; display: block; white-space: pre; line-height: 1; }}
    .math-candidate {{ /* Bboxes are listed in extraction-report.json for review. */ }}
  </style>
</head>
<body>
<h1>{html.escape(title)}</h1>
{''.join(pages)}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Temporary HTML output directory")
    parser.add_argument("--pages", nargs="+", type=int, help="Optional PDF pages to sample")
    parser.add_argument("--chapters", nargs="+", type=int, help="Optional chapter numbers to extract")
    parser.add_argument("--text-only", action="store_true", help="Write editing drafts and integrity report without HTML")
    args = parser.parse_args()
    if not PDF.is_file():
        raise FileNotFoundError(PDF)
    selected_pages = set(args.pages) if args.pages else None
    selected_chapters = set(args.chapters) if args.chapters else None
    chapter_ranges = {
        chapter["number"]: range(chapter["first_page"], chapter["last_page"] + 1)
        for chapter in BOOK["chapters"]
    }
    all_pages = set(page for page_range in chapter_ranges.values() for page in page_range)
    if selected_pages and not selected_pages <= all_pages:
        raise ValueError(f"Requested pages outside chapters: {sorted(selected_pages - all_pages)}")
    args.output.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(PDF.read_bytes()).hexdigest()
    counts: collections.Counter[int] = collections.Counter()
    report = {
        "source_pdf": BOOK["source_pdf"],
        "source_pdf_sha256": source_hash,
        "normalization": "Windows Thai PUA presentation glyphs to semantic Unicode only",
        "normalization_reference": "https://linux.thai.net/~thep/th-otf/shaping.html#pua",
        "reading_order_note": "Plain-text files retain Poppler raw extraction order and physical line breaks; equations require manual review.",
        "mode": "text-only" if args.text_only else "positioned-html-prototype",
        "human_verified": False,
        "sample_pages": sorted(selected_pages) if selected_pages else None,
        "chapters": [],
        "pages": [],
    }
    for chapter in BOOK["chapters"]:
        if selected_chapters and chapter["number"] not in selected_chapters:
            continue
        page_range = chapter_ranges[chapter["number"]]
        wanted = sorted(set(page_range) & selected_pages) if selected_pages else list(page_range)
        if not wanted:
            continue
        page_text_dir = args.output / "pages"
        page_text_dir.mkdir(exist_ok=True)
        if args.text_only:
            chapter_text_parts = []
            for page_number in wanted:
                original = get_raw_page_text(page_number)
                normalized = normalize_thai(original)
                if normalized != original.translate(THAI_TRANSLATION):
                    raise ValueError(f"Unexpected normalization on PDF page {page_number}")
                for character in original:
                    if is_pua(character):
                        counts[ord(character)] += 1
                (page_text_dir / f"pdf-page-{page_number:03d}.txt").write_text(normalized, encoding="utf-8")
                chapter_text_parts.append(normalized.rstrip("\f"))
                unresolved = collections.Counter(
                    f"U+{ord(character):04X}" for character in normalized if is_pua(character)
                )
                report["pages"].append({
                    "pdf_page": page_number,
                    "chapter": chapter["number"],
                    "characters_before": len(original),
                    "characters_after": len(normalized),
                    "thai_pua_replaced": sum(ord(character) in THAI_PUA for character in original),
                    "remaining_pua": sum(unresolved.values()),
                    "remaining_pua_codes": dict(sorted(unresolved.items())),
                    "original_text_sha256": digest(original),
                    "normalized_text_sha256": digest(normalized),
                    "draft_file": f"pages/pdf-page-{page_number:03d}.txt",
                })
            filename = f"chapter-{chapter['number']:02d}.txt"
            (args.output / filename).write_text("\f\n".join(chapter_text_parts), encoding="utf-8")
            report["chapters"].append({"number": chapter["number"], "file": filename, "pdf_pages": wanted})
            continue
        xml_root = get_xml(wanted[0], wanted[-1])
        page_elements = {int(page.attrib["number"]): page for page in xml_root.findall("page")}
        fonts = {
            font.attrib["id"]: font.attrib
            for page in xml_root.findall("page")
            for font in page.findall("fontspec")
        }
        missing = set(wanted) - page_elements.keys()
        if missing:
            raise ValueError(f"PDF extraction omitted pages: {sorted(missing)}")
        html_pages = []
        chapter_text_parts = []
        for page_number in wanted:
            html_page, page_report = render_page(page_elements[page_number], fonts, counts)
            html_pages.append(html_page)
            raw_text = normalize_thai(get_raw_page_text(page_number))
            (page_text_dir / f"pdf-page-{page_number:03d}.txt").write_text(raw_text, encoding="utf-8")
            chapter_text_parts.append(raw_text.rstrip("\f"))
            page_report["raw_text_sha256"] = digest(raw_text)
            page_report["raw_text_characters"] = len(raw_text)
            page_report["raw_text_remaining_pua"] = sum(is_pua(character) for character in raw_text)
            report["pages"].append(page_report)
        filename = f"chapter-{chapter['number']:02d}.html"
        (args.output / filename).write_text(document(chapter, html_pages, source_hash), encoding="utf-8")
        (args.output / f"chapter-{chapter['number']:02d}.txt").write_text(
            "\f\n".join(chapter_text_parts), encoding="utf-8"
        )
        report["chapters"].append({"number": chapter["number"], "file": filename, "pdf_pages": wanted})
    report["totals"] = {
        "pages": len(report["pages"]),
        "characters_before": sum(page["characters_before"] for page in report["pages"]),
        "thai_pua_replaced": sum(page["thai_pua_replaced"] for page in report["pages"]),
        "remaining_pua": sum(page["remaining_pua"] for page in report["pages"]),
    }
    if not args.text_only:
        report["totals"]["text_runs"] = sum(page["text_runs"] for page in report["pages"])
    report["pua_counts"] = {f"U+{code:04X}": count for code, count in sorted(counts.items())}
    report_name = "integrity-report.json" if args.text_only else "extraction-report.json"
    (args.output / report_name).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(report['chapters'])} chapters, {len(report['pages'])} pages to {args.output}")
    print(json.dumps(report["totals"], ensure_ascii=False))


if __name__ == "__main__":
    main()
