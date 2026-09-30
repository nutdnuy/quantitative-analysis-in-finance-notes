#!/usr/bin/env python3
"""Build a source-faithful, chapter-by-chapter HTML lecture note."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
TRANSCRIPTS = ROOT / "transcripts"
BOOK = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
SECTIONS = json.loads((ROOT / "sections.json").read_text(encoding="utf-8"))
REPO = "https://github.com/nutdnuy/quantitative-analysis-in-finance-notes"
STYLE_VERSION = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:12]
PREVIEW_DRAFT = False
REVIEWED_PAGES = 0
UNREVIEWED_PAGES = 0
SUPPLEMENT_BLANK_PAGES = frozenset({5, 9, 393})
SUPPLEMENT_REVIEW: dict[int, bool] = {}


class TranscriptPageText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_page: int | None = None
        self.current_text: list[str] = []
        self.pages: dict[int, str] = {}
        self.in_annotation = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "annotation":
            self.in_annotation += 1
        if tag == "section" and values.get("data-source-page"):
            self.current_page = int(values["data-source-page"])
            self.current_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "annotation":
            self.in_annotation -= 1
        if tag == "section" and self.current_page is not None:
            self.pages[self.current_page] = " ".join("".join(self.current_text).split())
            self.current_page = None
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_page is not None and not self.in_annotation:
            self.current_text.append(data)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def chapter_file(number: int) -> str:
    return f"chapter-{number:02d}.html"


def original_pdf(page: int) -> str:
    return f"{BOOK['source_pdf']}#page={page}"


def sidebar(current: str, chapter_number: int | None) -> str:
    destinations = [("index.html", "Welcome", "home")]
    destinations += [
        (chapter_file(c["number"]), f"บทที่ {c['number']} {c['title']}", f"ch-{c['number']}")
        for c in BOOK["chapters"]
    ]
    destinations += [
        ("front-matter.html", BOOK["front_matter"]["title"], "front"),
        ("back-matter.html", BOOK["back_matter"]["title"], "back"),
    ]
    links = []
    for href, title, key in destinations:
        selected = key == current
        css = "book-link current" if selected else "book-link"
        aria = ' aria-current="page"' if selected else ""
        links.append(f'<a class="{css}" href="{href}"{aria}>{esc(title)}</a>')
    sections = ""
    if chapter_number is not None:
        section_links = []
        for section in SECTIONS[str(chapter_number)]:
            prefix = f"{section['number']} " if section["number"] else ""
            section_links.append(
                f'<a href="#page-{section["pdf_page"]:03d}">{esc(prefix + section["title"])}</a>'
            )
        sections = (
            '<details class="page-contents" open><summary>ในหน้านี้</summary>'
            f'<nav aria-label="หัวข้อในหน้านี้">{"".join(section_links)}</nav></details>'
        )
        download = (
            f'<a href="assets/chapters/chapter-{chapter_number:02d}.pdf" download>ดาวน์โหลด PDF บทนี้</a>'
            f'<a href="chapters/chapter-{chapter_number:02d}.md" download>ไฟล์ Markdown บทนี้</a>'
        )
    else:
        download = f'<a href="{esc(BOOK["source_pdf"])}" download>ดาวน์โหลด PDF ต้นฉบับ</a>'
    return f'''<aside id="book-sidebar" class="book-sidebar" aria-label="สารบัญหนังสือ">
      <a class="cover-link" href="index.html" aria-label="กลับหน้า Welcome"><img src="{esc(BOOK['cover_image'])}" alt="ปกหนังสือ {esc(BOOK['title_th'])}"></a>
      <a class="book-name" href="index.html">{esc(BOOK['title_th'])}</a>
      <button class="search-trigger" id="search-button" type="button"><span aria-hidden="true">⌕</span><span>Search</span><kbd>⌘ K</kbd></button>
      <nav class="book-nav" aria-label="สารบัญ">{"".join(links)}</nav>
      {sections}
      <div class="book-sidebar-footer">{download}<a href="{REPO}">GitHub</a><button id="theme-button" type="button">พื้นหลังมืด</button></div>
    </aside>'''


def shell(title: str, body: str, current: str, chapter_number: int | None = None) -> str:
    review_banner = (
        f'<div class="review-banner" role="status">ตัวอย่างก่อนขึ้น Git · {REVIEWED_PAGES} หน้าตรวจเทียบต้นฉบับแล้ว · '
        f'อีก {UNREVIEWED_PAGES} หน้าเป็นร่างข้อความที่ยังต้องตรวจทีละหน้า</div>'
        if PREVIEW_DRAFT else ""
    )
    return f'''<!doctype html>
<html lang="th" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{esc(BOOK['title_th'])} — หนังสือต้นฉบับแยกหน้าอ่านตามบท">
  <meta name="theme-color" content="#ffffff">
  <title>{esc(title)} · {esc(BOOK['title_th'])}</title>
  <link rel="stylesheet" href="styles.css?v={STYLE_VERSION}">
</head>
<body class="book">
  <a class="skip-link" href="#content">ข้ามไปเนื้อหา</a>
  <header class="book-mobile-header"><a href="index.html">{esc(BOOK['title_th'])}</a><button id="menu-button" aria-expanded="false" aria-controls="book-sidebar">สารบัญ</button></header>
  <div class="book-layout">
    {sidebar(current, chapter_number)}
    <main class="book-main" id="content">
      <div class="page-topline"><span>{esc(BOOK['title_en'])}</span><button id="print-button" type="button">พิมพ์หน้านี้</button></div>
      {review_banner}
      {body}
      <footer class="book-footer"><span>{esc(BOOK['title_th'])}</span><span>{esc(BOOK['author'])}</span></footer>
    </main>
  </div>
  <dialog id="search-dialog" aria-labelledby="search-title">
    <div class="search-dialog-heading"><h2 id="search-title">ค้นหาบทและหัวข้อ</h2><button id="close-search" type="button" aria-label="ปิดการค้นหา">ปิด</button></div>
    <label class="sr-only" for="search-input">คำค้นหา</label>
    <input id="search-input" type="search" placeholder="ค้นหาชื่อบทหรือหัวข้อ" autocomplete="off">
    <p id="search-status" role="status"></p><div id="search-results"></div>
  </dialog>
  <script src="search-index.js" defer></script>
  <script src="assets/reader.js" defer></script>
</body>
</html>
'''


def build_home() -> str:
    cards = []
    for chapter in BOOK["chapters"]:
        cards.append(
            f'<a class="lesson-card" href="{chapter_file(chapter["number"])}">'
            f'<span class="lesson-number">{chapter["number"]:02d}</span>'
            f'<span class="lesson-copy"><strong>{esc(chapter["title"])}</strong>'
            f'<small>หน้าพิมพ์ {chapter["printed_first"]}–{chapter["printed_last"]}</small></span>'
            '<span aria-hidden="true">→</span></a>'
        )
    body = f'''<article class="welcome-content">
      <h1>Welcome</h1>
      <p class="book-kicker">Lecture Notes · {esc(BOOK['edition'])}</p>
      <h2>{esc(BOOK['title_th'])}</h2>
      <p class="english-title">{esc(BOOK['title_en'])}</p>
      <p class="book-author">{esc(BOOK['author'])} · {esc(BOOK['year'])} · ISBN {esc(BOOK['isbn'])}</p>
      <p class="welcome-description">อ่านเนื้อหาหนังสือเป็นข้อความแยกตามบท พร้อมสารบัญหัวข้อและเลขหน้าตามต้นฉบับ</p>
      <div class="welcome-actions"><a class="primary-action" href="chapter-01.html">เริ่มจากบทแรก →</a><a href="#lessons">ดูบทเรียนทั้งหมด ↓</a></div>
      <div class="welcome-cover"><img src="{esc(BOOK['cover_image'])}" alt="ปกหนังสือ {esc(BOOK['title_th'])}"></div>
      <h2 id="lessons">เลือกบทเรียน</h2>
      <div class="lesson-list">{"".join(cards)}</div>
      <nav class="supplement-list" aria-label="ส่วนประกอบหนังสือ"><a href="front-matter.html">คำนำและสารบัญต้นฉบับ →</a><a href="back-matter.html">ภาคผนวก เอกสารอ้างอิง และดัชนี →</a></nav>
      <p class="source-note">ข้อความในบทถอดจาก PDF ต้นฉบับ มีลิงก์เปิดหน้าหนังสือเดิมทุกหน้าเพื่อเทียบถ้อยคำ สมการ และภาพประกอบ</p>
    </article>'''
    return shell("Welcome", body, "home")


def source_pages(first: int, last: int, numbered: bool = True) -> str:
    parts = []
    for page in range(first, last + 1):
        caption = f"หน้าพิมพ์ {page - 9}" if numbered else f"หน้า PDF {page}"
        parts.append(f'''<figure class="source-page" id="page-{page:03d}">
          <img src="assets/pages/page-{page:03d}.webp" alt="{esc(caption)} จากหนังสือต้นฉบับ" loading="lazy" decoding="async">
          <figcaption><span>{esc(caption)}</span><a href="{esc(original_pdf(page))}" target="_blank" rel="noopener">เปิดหน้าต้นฉบับ ↗</a></figcaption>
        </figure>''')
    return "".join(parts)


def pager(previous: str, next_page: str) -> str:
    return f'<nav class="chapter-pager" aria-label="เปลี่ยนบท"><a href="{previous}">← ก่อนหน้า</a><a href="{next_page}">ถัดไป →</a></nav>'


def build_chapter(chapter: dict) -> str:
    number = chapter["number"]
    title = f"บทที่ {number} {chapter['title']}"
    previous = chapter_file(number - 1) if number > 1 else "index.html"
    next_page = chapter_file(number + 1) if number < len(BOOK["chapters"]) else "back-matter.html"
    transcript_path = TRANSCRIPTS / f"chapter-{number:02d}.html"
    chapter_content = (
        transcript_path.read_text(encoding="utf-8")
        if transcript_path.is_file()
        else f'<div class="page-list">{source_pages(chapter["first_page"], chapter["last_page"])}</div>'
    )
    body = f'''<article class="chapter">
      <header class="chapter-lede"><h1>{esc(title)}</h1>
        <p>หน้าพิมพ์ {chapter['printed_first']}–{chapter['printed_last']} · {chapter['last_page'] - chapter['first_page'] + 1} หน้า</p>
        <div class="chapter-actions"><a href="assets/chapters/chapter-{number:02d}.pdf" download>ดาวน์โหลด PDF บทนี้ ↓</a><a href="{esc(original_pdf(chapter['first_page']))}" target="_blank" rel="noopener">เปิดหนังสือต้นฉบับ ↗</a></div>
      </header>
      {chapter_content}
      {pager(previous, next_page)}
    </article>'''
    return shell(title, body, f"ch-{number}", number)


def build_supplement(key: str, current: str, previous: str, next_page: str) -> str:
    part = BOOK[key]
    title = part["title"]
    pages = []
    for page in range(part["first_page"], part["last_page"] + 1):
        if page in SUPPLEMENT_BLANK_PAGES:
            continue
        manual = TRANSCRIPTS / "manual" / f"page-{page:03d}.html"
        if manual.is_file():
            label = "" if SUPPLEMENT_REVIEW.get(page) else '<p class="transcript-page-header">รอตรวจทานเทียบต้นฉบับอย่างอิสระ</p>'
            body_page = manual.read_text(encoding="utf-8")
        else:
            label = '<p class="transcript-page-header">รอถอดข้อความจากต้นฉบับ</p>'
            body_page = source_pages(page, page, False)
        pages.append(
            f'<section class="transcript-page" id="page-{page:03d}" data-source-page="{page}" '
            f'data-review="{"reviewed" if SUPPLEMENT_REVIEW.get(page) else "draft"}">'
            f'{label}{body_page}<p class="source-page-link">'
            f'<a href="{esc(original_pdf(page))}" target="_blank" rel="noopener">เปิดหน้า PDF {page} ↗</a>'
            '</p></section>'
        )
    body = f'''<article class="chapter"><header class="chapter-lede"><h1>{esc(title)}</h1>
      <p>หน้า PDF {part['first_page']}–{part['last_page']}</p>
      <div class="chapter-actions"><a href="assets/chapters/{key.replace('_', '-')}.pdf" download>ดาวน์โหลด PDF ส่วนนี้ ↓</a></div></header>
      <div class="page-list">{"".join(pages)}</div>
      {pager(previous, next_page)}
    </article>'''
    return shell(title, body, current)


def build_markdown(chapter: dict) -> str:
    number = chapter["number"]
    transcript_path = TRANSCRIPTS / f"chapter-{number:02d}.md"
    if transcript_path.is_file():
        markdown = transcript_path.read_text(encoding="utf-8")
        return (markdown
                .replace("](excerpts/", "](../transcripts/excerpts/")
                .replace('src="assets/', 'src="../assets/')
                .replace('src="transcripts/excerpts/', 'src="../transcripts/excerpts/'))
    by_page: dict[int, list[str]] = {}
    for section in SECTIONS[str(number)]:
        prefix = f"{section['number']} " if section["number"] else ""
        by_page.setdefault(section["pdf_page"], []).append(prefix + section["title"])
    lines = [f"# บทที่ {number} {chapter['title']}", ""]
    for page in range(chapter["first_page"], chapter["last_page"] + 1):
        for heading in by_page.get(page, []):
            lines.extend([f"## {heading}", ""])
        lines.extend([f"![หน้าพิมพ์ {page - 9}](../assets/pages/page-{page:03d}.webp)", ""])
    return "\n".join(lines)


def build_search_index() -> str:
    index = [{"title": "Welcome", "section": "หน้าแรก", "url": "index.html", "text": BOOK["title_th"]}]
    for chapter in BOOK["chapters"]:
        href = chapter_file(chapter["number"])
        index.append({"title": chapter["title"], "section": f"บทที่ {chapter['number']}", "url": href, "text": chapter["title"]})
        for section in SECTIONS[str(chapter["number"])]:
            prefix = f"{section['number']} " if section["number"] else ""
            heading = prefix + section["title"]
            index.append({"title": heading, "section": chapter["title"], "url": f"{href}#page-{section['pdf_page']:03d}", "text": heading})
        transcript_path = TRANSCRIPTS / f"chapter-{chapter['number']:02d}.html"
        if transcript_path.is_file():
            parser = TranscriptPageText()
            parser.feed(transcript_path.read_text(encoding="utf-8"))
            for page, page_text in parser.pages.items():
                index.append({
                    "title": f"หน้าพิมพ์ {page - 9}",
                    "section": f"บทที่ {chapter['number']} {chapter['title']}",
                    "url": f"{href}#page-{page:03d}",
                    "text": page_text,
                })
    for key, href in (("front_matter", "front-matter.html"), ("back_matter", "back-matter.html")):
        part = BOOK[key]
        index.append({"title": part["title"], "section": "ส่วนประกอบหนังสือ", "url": href, "text": part["title"]})
        for page in range(part["first_page"], part["last_page"] + 1):
            if page in SUPPLEMENT_BLANK_PAGES:
                continue
            manual = TRANSCRIPTS / "manual" / f"page-{page:03d}.html"
            if manual.is_file():
                parser = TranscriptPageText()
                parser.feed(f'<section data-source-page="{page}">' + manual.read_text(encoding="utf-8") + '</section>')
                index.append({
                    "title": f"หน้า PDF {page}",
                    "section": part["title"],
                    "url": f"{href}#page-{page:03d}",
                    "text": parser.pages[page],
                })
    return "window.QAFSearchIndex = " + json.dumps(index, ensure_ascii=False).replace("<", "\\u003c") + ";\n"


def main() -> None:
    global PREVIEW_DRAFT, REVIEWED_PAGES, UNREVIEWED_PAGES, SUPPLEMENT_REVIEW
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preview-draft", action="store_true",
        help="Build a local review preview that includes unverified transcript pages",
    )
    args = parser.parse_args()
    PREVIEW_DRAFT = args.preview_draft
    reports = []
    for chapter in BOOK["chapters"]:
        report_path = TRANSCRIPTS / f"chapter-{chapter['number']:02d}.coverage.json"
        reports.append(json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {})
    REVIEWED_PAGES = sum(len(report.get("reviewed", [])) for report in reports)
    UNREVIEWED_PAGES = sum(len(report.get("unreviewed", [])) for report in reports)
    manifest_path = TRANSCRIPTS / "reviewed-pages.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    source_hash = hashlib.sha256((ROOT / BOOK["source_pdf"]).read_bytes()).hexdigest()
    for key in ("front_matter", "back_matter"):
        part = BOOK[key]
        for page in range(part["first_page"], part["last_page"] + 1):
            if page in SUPPLEMENT_BLANK_PAGES:
                continue
            path = TRANSCRIPTS / "manual" / f"page-{page:03d}.html"
            entry = manifest.get("pages", {}).get(str(page), {})
            signed = (
                path.is_file()
                and manifest.get("source_pdf_sha256") == source_hash
                and entry.get("manual_file") == str(path.relative_to(ROOT))
                and entry.get("sha256") == hashlib.sha256(path.read_bytes()).hexdigest()
            )
            SUPPLEMENT_REVIEW[page] = signed
            REVIEWED_PAGES += int(signed)
            UNREVIEWED_PAGES += int(not signed)
    if not args.preview_draft:
        incomplete = []
        for chapter, report in zip(BOOK["chapters"], reports):
            if not report.get("publishable_complete"):
                incomplete.append(chapter["number"])
        if incomplete:
            raise SystemExit(
                f"Unreviewed transcripts in chapters {incomplete}. "
                "Use --preview-draft only for local review; publishing requires page-by-page verification."
            )
        incomplete_supplement = [page for page, signed in SUPPLEMENT_REVIEW.items() if not signed]
        if incomplete_supplement:
            raise SystemExit(f"Unreviewed supplemental pages: {incomplete_supplement}")
    missing = [page for page in range(2, 408) if not (ROOT / "assets" / "pages" / f"page-{page:03d}.webp").is_file()]
    if missing:
        raise FileNotFoundError(f"Source page images missing: {missing[:10]} ({len(missing)} total). Run scripts/prepare_source.py.")
    SITE.mkdir(exist_ok=True)
    for name in ("assets", "styles.css", ".nojekyll"):
        source, target = ROOT / name, SITE / name
        if source.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
        elif source.is_file():
            shutil.copy2(source, target)
    excerpt_source = TRANSCRIPTS / "excerpts"
    excerpt_target = SITE / "transcripts" / "excerpts"
    if excerpt_target.exists():
        shutil.rmtree(excerpt_target)
    referenced_excerpts: set[str] = set()
    for transcript in TRANSCRIPTS.glob("chapter-*.html"):
        referenced_excerpts.update(
            re.findall(r"transcripts/excerpts/([^?\"'<> ]+)", transcript.read_text(encoding="utf-8"))
        )
    if referenced_excerpts:
        excerpt_target.mkdir(parents=True, exist_ok=True)
        for name in referenced_excerpts:
            shutil.copy2(excerpt_source / name, excerpt_target / name)
    (SITE / "index.html").write_text(build_home(), encoding="utf-8")
    (SITE / "search-index.js").write_text(build_search_index(), encoding="utf-8")
    chapter_dir = SITE / "chapters"
    source_chapter_dir = ROOT / "chapters"
    chapter_dir.mkdir(exist_ok=True)
    source_chapter_dir.mkdir(exist_ok=True)
    for chapter in BOOK["chapters"]:
        number = chapter["number"]
        (SITE / chapter_file(number)).write_text(build_chapter(chapter), encoding="utf-8")
        markdown = build_markdown(chapter)
        (chapter_dir / f"chapter-{number:02d}.md").write_text(markdown, encoding="utf-8")
        (source_chapter_dir / f"chapter-{number:02d}.md").write_text(markdown, encoding="utf-8")
    (SITE / "front-matter.html").write_text(build_supplement("front_matter", "front", "index.html", "chapter-01.html"), encoding="utf-8")
    (SITE / "back-matter.html").write_text(build_supplement("back_matter", "back", "chapter-10.html", "index.html"), encoding="utf-8")
    print(f"Built Welcome, {len(BOOK['chapters'])} chapters, and two supplementary sections in {SITE}")


if __name__ == "__main__":
    main()
