#!/usr/bin/env python3
"""Build the static chapter reader without altering the supplied book PDF."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BOOK = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def header(current: str = "") -> str:
    links = [
        ("index.html", "สารบัญ", "index"),
        ("front-matter.html", "คำนำและสารบัญต้นฉบับ", "front"),
        ("back-matter.html", "ภาคผนวกและดัชนี", "back"),
    ]
    nav_items = []
    for href, label, key in links:
        current_attr = ' aria-current="page"' if key == current else ""
        nav_items.append(f'<a href="{href}"{current_attr}>{label}</a>')
    nav = "\n".join(nav_items)
    return f"""<header class="site-header">
  <a class="brand" href="index.html" aria-label="สารบัญหนังสือ">QAF <span>Lecture note</span></a>
  <nav aria-label="เมนูหลัก">{nav}</nav>
</header>"""


def chapter_list(current: int | None = None) -> str:
    items = []
    for chapter in BOOK["chapters"]:
        number = chapter["number"]
        label = f"บทที่ {number} {chapter['title']}"
        current_attr = ' aria-current="page"' if number == current else ""
        items.append(
            f'<li><a href="chapter-{number:02d}.html"{current_attr}>'
            f'<span class="chapter-number">{number:02d}</span>'
            f'<span>{esc(label)}</span></a></li>'
        )
    return "\n".join(items)


def page_shell(title: str, current: str, body: str, page_class: str = "") -> str:
    return f"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#121212">
  <title>{esc(title)} · {esc(BOOK['title_th'])}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body class="{page_class}">
{header(current)}
{body}
<footer class="site-footer">
  <span>{esc(BOOK['title_th'])}</span>
  <a href="{esc(BOOK['source_pdf'])}">PDF ต้นฉบับ</a>
</footer>
</body>
</html>
"""


def reader_frame(pdf_page: int, label: str) -> str:
    src = f"{BOOK['source_pdf']}#page={pdf_page}&view=FitH"
    return f"""<div class="reader-frame">
  <iframe src="{esc(src)}" title="{esc(label)}" loading="lazy"></iframe>
  <p class="reader-fallback">หากตัวอ่าน PDF ไม่แสดงในหน้านี้ <a href="{esc(src)}" target="_blank" rel="noopener">เปิดหน้าต้นฉบับในแท็บใหม่</a></p>
</div>"""


def build_index() -> str:
    cards = []
    for chapter in BOOK["chapters"]:
        number = chapter["number"]
        cards.append(
            f"""<li class="chapter-card">
  <a href="chapter-{number:02d}.html">
    <span class="chapter-number">{number:02d}</span>
    <span class="chapter-card-copy">
      <span class="eyebrow">บทที่ {number}</span>
      <span class="chapter-title">{esc(chapter['title'])}</span>
      <span class="page-range">หน้า {chapter['printed_first']}–{chapter['printed_last']}</span>
    </span>
    <span class="card-arrow" aria-hidden="true">→</span>
  </a>
</li>"""
        )
    cover = BOOK["cover_image"]
    body = f"""<main class="home-layout">
  <section class="book-intro" aria-labelledby="book-title">
    <div class="cover-wrap"><img src="{esc(cover)}" alt="ปกหนังสือ {esc(BOOK['title_th'])}"></div>
    <div class="intro-copy">
      <p class="eyebrow">Lecture note · ฉบับต้นฉบับ</p>
      <h1 id="book-title">{esc(BOOK['title_th'])}</h1>
      <p class="english-title">{esc(BOOK['title_en'])}</p>
      <p class="author">{esc(BOOK['author'])}</p>
      <p class="edition">{esc(BOOK['edition'])} · {esc(BOOK['year'])} · ISBN {esc(BOOK['isbn'])}</p>
      <div class="action-row">
        <a class="button primary" href="chapter-01.html">เริ่มอ่านบทที่ 1</a>
        <a class="button outlined" href="{esc(BOOK['source_pdf'])}" target="_blank" rel="noopener">เปิด PDF ต้นฉบับ</a>
      </div>
      <p class="source-note">หน้าอ่านแต่ละบทแสดง PDF ต้นฉบับโดยตรง เพื่อคงถ้อยคำ สมการ และภาพประกอบตามหนังสือ</p>
    </div>
  </section>
  <section class="contents-section" aria-labelledby="contents-title">
    <div class="section-heading"><p class="eyebrow">10 chapters</p><h2 id="contents-title">สารบัญ</h2></div>
    <ol class="chapter-grid">{''.join(cards)}</ol>
    <div class="supplement-links">
      <a href="front-matter.html"><span>คำนำและสารบัญต้นฉบับ</span><span>หน้า PDF 2–9</span></a>
      <a href="back-matter.html"><span>ภาคผนวก เอกสารอ้างอิง และดัชนี</span><span>หน้า PDF 392–407</span></a>
    </div>
  </section>
</main>"""
    return page_shell("สารบัญ", "index", body, "home-page")


def build_chapter(chapter: dict) -> str:
    number = chapter["number"]
    previous = BOOK["chapters"][number - 2] if number > 1 else None
    following = BOOK["chapters"][number] if number < len(BOOK["chapters"]) else None
    previous_link = (
        f'<a class="button outlined" href="chapter-{previous["number"]:02d}.html">← บทที่ {previous["number"]} {esc(previous["title"])}</a>'
        if previous else '<a class="button outlined" href="index.html">← สารบัญ</a>'
    )
    next_link = (
        f'<a class="button primary" href="chapter-{following["number"]:02d}.html">บทที่ {following["number"]} {esc(following["title"])} →</a>'
        if following else '<a class="button primary" href="back-matter.html">ภาคผนวกและดัชนี →</a>'
    )
    title = f"บทที่ {number} {chapter['title']}"
    body = f"""<main class="reader-layout">
  <aside class="chapter-sidebar" aria-label="สารบัญบท">
    <a class="back-link" href="index.html">← สารบัญหนังสือ</a>
    <ol>{chapter_list(number)}</ol>
  </aside>
  <article class="reader-content">
    <p class="eyebrow">บทที่ {number} · PDF ต้นฉบับ</p>
    <h1>{esc(chapter['title'])}</h1>
    <p class="page-range">หน้าพิมพ์ {chapter['printed_first']}–{chapter['printed_last']}</p>
    {reader_frame(chapter['first_page'], title)}
    <nav class="chapter-pager" aria-label="เปลี่ยนบท">{previous_link}{next_link}</nav>
  </article>
</main>"""
    return page_shell(title, "", body, "reader-page")


def build_supplement(title: str, first_page: int, current: str) -> str:
    body = f"""<main class="reader-layout supplement-layout">
  <aside class="chapter-sidebar" aria-label="สารบัญบท">
    <a class="back-link" href="index.html">← สารบัญหนังสือ</a>
    <ol>{chapter_list()}</ol>
  </aside>
  <article class="reader-content">
    <p class="eyebrow">ต้นฉบับ PDF</p>
    <h1>{esc(title)}</h1>
    {reader_frame(first_page, title)}
    <nav class="chapter-pager" aria-label="กลับไปยังสารบัญ"><a class="button outlined" href="index.html">← สารบัญ</a></nav>
  </article>
</main>"""
    return page_shell(title, current, body, "reader-page")


def main() -> None:
    if not (ROOT / BOOK["source_pdf"]).is_file():
        raise FileNotFoundError(f"Source PDF not found: {BOOK['source_pdf']}")
    SITE.mkdir(exist_ok=True)
    for name in ["assets", "styles.css", ".nojekyll"]:
        source = ROOT / name
        target = SITE / name
        if source.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
        elif source.is_file():
            shutil.copy2(source, target)

    (SITE / "index.html").write_text(build_index(), encoding="utf-8")
    for chapter in BOOK["chapters"]:
        filename = f"chapter-{chapter['number']:02d}.html"
        (SITE / filename).write_text(build_chapter(chapter), encoding="utf-8")
    (SITE / "front-matter.html").write_text(
        build_supplement(BOOK["front_matter"]["title"], BOOK["front_matter"]["first_page"], "front"),
        encoding="utf-8",
    )
    (SITE / "back-matter.html").write_text(
        build_supplement(BOOK["back_matter"]["title"], BOOK["back_matter"]["first_page"], "back"),
        encoding="utf-8",
    )
    print(f"Built {len(BOOK['chapters'])} chapter pages in {SITE}")


if __name__ == "__main__":
    main()
