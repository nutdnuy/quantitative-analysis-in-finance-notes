# Visual implementation notes

- The layout follows the existing Quantitative Finance Notes reader: left navigation, Welcome page, chapter pages, search, light/dark mode, and print controls.
- The cover, original-page comparisons, chapter PDFs, and figures come from the supplied PDF. No generated artwork or decorative replacement was added.
- Thai UI uses bundled Noto Sans Thai; Latin UI uses bundled Roboto.
- Welcome is a website introduction and table of contents. All source-book content is organized by original PDF page in the ten chapters and supplementary sections.
- The 390 non-cover content pages are selectable HTML. Equations use MathML, tables use HTML, and original figures remain source images. Each page links back to the corresponding PDF page.
- Long equations and tables scroll inside their content blocks, leaving prose in the normal reading column.
- All 390 pages with content were independently checked against the source. The local publishing build rejects any page whose signed file hash no longer matches.
