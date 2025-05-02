# -----------------------------------------------------------------------------
# docs/scripts/export_html_to_md.py
# Description: Generate Markdown documentation for all source modules using pdoc.
# -----------------------------------------------------------------------------

# docs/scripts/export_html_to_md.py
"""
Convert HTML files in the MkDocs `site/` directory to Markdown files
so the documentation can be viewed or edited as plain .md content.
"""

from pathlib import Path

import html2text

SITE_DIR = Path("site")
EXPORT_DIR = Path("docs/api_md")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

converter = html2text.HTML2Text()
converter.ignore_links = False  # Keep hyperlinks
converter.ignore_images = True
converter.body_width = 0  # Don't wrap text

for html_file in SITE_DIR.glob("**/*.html"):
    rel_path = html_file.relative_to(SITE_DIR).with_suffix(".md")
    out_file = EXPORT_DIR / rel_path
    out_file.parent.mkdir(parents=True, exist_ok=True)

    html = html_file.read_text(encoding="utf-8")
    markdown = converter.handle(html)

    out_file.write_text(markdown, encoding="utf-8")
    print(f"✅ Converted {html_file} → {out_file}")
