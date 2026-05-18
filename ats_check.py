#!/usr/bin/env python3
"""Run ATS-style checks for generated tailored CV sources."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import make_pdfs


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "tailored-cv"
PDF_DIR = ROOT / "pdf"
REPORT_PATH = ROOT / "ats-check.md"
INTERVIEWS_DIR = Path("/Users/yauhenisheima/Sources/Interviews")

STOPWORDS = {
    "a", "about", "across", "active", "after", "all", "also", "an", "and",
    "any", "are", "as", "at", "based", "be", "but", "by", "can",
    "company", "for", "from", "has", "have", "in", "including", "into",
    "is", "it", "of", "on", "or", "role", "senior", "should", "strong",
    "team", "the", "this", "to", "with", "work", "years",
    "applied", "contact", "cv", "earlier", "fit", "imported", "links",
    "outreach", "planned", "salary", "shortlist", "source", "status",
    "updated",
}

NOISE_WORDS = {
    "404", "bana", "csv", "n/a", "pdf", "qa-devops-cv.pdf", "justjoin.it",
    "linkedin", "specified", "url",
}

SKILL_ALIASES = {
    "api": ["api", "rest", "rest api", "graphql"],
    "azure": ["azure", "azure devops", "azure pipelines"],
    "bdd": ["bdd", "gherkin", "cucumber", "specflow"],
    "ci/cd": ["ci/cd", "cicd", "jenkins", "github actions", "gitlab", "teamcity", "azure pipelines"],
    "c#": ["c#", ".net", "dotnet"],
    "docker": ["docker", "container", "containers"],
    "javascript": ["javascript", "js", "node.js", "nodejs"],
    "kubernetes": ["kubernetes", "k8s", "openshift"],
    "playwright": ["playwright"],
    "postman": ["postman", "newman", "bruno"],
    "python": ["python"],
    "selenium": ["selenium", "webdriver", "selenide"],
    "sql": ["sql", "database", "databases", "postgresql"],
    "test automation": ["test automation", "automation qa", "qa automation", "sdet"],
    "typescript": ["typescript", "ts"],
}

ACTION_VERBS = {
    "automated", "built", "created", "designed", "enabled", "extended",
    "improved", "increased", "integrated", "maintained", "optimized",
    "reduced", "stabilized", "supported",
}


@dataclass(frozen=True)
class CompanyContext:
    slug: str
    name: str
    match: str
    source_path: Path
    text: str
    stack_text: str
    fit: str


@dataclass(frozen=True)
class AtsResult:
    slug: str
    context: CompanyContext | None
    overall: int | None
    keyword_score: int | None
    skill_score: int | None
    prominence_score: int | None
    evidence_score: int
    structure_score: int
    pdf_score: int
    matched_keywords: list[str]
    missing_keywords: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    warnings: list[str]
    pdf_path: Path | None


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9+#./-]+", value.lower())


def normalized_text(value: str) -> str:
    return " ".join(words(value))


def clone_context(context: CompanyContext, match: str) -> CompanyContext:
    return CompanyContext(
        slug=context.slug,
        name=context.name,
        match=match,
        source_path=context.source_path,
        text=context.text,
        stack_text=context.stack_text,
        fit=context.fit,
    )


def load_company_contexts(interviews_dir: Path) -> list[CompanyContext]:
    by_slug: dict[str, dict] = {}
    root_json = interviews_dir / "companies.json"
    if root_json.exists():
        data = json.loads(root_json.read_text(encoding="utf-8"))
        for item in data.get("companies", []):
            if item.get("slug"):
                by_slug[item["slug"]] = {**item, "_source_path": root_json}

    companies_dir = interviews_dir / "companies"
    if companies_dir.exists():
        for path in sorted(companies_dir.glob("*/company.json")):
            item = json.loads(path.read_text(encoding="utf-8"))
            if item.get("slug"):
                by_slug[item["slug"]] = {**by_slug.get(item["slug"], {}), **item, "_source_path": path}

    contexts: list[CompanyContext] = []
    for slug, item in sorted(by_slug.items()):
        parts = [str(item.get(key, "")).strip() for key in ("role", "stack", "requirements")]
        notes = str(item.get("notes") or "").strip()
        stack_match = re.search(r"(?:stack|requires?|jd mentions):\s*([^.;]+(?:[.;][^.;]+)?)", notes, re.I)
        if stack_match:
            parts.append(stack_match.group(1).strip())
        text = "; ".join(part for part in parts if part)
        stack_text = str(item.get("stack") or item.get("requirements") or item.get("notes") or "").strip()
        if text:
            contexts.append(CompanyContext(
                slug=slug,
                name=str(item.get("name") or slug),
                match="",
                source_path=Path(item.get("_source_path", "")),
                text=text,
                stack_text=stack_text,
                fit=str(item.get("fit") or ""),
            ))
    return contexts


def match_context(cv_slug: str, contexts: list[CompanyContext]) -> CompanyContext | None:
    context_by_slug = {context.slug: context for context in contexts}
    if cv_slug in context_by_slug:
        return clone_context(context_by_slug[cv_slug], "exact")

    for context in contexts:
        if cv_slug.startswith(context.slug + "-") or context.slug.startswith(cv_slug + "-"):
            return clone_context(context, f"prefix:{context.slug}")

    cv_tokens = set(slugify(cv_slug).split("-"))
    best: tuple[float, CompanyContext] | None = None
    for context in contexts:
        context_tokens = set(slugify(context.slug + " " + context.name).split("-"))
        if not cv_tokens or not context_tokens:
            continue
        score = len(cv_tokens & context_tokens) / math.sqrt(len(cv_tokens) * len(context_tokens))
        if score >= 0.72 and (best is None or score > best[0]):
            best = (score, context)
    if best:
        return clone_context(best[1], f"token:{best[0]:.2f}")
    return None


def recruiter_markdown(path: Path) -> str:
    cleaned = make_pdfs.clean_markdown(path.read_text(encoding="utf-8", errors="replace"))
    return make_pdfs.format_skills_markdown(cleaned)


def extract_keywords(context_text: str) -> list[str]:
    lowered = normalized_text(context_text)
    phrases = set()
    for canonical, aliases in SKILL_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            phrases.add(canonical)

    for raw in re.split(r"[;,()|\n]+", context_text):
        raw_words = [word for word in words(raw.strip(" .:-")) if word not in STOPWORDS and word not in NOISE_WORDS]
        if 1 <= len(raw_words) <= 4:
            phrase = " ".join(raw_words)
            if len(phrase) >= 3:
                phrases.add(phrase)

    counts = Counter(word for word in words(context_text) if word not in STOPWORDS and word not in NOISE_WORDS and len(word) > 2)
    for word, _count in counts.most_common(20):
        phrases.add(word)
    return sorted(phrases)


def extract_required_skills(context_text: str) -> list[str]:
    lowered = normalized_text(context_text)
    return sorted(canonical for canonical, aliases in SKILL_ALIASES.items() if any(alias in lowered for alias in aliases))


def contains_term(text: str, term: str) -> bool:
    aliases = SKILL_ALIASES.get(term, [term])
    return any(alias in text for alias in aliases)


def score_ratio(matched: int, total: int) -> int | None:
    if total == 0:
        return None
    return round(100 * matched / total)


def cap_score(value: float) -> int:
    return max(0, min(100, round(value)))


def score_structure(markdown: str) -> tuple[int, list[str]]:
    headings = {make_pdfs.normalize_heading(match.group(2)) for match in re.finditer(r"^(#{1,6})\s+(.+)$", markdown, re.M)}
    expected = {
        "identity / positioning",
        "short recruiter summary",
        "core strengths",
        "main stack",
        "additional tools / technologies",
        "experience",
    }
    present = expected & headings
    score = round(100 * len(present) / len(expected))
    warnings = [f"missing section: {heading}" for heading in sorted(expected - present)]
    return score, warnings


def score_evidence(markdown: str) -> int:
    text = normalized_text(markdown)
    word_count = max(1, len(text.split()))
    number_hits = len(re.findall(r"\b\d+(?:[.,]\d+)?\s*(?:%|x|gb|mb|tests?|years?)?\b", markdown.lower()))
    action_hits = sum(text.count(verb) for verb in ACTION_VERBS)
    density = (number_hits * 1.7 + action_hits) / word_count * 1000
    return cap_score(density * 14)


def find_pdf(slug: str) -> Path | None:
    path = PDF_DIR / slug / f"{slug}.cv.Yauheni.Sheima.pdf"
    return path if path.exists() else None


def score_pdf(pdf_path: Path | None) -> tuple[int, list[str]]:
    if not pdf_path:
        return 0, ["PDF not generated"]
    size = pdf_path.stat().st_size
    if size < 20_000:
        return 50, [f"PDF suspiciously small: {size} bytes"]
    return 100, []


def evaluate(path: Path, contexts: list[CompanyContext]) -> AtsResult:
    slug = path.stem
    context = match_context(slug, contexts)
    markdown = recruiter_markdown(path)
    text = normalized_text(markdown)
    first_pageish = normalized_text(markdown[:1600])
    warnings: list[str] = []

    structure_score, structure_warnings = score_structure(markdown)
    warnings.extend(structure_warnings)
    evidence_score = score_evidence(markdown)
    pdf_path = find_pdf(slug)
    pdf_score, pdf_warnings = score_pdf(pdf_path)
    warnings.extend(pdf_warnings)

    matched_keywords: list[str] = []
    missing_keywords: list[str] = []
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    keyword_score: int | None = None
    skill_score: int | None = None
    prominence_score: int | None = None
    overall: int | None = None

    if context:
        keywords = extract_keywords(context.text)
        for keyword in keywords:
            if contains_term(text, keyword):
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        keyword_score = score_ratio(len(matched_keywords), len(keywords))

        skills = extract_required_skills(context.text)
        for skill in skills:
            if contains_term(text, skill):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        skill_score = score_ratio(len(matched_skills), len(skills))

        prominent = [keyword for keyword in matched_keywords if contains_term(first_pageish, keyword)]
        prominence_score = score_ratio(len(prominent), len(matched_keywords))

        weighted_parts = [
            (keyword_score, 0.34),
            (skill_score, 0.26),
            (prominence_score, 0.16),
            (evidence_score, 0.10),
            (structure_score, 0.08),
            (pdf_score, 0.06),
        ]
        available = [(score, weight) for score, weight in weighted_parts if score is not None]
        weight_total = sum(weight for _score, weight in available)
        overall = round(sum(score * weight for score, weight in available) / weight_total) if weight_total else None
        if keyword_score is not None and keyword_score < 65:
            warnings.append("low JD keyword coverage")
        if skill_score is not None and skill_score < 75:
            warnings.append("required stack not fully represented")
        if prominence_score is not None and prominence_score < 55:
            warnings.append("matched terms are not prominent enough near the top")
    else:
        warnings.append("no Interviews context found; ATS fit cannot be measured against this vacancy")

    return AtsResult(
        slug=slug,
        context=context,
        overall=overall,
        keyword_score=keyword_score,
        skill_score=skill_score,
        prominence_score=prominence_score,
        evidence_score=evidence_score,
        structure_score=structure_score,
        pdf_score=pdf_score,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        warnings=warnings,
        pdf_path=pdf_path,
    )


def fmt_score(value: int | None) -> str:
    return "n/a" if value is None else f"{value}%"


def item_list(items: list[str], limit: int = 12) -> str:
    if not items:
        return "none"
    shown = items[:limit]
    suffix = "" if len(items) <= limit else f"; +{len(items) - limit} more"
    return ", ".join("'" + item + "'" for item in shown) + suffix


def render_report(results: list[AtsResult], contexts: list[CompanyContext]) -> str:
    scored = [result for result in results if result.overall is not None]
    unscored = [result for result in results if result.overall is None]
    avg = round(statistics.mean(result.overall for result in scored)) if scored else 0
    median = round(statistics.median(result.overall for result in scored)) if scored else 0
    high = sum(1 for result in scored if result.overall and result.overall >= 80)
    medium = sum(1 for result in scored if result.overall and 65 <= result.overall < 80)
    low = sum(1 for result in scored if result.overall and result.overall < 65)

    lines = [
        "# ATS Check",
        "",
        "Generated from ats_check.py.",
        f"CV sources checked: {len(results)}",
        f"Interviews contexts loaded: {len(contexts)}",
        f"Vacancy context matched: {len(scored)}",
        f"No vacancy context found: {len(unscored)}",
        "",
        "## Short Answer",
        "",
        "company-context-coverage.md was not used to tailor the CV files. It was a coverage report only. This ATS check now uses the Interviews context directly as the comparison source.",
        "",
        "## Metrics",
        "",
        "- Overall: weighted score from keyword, stack, prominence, evidence, structure, and PDF checks.",
        "- JD keywords: meaningful terms from role, stack, requirements, and explicit stack/JD hints in notes that appear in the recruiter-facing CV.",
        "- Stack: canonical technology/tool coverage, including aliases such as TS -> TypeScript, REST -> API, K8s -> Kubernetes.",
        "- Prominence: matched JD terms appearing near the top of the CV.",
        "- Evidence: density of action verbs and measurable outcomes.",
        "- Structure: expected CV sections are present after PDF filtering.",
        "- PDF: generated PDF exists and is not suspiciously small.",
        "",
        "## Summary",
        "",
        f"- Average scored fit: **{avg}%**",
        f"- Median scored fit: **{median}%**",
        f"- Strong matches (>=80%): **{high}**",
        f"- Medium matches (65-79%): **{medium}**",
        f"- Weak matches (<65%): **{low}**",
        f"- Unscored because context is missing: **{len(unscored)}**",
        "",
        "## Ranked Results",
        "",
        "| CV | Context | Overall | JD keywords | Stack | Prominence | Evidence | Structure | PDF | Notes |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]

    def sort_key(result: AtsResult) -> tuple[int, int, str]:
        return (0 if result.overall is not None else 1, -(result.overall or -1), result.slug)

    for result in sorted(results, key=sort_key):
        context_name = result.context.name if result.context else "not found"
        notes = "; ".join(result.warnings[:3]).replace("|", "/")
        lines.append(
            f"| {result.slug} | {context_name.replace('|', '/')} | {fmt_score(result.overall)} | {fmt_score(result.keyword_score)} | "
            f"{fmt_score(result.skill_score)} | {fmt_score(result.prominence_score)} | {fmt_score(result.evidence_score)} | "
            f"{fmt_score(result.structure_score)} | {fmt_score(result.pdf_score)} | {notes} |"
        )

    lines.extend(["", "## Detailed Findings", ""])
    for result in sorted(scored, key=lambda item: (item.overall or 0, item.slug)):
        context = result.context
        assert context is not None
        lines.extend([
            f"### {result.slug}",
            "",
            f"- Context: {context.name} ({context.match}), source {context.source_path}",
            f"- Overall: **{fmt_score(result.overall)}**; JD keywords: {fmt_score(result.keyword_score)}; stack: {fmt_score(result.skill_score)}; prominence: {fmt_score(result.prominence_score)}",
            f"- Matched skills: {item_list(result.matched_skills)}",
            f"- Missing skills: {item_list(result.missing_skills)}",
            f"- Missing JD keywords: {item_list(result.missing_keywords)}",
            f"- Warnings: {item_list(result.warnings, limit=8)}",
            "",
        ])

    if unscored:
        lines.extend(["## No Context Found", ""])
        for result in sorted(unscored, key=lambda item: item.slug):
            lines.append(f"- {result.slug}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("only", nargs="*", help="Optional CV slugs to check.")
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    parser.add_argument("--interviews-dir", type=Path, default=INTERVIEWS_DIR)
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir if args.source_dir.is_absolute() else ROOT / args.source_dir
    out = args.out if args.out.is_absolute() else ROOT / args.out
    contexts = load_company_contexts(args.interviews_dir)
    sources = [source_dir / f"{item}.md" if not item.endswith(".md") else Path(item) for item in args.only] if args.only else sorted(source_dir.glob("*.md"))

    missing = [path for path in sources if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing source: {path}")
        return 2

    results = [evaluate(path, contexts) for path in sources]
    out.write_text(render_report(results, contexts), encoding="utf-8")

    scored = [result for result in results if result.overall is not None]
    display_out = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"checked {len(results)} CV sources")
    print(f"matched context: {len(scored)}")
    print(f"missing context: {len(results) - len(scored)}")
    print(f"report: {display_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
