#!/usr/bin/env python3
"""Build recruiter-facing PDF CVs from tailored Markdown sources.

The Markdown files can keep internal positioning notes. This script removes
those sections only from generated PDF/HTML output.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "tailored-cv"
OUTPUT_DIR = ROOT / "pdf"
STYLE_HTML = SOURCE_DIR / "us3-consulting-quality-assurance-automation-engineer.cv.html"


REMOVE_HEADINGS = {
    "tailoring notes",
    "core positioning summary",
    "positioning boundaries / honest framing",
    "strongest honest framing",
    "avoid overclaiming",
    "best-fit roles",
    "reusable achievement themes",
    "future growth directions / interests",
    "raw narrative source notes",
    "ats ai keyword bank",
    "ats keyword pack for this role (use in application forms / profile)",
    "honest positioning note (internal)",
    "public links",
    "evidence from practice / coding style notes",
    "language background and practical depth",
}


CHIP_SECTIONS = {
    "core strengths",
    "main stack",
    "additional tools / technologies",
}


COMPACT_SKILLS_SECTION = "technical skills"


FALLBACK_CSS = """
:root {
  --text: #1f2937;
  --muted: #4b5563;
  --accent: #0f766e;
  --line: #d1d5db;
}
@page { size: A4; margin: 14mm 14mm 16mm 14mm; }
html, body {
  font-family: "Inter", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  line-height: 1.34;
  font-size: 10.4pt;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
body { margin: 0; }
h1 {
  margin: 0;
  font-size: 23pt;
  line-height: 1.08;
  color: #0b1320;
}
h2 {
  margin: 5.4mm 0 2.2mm;
  font-size: 11pt;
  letter-spacing: .03em;
  text-transform: uppercase;
  color: #111827;
}
h3 {
  margin: 4.4mm 0 1.4mm;
  font-size: 10.5pt;
  color: #111827;
}
p { margin: 0 0 2.4mm; }
ul { margin: 1mm 0 2.8mm 4.2mm; padding: 0; }
li { margin: 0 0 1.2mm; }
a { color: #0b5cab; text-decoration: none; }
""".strip()


def normalize_heading(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*_]+", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def parse_heading(line: str) -> tuple[int, str] | None:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
    if not match:
        return None
    return len(match.group(1)), normalize_heading(match.group(2))


def strip_leading_internal_brief(lines: list[str]) -> list[str]:
    """Drop generated company metadata before the real Yauheni CV heading."""
    if not lines:
        return lines

    first = parse_heading(lines[0])
    if not first or not first[1].startswith("tailored cv"):
        return lines

    for index, line in enumerate(lines[1:], start=1):
        heading = parse_heading(line)
        if heading and heading[0] == 1 and "yauheni sheima" in heading[1]:
            return lines[index:]
    return lines


def clean_markdown(text: str) -> str:
    lines = strip_leading_internal_brief(text.splitlines())
    output: list[str] = []
    skipped_stack: list[int] = []

    for line in lines:
        heading = parse_heading(line)
        if heading:
            level, title = heading

            while skipped_stack and level <= skipped_stack[-1]:
                skipped_stack.pop()

            if title in REMOVE_HEADINGS:
                skipped_stack.append(level)
                continue

            if level == 1 and title == "yauheni sheima — master profile":
                line = "# Yauheni Sheima"

        if not skipped_stack:
            output.append(line)

    cleaned = "\n".join(output).strip()
    return cleaned + "\n"


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return text.strip()


def is_bullet(line: str) -> bool:
    return bool(re.match(r"^\s*[-*]\s+", line))


def bullet_text(line: str) -> str:
    return strip_inline_markdown(re.sub(r"^\s*[-*]\s+", "", line).strip())


def chip_block(items: list[str]) -> list[str]:
    if not items:
        return []
    lines = ['<div class="chips">']
    for item in items:
        lines.append(f'  <span class="chip">{html.escape(item)}</span>')
    lines.append("</div>")
    lines.append("")
    return lines


def collect_bullet_block(lines: list[str], start: int) -> tuple[list[str], int]:
    items: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if parse_heading(line):
            break
        if is_bullet(line):
            items.append(bullet_text(line))
        elif line.strip() and items:
            break
        elif line.strip():
            break
        index += 1
    return items, index


def format_skills_markdown(markdown: str) -> str:
    """Apply the reusable PDF skill layout used by the hand-polished sample."""
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0
    in_compact_skills = False

    while index < len(lines):
        line = lines[index]
        heading = parse_heading(line)

        if heading:
            level, title = heading
            if level <= 2:
                in_compact_skills = title == COMPACT_SKILLS_SECTION

            if title in CHIP_SECTIONS:
                output.append(line)
                index += 1
                while index < len(lines) and not lines[index].strip():
                    output.append(lines[index])
                    index += 1
                items, next_index = collect_bullet_block(lines, index)
                if items:
                    output.extend(chip_block(items))
                    index = next_index
                    continue

            if in_compact_skills and level == 3:
                label = strip_inline_markdown(line.lstrip("#").strip())
                index += 1
                while index < len(lines) and not lines[index].strip():
                    index += 1
                items, next_index = collect_bullet_block(lines, index)
                if items:
                    output.append(f"<p><strong>{html.escape(label)}:</strong> {html.escape(', '.join(items))}</p>")
                    output.append("")
                    index = next_index
                    continue

        output.append(line)
        index += 1

    return "\n".join(output).strip() + "\n"


def load_css() -> str:
    if not STYLE_HTML.exists():
        return FALLBACK_CSS
    content = STYLE_HTML.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<style>(.*?)</style>", content, re.DOTALL | re.IGNORECASE)
    if not match:
        return FALLBACK_CSS
    return match.group(1).strip()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True)


def render_one(md_path: Path, out_root: Path, keep_html: bool, force: bool) -> Path:
    slug = md_path.stem
    company_dir = out_root / slug
    company_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = company_dir / f"{slug}.cv.Yauheni.Sheima.pdf"
    html_path = company_dir / f"{slug}.cv.html"
    if pdf_path.exists() and not force:
        print(f"skip existing {pdf_path.relative_to(ROOT)}")
        return pdf_path

    cleaned_md = clean_markdown(md_path.read_text(encoding="utf-8", errors="replace"))
    formatted_md = format_skills_markdown(cleaned_md)
    css = load_css()

    with tempfile.TemporaryDirectory(prefix="cv-pdf-") as tmp:
        tmp_dir = Path(tmp)
        tmp_md = tmp_dir / f"{slug}.md"
        tmp_body = tmp_dir / f"{slug}.body.html"
        tmp_html = tmp_dir / f"{slug}.html"
        tmp_md.write_text(formatted_md, encoding="utf-8")

        pandoc = run(["pandoc", str(tmp_md), "--from", "gfm", "--to", "html", "--output", str(tmp_body)])
        if pandoc.returncode != 0:
            raise RuntimeError(f"pandoc failed for {md_path}:\n{pandoc.stderr}")

        body = tmp_body.read_text(encoding="utf-8", errors="replace")
        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""
        tmp_html.write_text(html, encoding="utf-8")

        weasy = run(["weasyprint", str(tmp_html), str(pdf_path)])
        if weasy.returncode != 0:
            raise RuntimeError(f"weasyprint failed for {md_path}:\n{weasy.stderr}")

        if keep_html:
            shutil.copyfile(tmp_html, html_path)
        elif html_path.exists():
            html_path.unlink()

    print(f"generated {pdf_path.relative_to(ROOT)}")
    return pdf_path


def markdown_sources(source_dir: Path, only: list[str]) -> list[Path]:
    if only:
        requested = []
        for item in only:
            path = Path(item)
            if not path.suffix:
                path = source_dir / f"{item}.md"
            elif not path.is_absolute():
                path = ROOT / path
            requested.append(path)
        return sorted(requested)
    return sorted(source_dir.glob("*.md"))


def require_cli(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required command not found: {name}")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("only", nargs="*", help="Optional source slugs or Markdown paths to render.")
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR, help="Markdown source directory.")
    parser.add_argument("--out", type=Path, default=OUTPUT_DIR, help="Output root for company folders.")
    parser.add_argument("--keep-html", action="store_true", help="Save the intermediate styled HTML next to each PDF.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing PDFs.")
    parser.add_argument("--check", action="store_true", help="Print render plan and section filtering checks without generating PDFs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir if args.source_dir.is_absolute() else ROOT / args.source_dir
    out_root = args.out if args.out.is_absolute() else ROOT / args.out
    sources = markdown_sources(source_dir, args.only)

    missing = [path for path in sources if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing source: {path}", file=sys.stderr)
        return 2

    if args.check:
        print(f"sources: {len(sources)}")
        print(f"output: {display_path(out_root)}")
        print("filtered headings:")
        for heading in sorted(REMOVE_HEADINGS):
            print(f"- {heading}")
        return 0

    try:
        require_cli("pandoc")
        require_cli("weasyprint")

        rendered = 0
        for source in sources:
            render_one(source, out_root, args.keep_html, args.force)
            rendered += 1

        print(f"\nRendered {rendered}/{len(sources)} PDF files into {out_root}")
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
