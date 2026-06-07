# ATS Check

Generated from ats_check.py.
CV sources checked: 1
Interviews contexts loaded: 134
Vacancy context matched: 1
No vacancy context found: 0

## Short Answer

company-context-coverage.md was not used to tailor the CV files. It was a coverage report only. This ATS check now uses the Interviews context directly as the comparison source.

## Metrics

- Overall: weighted score from keyword, stack, prominence, evidence, structure, and PDF checks.
- JD keywords: meaningful terms from role, stack, requirements, and explicit stack/JD hints in notes that appear in the recruiter-facing CV.
- Stack: canonical technology/tool coverage, including aliases such as TS -> TypeScript, REST -> API, K8s -> Kubernetes.
- Prominence: matched JD terms appearing near the top of the CV.
- Evidence: density of action verbs and measurable outcomes.
- Structure: expected CV sections are present after PDF filtering.
- PDF: generated PDF exists and is not suspiciously small.

## Summary

- Average scored fit: **88%**
- Median scored fit: **88%**
- Strong matches (>=80%): **1**
- Medium matches (65-79%): **0**
- Weak matches (<65%): **0**
- Unscored because context is missing: **0**

## Ranked Results

| CV | Context | Overall | JD keywords | Stack | Prominence | Evidence | Structure | PDF | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| xebia | Xebia | 88% | 75% | 100% | 86% | 100% | 83% | 100% | missing section: identity / positioning |

## Detailed Findings

### xebia

- Context: Xebia (exact), source /Users/yauhenisheima/Sources/Interviews/companies/xebia/company.json
- Overall: **88%**; JD keywords: 75%; stack: 100%; prominence: 86%
- Matched skills: 'api', 'ci/cd', 'javascript', 'playwright', 'test automation', 'typescript'
- Missing skills: none
- Missing JD keywords: 'ab testing feature flags', 'bulgaria/poland/romania.', 'ci/cd tools', 'collaborate development/product teams', 'create test strategies', 'multi-viewport testing', 'parallel execution reporting', 'production-safe smoke tests', 'quality metrics documentation', 'support shift-left qa', 'test data staging/pre-production', 'third-party/supplier integrations'
- Warnings: 'missing section: identity / positioning'
