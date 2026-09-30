#!/usr/bin/env python3
"""Build selectable chapter fragments from page-by-page PDF transcripts.

The PDF is the authority. Manual pages count as reviewed only when their exact
file bytes and source PDF match the reviewed-page manifest. Other pages are
conspicuously marked as review drafts. The local preview may show drafts,
while public publishing is blocked by ``build_site.py`` until they are reviewed.
Uncertain equations are cropped from the source and embedded PDF illustrations
are retained rather than silently reconstructed.

Examples:
    python3 scripts/build_transcript.py --chapter 1 --pages 10 11 --drafts
    python3 scripts/build_transcript.py --chapter 1 --require-complete
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOK = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
SECTIONS = json.loads((ROOT / "sections.json").read_text(encoding="utf-8"))
SOURCE = ROOT / BOOK["source_pdf"]
TRANSCRIPTS = ROOT / "transcripts"
MANUAL = TRANSCRIPTS / "manual"
DRAFTS = TRANSCRIPTS / "drafts"
EXCERPTS = TRANSCRIPTS / "excerpts"
REVIEWED_MANIFEST = TRANSCRIPTS / "reviewed-pages.json"
FONT_LOOKUP: dict[str, dict[str, str]] = {}
PDF_READER = PdfReader(SOURCE)
SOURCE_SHA256 = "c74929f8e9137c2145427f537c81b578af6ba4727c77b7f1851480d1a770fa2c"
# Source-rendered blanks, individually checked against this exact PDF. Do not
# infer blankness merely from missing text, since a page can contain a diagram.
BLANK_SOURCE_PAGES = frozenset({47, 85, 91, 137, 141, 185, 215, 255, 259, 289, 333, 337, 387})

# Legacy Thai presentation code points used by the embedded THSarabunNew font.
# The draft normalizer alters glyph encoding only, never the source PDF.
THAI_PUA = str.maketrans({
    "\uf700": "ฐ", "\uf701": "ิ", "\uf702": "ี", "\uf703": "ึ",
    "\uf704": "ื", "\uf705": "่", "\uf706": "้", "\uf707": "๊",
    "\uf708": "๋", "\uf709": "์", "\uf70a": "่", "\uf70b": "้",
    "\uf70c": "๊", "\uf70d": "๋", "\uf70e": "์", "\uf70f": "ญ",
    "\uf710": "ั", "\uf711": "ํ", "\uf712": "็", "\uf713": "่",
    "\uf714": "้", "\uf715": "๊", "\uf716": "๋", "\uf717": "์",
    "\uf718": "ุ", "\uf719": "ู", "\uf71a": "ฺ",
})


def normalize_thai(value: str) -> str:
    return value.translate(THAI_PUA).replace("ํา", "ำ")


def source_pages(chapter: dict) -> dict[int, str]:
    first, last = chapter["first_page"], chapter["last_page"]
    result = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), "-raw", str(SOURCE), "-"],
        check=True, capture_output=True, text=True,
    )
    chunks = result.stdout.split("\f")
    if chunks and not chunks[-1].strip():
        chunks.pop()
    if len(chunks) != last - first + 1:
        raise ValueError(f"Expected {last - first + 1} pages, got {len(chunks)}")
    return {page: normalize_thai(chunk).strip() for page, chunk in enumerate(chunks, first)}


def draft_paragraphs(raw: str, page: int) -> str:
    """Join obvious prose wraps for editing; mark equations for visual review.

    The local ``--preview-draft`` build may display these as unverified work;
    the public build remains blocked until each page is signed off.
    """
    output: list[str] = [f"<!-- UNREVIEWED PDF page {page}; do not publish -->", ""]
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            output.extend([" ".join(paragraph), ""])
            paragraph.clear()

    for original in raw.splitlines():
        line = original.strip()
        if not line:
            flush()
            continue
        if re.match(r"^\d+\s+การวิเคราะห์เชิงปริมาณทางการเงิน$", line):
            continue  # running page header, not chapter body
        if re.match(r"^(?:\d+(?:\.\d+){1,2}\s+|บทนำ$|ตัวอย่าง\s+\d+\.\d+|วิธีทำ\s+)", line):
            flush()
            if re.match(r"^\d+(?:\.\d+){1,2}\s+", line):
                output.extend(["## " + line, ""])
            else:
                paragraph.append(line)
            continue
        # A short line of variables or equation operators is almost always a
        # fraction/superscript whose reading order pdftotext cannot preserve.
        if len(line) < 48 and re.search(r"[=∑∫√÷×]", line):
            flush()
            output.extend([
                f"[สมการ: ตรวจภาพ PDF หน้า {page} ก่อนถอดเป็น MathML]",
                f"[เปิดหน้าต้นฉบับ]({BOOK['source_pdf']}#page={page})", "",
            ])
            continue
        paragraph.append(line)
    flush()
    return "\n".join(output).rstrip() + "\n"


def write_drafts(chapter: dict) -> None:
    DRAFTS.mkdir(parents=True, exist_ok=True)
    for page, raw in source_pages(chapter).items():
        path = DRAFTS / f"page-{page:03d}.md"
        path.write_text(draft_paragraphs(raw, page), encoding="utf-8")


def inline_markdown(value: str) -> str:
    # This deliberately supports only the constructs used by reviewed source
    # pages: escaped text, italics, and nothing that could rewrite the prose.
    escaped = html.escape(value, quote=False)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)


def reviewed_markdown_to_html(source: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            joined = "\n".join(paragraph)
            blocks.append("<p>" + "<br>".join(inline_markdown(part.rstrip()) for part in joined.split("  \n")) + "</p>")
            paragraph.clear()

    for line in source.splitlines():
        if not line.strip():
            flush()
            continue
        match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if match:
            flush()
            level = min(6, len(match.group(1)))
            blocks.append(f"<h{level}>{inline_markdown(match.group(2))}</h{level}>")
        else:
            paragraph.append(line)
    flush()
    return "\n".join(blocks)


def reviewed_page(page: int) -> tuple[str, str] | None:
    html_path = MANUAL / f"page-{page:03d}.html"
    md_path = MANUAL / f"page-{page:03d}.md"
    if html_path.is_file():
        return html_path.read_text(encoding="utf-8").strip(), str(html_path.relative_to(ROOT))
    if md_path.is_file():
        return reviewed_markdown_to_html(md_path.read_text(encoding="utf-8")), str(md_path.relative_to(ROOT))
    return None


def signed_off_page(page: int, file_name: str, source_hash: str, manifest: dict) -> bool:
    """A manual override is reviewed only when its signed-off bytes still match."""
    if manifest.get("source_pdf_sha256") != source_hash:
        return False
    entry = manifest.get("pages", {}).get(str(page), {})
    return bool(
        entry.get("manual_file") == file_name
        and entry.get("sha256") == hashlib.sha256((ROOT / file_name).read_bytes()).hexdigest()
    )


def xml_pages(chapter: dict) -> dict[int, ET.Element]:
    result = subprocess.run(
        ["pdftohtml", "-f", str(chapter["first_page"]), "-l", str(chapter["last_page"]),
         "-xml", "-stdout", "-i", str(SOURCE)],
        check=True, capture_output=True, text=True,
    )
    root = ET.fromstring(result.stdout)
    FONT_LOOKUP.clear()
    FONT_LOOKUP.update({font.attrib["id"]: font.attrib for font in root.iter("fontspec")})
    return {int(page.attrib["number"]): page for page in root.findall("page")}


def page_lines(page: ET.Element) -> list[dict]:
    runs: list[dict] = []
    for element in page.findall("text"):
        raw = "".join(element.itertext())
        normalized = normalize_thai(raw)
        if not normalized:
            continue
        font = FONT_LOOKUP.get(element.attrib["font"], {})
        family = font.get("family", "")
        top = int(element.attrib["top"])
        if top < 82 and int(page.attrib["number"]) != 10:
            continue  # running page number and book title
        runs.append({
            "text": normalized, "top": top, "left": int(element.attrib["left"]),
            "width": int(element.attrib["width"]), "height": int(element.attrib["height"]),
            "family": family, "size": int(font.get("size", "0")),
            "bold": element.find("b") is not None,
            "italic": element.find("i") is not None,
        })
    lines: list[dict] = []
    for run in sorted(runs, key=lambda item: (item["top"], item["left"])):
        candidates = [line for line in lines if abs(line["top"] - run["top"]) <= 12]
        if candidates:
            line = min(candidates, key=lambda item: abs(item["top"] - run["top"]))
            line["runs"].append(run)
            line["top"] = min(line["top"], run["top"])
            line["bottom"] = max(line["bottom"], run["top"] + run["height"])
        else:
            lines.append({"top": run["top"], "bottom": run["top"] + run["height"], "runs": [run]})
    for line in lines:
        line["runs"].sort(key=lambda item: (item["left"], item["top"]))
        text_parts: list[str] = []
        previous_run: dict | None = None
        for run in line["runs"]:
            if previous_run and text_parts and not text_parts[-1].endswith((" ", "\t")) and not run["text"].startswith((" ", "\t")):
                gap = run["left"] - previous_run["left"] - previous_run["width"]
                if gap > max(5, min(run["size"], previous_run["size"]) * 0.28):
                    text_parts.append(" ")
            text_parts.append(run["text"])
            previous_run = run
        line["text"] = "".join(text_parts).strip()
        line["left"] = min(run["left"] for run in line["runs"])
        line["right"] = max(run["left"] + run["width"] for run in line["runs"])
        visible_runs = [run for run in line["runs"] if run["text"].strip()]
        line["bold"] = sum(run["bold"] for run in visible_runs) >= max(1, len(visible_runs) // 2)
        line["figure_caption"] = bool(
            visible_runs and visible_runs[0]["italic"]
            and re.match(r"^รูปที่\s*\d+\.\d+\b", line["text"])
            and line["left"] >= 120
        )
        line["uncertain"] = any(
            ("symbol" in run["family"].lower() or "math" in run["family"].lower()
             or "mt-extra" in run["family"].lower()
             or any(0xE000 <= ord(char) <= 0xF8FF for char in run["text"]))
            for run in line["runs"]
        ) or bool(re.search(r"[=∑∫√÷×]", line["text"]))
        # Raised/lowered mathematical characters often arrive in different
        # runs with small fonts; their pdftohtml text order is not dependable.
        if any(run["size"] < 20 and re.search(r"[A-Za-z0-9]", run["text"])
               for run in line["runs"]):
            line["uncertain"] = True
    lines.sort(key=lambda item: (item["top"], item["left"]))
    # A prose sentence can contain an italic variable or a superscript. That
    # makes its extraction "uncertain", but must not make adjacent displayed
    # equations swallow the sentence into one wide source image. Render the
    # original Thai runs as text and crop just the inline mathematical runs.
    page_width = int(page.attrib["width"])
    for line in lines:
        thai_letters = sum("\u0e01" <= char <= "\u0e5b" for char in line["text"])
        line["inline_prose"] = bool(
            thai_letters >= 20
            and line["left"] < page_width * 0.25
            and not re.search(r"[=∑∫√÷×≈]", line["text"])
            and any("thsarabun" not in run["family"].lower() for run in line["runs"])
        )
    # Fractions/subscripts occupy additional short visual rows. Fold a short
    # centered row into its adjacent uncertain equation before cropping.
    for index, line in enumerate(lines):
        if (not line["uncertain"] and re.fullmatch(r"[\d\s.−+]+", line["text"])
                and any(other["uncertain"] and not other["inline_prose"]
                        and abs(other["top"] - line["top"]) <= 32
                        for other in lines[max(0, index - 2):index + 3] if other is not line)):
            line["uncertain"] = True
        if (line["uncertain"] or line["inline_prose"]
                or line["left"] < page_width * 0.25 or len(line["text"]) > 70):
            continue
        if any(
            other["uncertain"] and not other["inline_prose"]
            and abs(other["top"] - line["top"]) <= 32
            for other in lines[max(0, index - 1):index + 2] if other is not line
        ):
            line["uncertain"] = True
    merged: list[dict] = []
    for line in lines:
        if (line["uncertain"] and not line["inline_prose"] and merged
                and merged[-1]["uncertain"] and not merged[-1]["inline_prose"]
                and line["top"] - merged[-1]["bottom"] <= 26):
            last = merged[-1]
            last["top"] = min(last["top"], line["top"])
            last["bottom"] = max(last["bottom"], line["bottom"])
            last["left"] = min(last["left"], line["left"])
            last["right"] = max(last["right"], line["right"])
            last["text"] += " " + line["text"]
            last["runs"].extend(line["runs"])
        else:
            merged.append(line)
    return merged


def excerpt_for(page: ET.Element, line: dict, index: int) -> str:
    number = int(page.attrib["number"])
    EXCERPTS.mkdir(parents=True, exist_ok=True)
    source = ROOT / "assets" / "pages" / f"page-{number:03d}.webp"
    target = EXCERPTS / f"page-{number:03d}-line-{index:02d}.webp"
    with Image.open(source) as image:
        scale_x = image.width / int(page.attrib["width"])
        scale_y = image.height / int(page.attrib["height"])
        # The merged glyph bounds include subscripts and fraction rows. Use a
        # tight margin so adjacent prose is not clipped into the excerpt.
        left = max(0, int((line["left"] - 18) * scale_x))
        right = min(image.width, int((line["right"] + 18) * scale_x))
        top = max(0, int((line["top"] - 1) * scale_y))
        bottom = min(image.height, int((line["bottom"] + 1) * scale_y))
        image.crop((left, top, right, bottom)).save(target, "WEBP", lossless=True)
    version = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
    return f"transcripts/excerpts/{target.name}?v={version}"


def inline_prose_for(page: ET.Element, line: dict, index: int) -> tuple[str, str]:
    """Keep source Thai selectable, using tiny source crops for inline math."""
    number = int(page.attrib["number"])
    runs = line["runs"]
    pieces: list[tuple[str, str | list[dict]]] = []
    previous: dict | None = None
    for run in runs:
        gap = run["left"] - previous["left"] - previous["width"] if previous else 0
        if (previous and gap > max(5, min(run["size"], previous["size"]) * 0.28)
                and not previous["text"].endswith((" ", "\t"))
                and not run["text"].startswith((" ", "\t"))):
            pieces.append(("text", " "))
        if "thsarabun" in run["family"].lower():
            pieces.append(("text", run["text"]))
        elif pieces and pieces[-1][0] == "math" and gap <= 10:
            math_runs = pieces[-1][1]
            assert isinstance(math_runs, list)
            math_runs.append(run)
        else:
            pieces.append(("math", [run]))
        previous = run

    html_parts: list[str] = []
    markdown_parts: list[str] = []
    math_number = 0
    source = ROOT / "assets" / "pages" / f"page-{number:03d}.webp"
    with Image.open(source) as image:
        scale_x = image.width / int(page.attrib["width"])
        scale_y = image.height / int(page.attrib["height"])
        for kind, content in pieces:
            if kind == "text":
                assert isinstance(content, str)
                html_parts.append(html.escape(content))
                markdown_parts.append(content)
                continue
            assert isinstance(content, list)
            math_number += 1
            left = min(run["left"] for run in content)
            right = max(run["left"] + run["width"] for run in content)
            top = min(run["top"] for run in content)
            bottom = max(run["top"] + run["height"] for run in content)
            box = (
                max(0, int((left - 2) * scale_x)),
                max(0, int((top - 2) * scale_y)),
                min(image.width, int((right + 2) * scale_x)),
                min(image.height, int((bottom + 2) * scale_y)),
            )
            target = EXCERPTS / f"page-{number:03d}-inline-{index:02d}-{math_number:02d}.webp"
            EXCERPTS.mkdir(parents=True, exist_ok=True)
            image.crop(box).save(target, "WEBP", lossless=True)
            version = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
            path = f"transcripts/excerpts/{target.name}?v={version}"
            html_parts.append(f'<img src="{path}" alt="สัญลักษณ์จากหน้าต้นฉบับ {number - 9}">')
            markdown_parts.append(
                f"![สัญลักษณ์จากหน้าต้นฉบับ {number - 9}](excerpts/{target.name})"
            )
    return "".join(html_parts).strip(), "".join(markdown_parts).strip()


def embedded_figures(page_number: int) -> list[str]:
    """Copy embedded PDF images as lossless assets, preserving diagram labels."""
    images = PDF_READER.pages[page_number - 1].images
    if not images:
        return []
    EXCERPTS.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    for number, image_file in enumerate(images, 1):
        target = EXCERPTS / f"page-{page_number:03d}-figure-{number:02d}.webp"
        with Image.open(BytesIO(image_file.data)) as image:
            image.save(target, "WEBP", lossless=True)
        paths.append(f"transcripts/excerpts/{target.name}")
    return paths


def figure_block(paths: list[str], page_number: int, caption: str | None = None) -> tuple[str, str]:
    caption_html = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
    images_html = "".join(
        f'<img src="{path}" alt="ภาพประกอบต้นฉบับหน้า {page_number - 9}" loading="lazy">'
        for path in paths
    )
    markup = (
        '<figure class="source-excerpt source-figure" data-figure-source="embedded-pdf-image">'
        f'<div class="source-figure-images">{images_html}</div>{caption_html}</figure>'
    )
    md = "\n\n".join(
        f"![ภาพประกอบต้นฉบับหน้า {page_number - 9}]({path.replace('transcripts/excerpts/', 'excerpts/', 1)})"
        for path in paths
    )
    if caption:
        md += f"\n\n{caption}"
    return markup, md


def vector_figure_for(page: ET.Element, caption: dict, label_lines: list[dict]) -> str:
    """Crop a plotted PDF vector figure that has no extractable image object."""
    number = int(page.attrib["number"])
    source = ROOT / "assets" / "pages" / f"page-{number:03d}.webp"
    target = EXCERPTS / f"page-{number:03d}-vector-01.webp"
    with Image.open(source) as image:
        scale_x = image.width / int(page.attrib["width"])
        scale_y = image.height / int(page.attrib["height"])
        left = max(0, int((min(line["left"] for line in label_lines) - 25) * scale_x))
        right = min(image.width, int((max(line["right"] for line in label_lines) + 25) * scale_x))
        top = max(0, int((min(line["top"] for line in label_lines) - 25) * scale_y))
        bottom = min(image.height, int((caption["top"] - 2) * scale_y))
        EXCERPTS.mkdir(parents=True, exist_ok=True)
        image.crop((left, top, right, bottom)).save(target, "WEBP", lossless=True)
    version = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
    return f"transcripts/excerpts/{target.name}?v={version}"


def auto_page(page: ET.Element, chapter: dict) -> tuple[str, str, int, int]:
    number = int(page.attrib["number"])
    is_chapter_opening = number == chapter["first_page"]
    lines = page_lines(page)
    top_sections = {item["number"] for item in SECTIONS[str(chapter["number"])] if item["number"]}
    figure_paths = embedded_figures(number)
    caption_lines = [line for line in lines if line.get("figure_caption")]
    caption_images: dict[int, list[str]] = {id(line): [] for line in caption_lines}
    if caption_lines:
        for image_index, image_path in enumerate(figure_paths):
            target_index = min(image_index * len(caption_lines) // len(figure_paths), len(caption_lines) - 1)
            caption_images[id(caption_lines[target_index])].append(image_path)
    vector_captions: dict[int, str] = {}
    vector_label_ids: set[int] = set()
    if not figure_paths:
        for caption in caption_lines:
            caption_index = lines.index(caption)
            labels: list[dict] = []
            for candidate in reversed(lines[:caption_index]):
                if sum("\u0e01" <= char <= "\u0e5b" for char in candidate["text"]) >= 8:
                    break
                if labels and labels[-1]["top"] - candidate["bottom"] > 45:
                    break
                labels.append(candidate)
            if len(labels) >= 2:
                vector_captions[id(caption)] = vector_figure_for(page, caption, labels)
                vector_label_ids.update(id(label) for label in labels)
    blocks: list[str] = [
        '<p class="transcript-page-header">ฉบับถอดข้อความอัตโนมัติ · ยังไม่ได้ตรวจเทียบทุกคำกับต้นฉบับ</p>'
    ]
    markdown: list[str] = [f"<!-- UNREVIEWED PDF page {number} -->", ""]
    prose: list[str] = []
    previous: dict | None = None
    uncertain_count = 0
    outline_mode = False
    opening_title = False

    def flush() -> None:
        if prose:
            sentence = "".join(prose).strip()
            if sentence:
                blocks.append(f"<p>{html.escape(sentence)}</p>")
                markdown.extend([sentence, ""])
            prose.clear()

    for index, line in enumerate(lines, 1):
        if id(line) in vector_label_ids:
            continue  # axis labels are present in the faithful source crop
        value = line["text"]
        if not value:
            continue
        if is_chapter_opening and re.match(rf"^บทที่\s+{chapter['number']}\b", value):
            # The chapter lede already contains this exact source title.
            opening_title = True
            continue
        if opening_title and not value.startswith("เนื้อหาประกอบด้วย") and line["top"] < 220:
            # A long chapter title can occupy another visual line (chapter 6).
            continue
        opening_title = False
        if is_chapter_opening and value.startswith("เนื้อหาประกอบด้วย"):
            flush()
            blocks.append('<div class="chapter-outline">')
            blocks.append(f'<p class="chapter-outline-title">{html.escape(value)}</p>')
            markdown.extend([value, ""])
            outline_mode = True
            previous = None
            continue
        if outline_mode and value == "บทนำ":
            flush()
            blocks.append("</div>")
            outline_mode = False
        elif outline_mode:
            if re.match(r"^\d+\.\d+\s+", value):
                blocks.append(f'<p class="chapter-outline-item">{html.escape(value)}</p>')
                markdown.extend([value, ""])
                previous = None
                continue
            blocks.append("</div>")
            outline_mode = False
        if line.get("figure_caption"):
            flush()
            attached = caption_images.get(id(line), [])
            if attached:
                markup, md = figure_block(attached, number, value)
                blocks.append(markup)
                markdown.extend([md, ""])
            elif id(line) in vector_captions:
                image = vector_captions[id(line)]
                blocks.append(
                    '<figure class="source-excerpt source-figure" data-figure-source="source-page-crop">'
                    f'<div class="source-figure-images"><img src="{image}" '
                    f'alt="ภาพประกอบต้นฉบับหน้า {number - 9}" loading="lazy"></div>'
                    f'<figcaption>{html.escape(value)}</figcaption></figure>'
                )
                markdown.extend([
                    f"![ภาพประกอบต้นฉบับหน้า {number - 9}]({image.split('?', 1)[0].replace('transcripts/excerpts/', 'excerpts/', 1)})",
                    "", value, "",
                ])
            else:
                blocks.append(f"<p>{html.escape(value)}</p>")
                markdown.extend([value, ""])
            previous = None
            continue
        if line.get("inline_prose"):
            flush()
            mixed_html, mixed_md = inline_prose_for(page, line, index)
            blocks.append(f'<p class="source-inline-prose">{mixed_html}</p>')
            markdown.extend([mixed_md, ""])
            previous = None
            continue
        if line["uncertain"]:
            flush()
            image = excerpt_for(page, line, index)
            blocks.append(
                '<figure class="source-excerpt equation">'
                f'<img src="{image}" alt="ข้อความหรือสมการจากหน้าต้นฉบับ {number - 9}">'
                f'<figcaption>ข้อความหรือสมการจากหน้าต้นฉบับ {number - 9}</figcaption>'
                '</figure>'
            )
            markdown_image = image.split("?", 1)[0].replace("transcripts/excerpts/", "excerpts/", 1)
            markdown.extend([f"![ข้อความหรือสมการจากหน้าต้นฉบับ {number - 9}]({markdown_image})", ""])
            uncertain_count += 1
            previous = None
            continue
        heading = re.match(r"^(\d+(?:\.\d+){1,2})\s+(.+)$", value)
        heading_number = heading.group(1) if heading else ""
        heading_parent = heading_number.rsplit(".", 1)[0] if heading_number.count(".") == 2 else heading_number
        if heading and line["bold"] and heading_parent in top_sections:
            flush()
            level = "h3" if heading.group(1).count(".") == 2 else "h2"
            blocks.append(f"<{level}>{html.escape(value)}</{level}>")
            markdown.extend([f"{'###' if level == 'h3' else '##'} {value}", ""])
            previous = None
            continue
        if value in {"บทนำ", "แบบฝึกหัด"} and line["bold"]:
            flush()
            blocks.append(f"<h2>{html.escape(value)}</h2>")
            markdown.extend([f"## {value}", ""])
            previous = None
            continue
        if re.match(r"^(ปีที่|งวดที่|เงินสดจ่าย|เงินสดรับ|เงินสดสุทธิ)(?:\s|$)", value):
            flush()
            blocks.append(f'<p class="source-table-row">{html.escape(value)}</p>')
            markdown.extend([value, ""])
            previous = None
            continue
        if previous and (line["top"] - previous["bottom"] > 20 or line["left"] > previous["left"] + 45):
            flush()
        elif prose:
            # A wrap may split Thai words, but concatenating can also create a
            # false new word (for example "6ตามลำดับ"). Keep a visible space
            # in this unreviewed draft so the boundary can be checked later.
            prose.append("" if prose[-1].endswith(" ") or value.startswith(" ") else " ")
        prose.append(value)
        previous = line
        if value.startswith(("ตัวอย่าง ", "วิธีทำ ")):
            flush()
            previous = None
    flush()
    if outline_mode:
        blocks.append("</div>")
    if figure_paths and not caption_lines:
        markup, md = figure_block(figure_paths, number)
        blocks.append(markup)
        markdown.extend([md, ""])
    if uncertain_count:
        image = f"assets/pages/page-{number:03d}.webp"
        blocks.append(
            '<details class="source-excerpt"><summary>ดูหน้าต้นฉบับเต็มสำหรับสมการและภาพประกอบ</summary>'
            f'<img src="{image}" alt="หน้าต้นฉบับ PDF {number}" loading="lazy">'
            '</details>'
        )
    return "\n".join(blocks), "\n".join(markdown), uncertain_count, len(figure_paths)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", type=int, help="Chapter number; default: every chapter")
    parser.add_argument("--pages", type=int, nargs="+", help="Selected PDF pages (requires --chapter)")
    parser.add_argument("--drafts", action="store_true", help="Write unreviewed pdftotext drafts for the whole chapter")
    parser.add_argument("--require-complete", action="store_true", help="Fail unless every chapter page is signed off in the reviewed-page manifest")
    args = parser.parse_args()
    if args.pages and args.chapter is None:
        parser.error("--pages requires --chapter")
    chapters = BOOK["chapters"] if args.chapter is None else [
        chapter for chapter in BOOK["chapters"] if chapter["number"] == args.chapter
    ]
    if not chapters:
        parser.error(f"Unknown chapter {args.chapter}")
    TRANSCRIPTS.mkdir(exist_ok=True)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    review_manifest = json.loads(REVIEWED_MANIFEST.read_text(encoding="utf-8")) if REVIEWED_MANIFEST.exists() else {}
    for chapter in chapters:
        if args.drafts:
            write_drafts(chapter)
        chapter_pages = set(range(chapter["first_page"], chapter["last_page"] + 1))
        selected = args.pages or sorted(chapter_pages)
        if not set(selected) <= chapter_pages:
            parser.error(f"Pages outside chapter {chapter['number']}: {sorted(set(selected) - chapter_pages)}")
        xml = xml_pages(chapter)
        parts: list[str] = []
        markdown_parts: list[str] = []
        covered: list[dict] = []
        unreviewed: list[dict] = []
        blank_pages: list[int] = []
        for page in selected:
            if source_hash == SOURCE_SHA256 and page in BLANK_SOURCE_PAGES:
                blank_pages.append(page)
                continue
            manual = reviewed_page(page)
            signed_off = False
            if manual is None:
                body, md, uncertain_count, figure_count = auto_page(xml[page], chapter)
                unreviewed.append({"pdf_page": page, "source_excerpts": uncertain_count,
                                   "embedded_figure_images": figure_count})
                markdown_parts.extend([f"<!-- PDF page {page}: automatic review draft -->", md, ""])
            else:
                body, file_name = manual
                signed_off = signed_off_page(page, file_name, source_hash, review_manifest)
                if signed_off:
                    covered.append({"pdf_page": page, "printed_page": page - 9, "reviewed_source": file_name})
                else:
                    unreviewed.append({"pdf_page": page, "manual_draft": file_name,
                                       "review_reason": "Pending independent source proofread or changed since sign-off"})
                    body = (
                        '<p class="transcript-page-header">ฉบับพิมพ์จากต้นฉบับ · '
                        'รอตรวจทานเทียบต้นฉบับอย่างอิสระ</p>\n' + body
                    )
                original = (ROOT / file_name).read_text(encoding="utf-8")
                state = "independently reviewed" if signed_off else "manual review draft"
                markdown_parts.extend([f"<!-- PDF page {page}: {state} -->", original, ""])
            href = f"{BOOK['source_pdf']}#page={page}"
            parts.append(
                f'<section class="transcript-page" id="page-{page:03d}" '
                f'data-source-page="{page}" data-review="{"reviewed" if signed_off else "draft"}">\n{body}\n'
                f'<p class="source-page-link"><a href="{html.escape(href, quote=True)}" '
                f'target="_blank" rel="noopener">เปิดหน้าต้นฉบับ {page - 9} ↗</a></p>\n'
                '</section>'
            )
        if args.require_complete and unreviewed:
            raise SystemExit(f"Chapter {chapter['number']}: {len(unreviewed)} pages still unreviewed")
        name = f"chapter-{chapter['number']:02d}"
        destination = TRANSCRIPTS / f"{name}.html"
        destination.write_text("\n".join(parts) + "\n", encoding="utf-8")
        (TRANSCRIPTS / f"{name}.md").write_text("\n".join(markdown_parts).rstrip() + "\n", encoding="utf-8")
        report = {
            "chapter": chapter["number"], "source_pdf": BOOK["source_pdf"],
            "source_sha256": source_hash, "selected_pages": selected,
            "reviewed": covered, "unreviewed": unreviewed,
            "blank_source_pages": blank_pages,
            "publishable_complete": len(unreviewed) == 0 and set(selected) == chapter_pages,
        }
        (TRANSCRIPTS / f"{name}.coverage.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{destination}: {len(covered)} reviewed pages; {len(unreviewed)} draft pages")


if __name__ == "__main__":
    main()
