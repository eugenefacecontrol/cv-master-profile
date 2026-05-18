# cv-master-profile

Source repository for Yauheni Sheima's master CV/profile materials.

## Structure

- `master-profile.md` — canonical profile source
- `source-materials/` — raw inputs and extracted notes
- `tailored-cv/` — vacancy-specific CV variants
- `cover-letters/` — reusable and tailored cover letters
- `story-bank/` — interview stories, project examples, achievement narratives
- `notes/` — working notes, gaps, positioning decisions

## PDF generation

Use `make_pdfs.py` to build recruiter-facing PDFs from the Markdown files in `tailored-cv/`.

```bash
./make_pdfs.py --force
```

The script writes one folder per company under `pdf/`, for example:

```text
pdf/us3-consulting/us3-consulting.cv.Yauheni.Sheima.pdf
```

To regenerate only specific companies:

```bash
./make_pdfs.py --force us3-consulting lingaro-ai-devops-engineer
```

To inspect the styled HTML while tuning layout:

```bash
./make_pdfs.py --force --keep-html us3-consulting
```

### Source-vs-PDF Rules

- Markdown sources can keep internal working notes; generated PDFs must be HR-facing only.
- Do not manually edit generated PDFs. Edit the Markdown source or `make_pdfs.py`, then regenerate.
- Keep one Markdown source per company in `tailored-cv/`; generated output goes to one company folder under `pdf/`.
- The visual baseline is `tailored-cv/us3-consulting-quality-assurance-automation-engineer.cv.html`.
- `pandoc` and `weasyprint` are required CLI dependencies.

### Sections Skipped In PDFs

The generator removes internal or application-helper sections from PDF/HTML output while leaving them in Markdown:

- `Tailoring notes`
- `Core Positioning Summary`
- `Best-fit roles`
- `Reusable Achievement Themes`
- `Positioning Boundaries / Honest Framing`
- `Strongest honest framing`
- `Avoid overclaiming`
- `Honest Positioning Note (Internal)`
- ATS keyword packs
- future-growth notes
- raw narrative/source notes
- public-link/evidence/language-background helper sections

If a Markdown file starts with a generated company brief such as `# Tailored CV — Company` and later has the real `# Yauheni Sheima...` heading, the brief is skipped in the PDF.

### Skill Formatting Rules

The generator applies the same skill styling pattern as the hand-polished Us3 Consulting HTML example:

- `Core Strengths` bullet lists become pill-style chips.
- `Main Stack` bullet lists become pill-style chips.
- `Additional Tools / Technologies` bullet lists become pill-style chips.
- `Technical Skills` subsections written as `### Category` plus bullets become compact category paragraphs: `Category: item, item, item`.
- These skill sections must render with normal section headings, not literal Markdown markers such as `## Main Stack`.
- When adding raw HTML helpers in `make_pdfs.py`, keep a blank line after the HTML block so Pandoc resumes Markdown parsing for the next section.
- Keep skill bullets short and recruiter-readable; long explanatory bullets produce oversized chips.
- Prefer grouped skills such as `Azure / Azure DevOps`, `Postman / Newman`, or `Docker / Kubernetes` when that reads cleaner than many tiny chips.

The generic master-profile heading `Yauheni Sheima — Master Profile` is normalized to `Yauheni Sheima` in generated PDFs.

### Company Context Coverage

Company stack/context matching against `/Users/yauhenisheima/Sources/Interviews` is tracked in:

```text
company-context-coverage.md
```

Use that file to see which tailored CV sources have matching interview-tracker context and which still need company stack data added upstream.

### ATS Check

Use ats_check.py to compare recruiter-facing CV content against company context from /Users/yauhenisheima/Sources/Interviews.

    ./ats_check.py

The script writes:

    ats-check.md

ATS scoring rules:

- company-context-coverage.md is a coverage report only; it does not tailor CV text by itself.
- ATS comparison is made from the cleaned recruiter-facing Markdown, using the same filtering path as PDF generation.
- Vacancy context comes from role, stack, and requirements; notes are used only when they contain an explicit stack/JD hint.
- The report uses multiple metrics instead of a single opaque score: JD keyword coverage, stack coverage, term prominence near the top, evidence density, section structure, and generated PDF presence.
- CVs without a matched Interviews context are marked n/a for vacancy-fit scoring; they still get structure/PDF checks.
- Treat low keyword coverage as a signal to manually tailor the summary, core strengths, stack, and experience bullets for that company.
- Do not inflate CVs with unsupported keywords. Add only skills and claims that are honestly backed by the master profile or real experience.

### Verification

Before treating a PDF batch as final, run:

```bash
python3 -m py_compile make_pdfs.py
python3 -m py_compile ats_check.py
./make_pdfs.py --check
./make_pdfs.py --force
./ats_check.py
```

Expected result: the number of generated PDFs under `pdf/*/*.pdf` should match the number of Markdown sources in `tailored-cv/*.md`.
