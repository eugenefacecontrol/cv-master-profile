# ATS Check

Generated from ats_check.py.
CV sources checked: 1
Interviews contexts loaded: 87
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

- Average scored fit: **81%**
- Median scored fit: **81%**
- Strong matches (>=80%): **1**
- Medium matches (65-79%): **0**
- Weak matches (<65%): **0**
- Unscored because context is missing: **0**

## Ranked Results

| CV | Context | Overall | JD keywords | Stack | Prominence | Evidence | Structure | PDF | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| omada | Omada | 81% | 67% | 90% | 66% | 100% | 100% | 100% |  |

## Detailed Findings

### omada

- Context: Omada (exact), source /Users/yauhenisheima/Sources/Interviews/companies/omada/company.json
- Overall: **81%**; JD keywords: 67%; stack: 90%; prominence: 66%
- Matched skills: 'api', 'azure', 'c#', 'ci/cd', 'playwright', 'selenium', 'sql', 'test automation', 'typescript'
- Missing skills: 'bdd'
- Missing JD keywords: '5+ test automation', 'ai-assisted development tools', 'azure devops pipelines/releases', 'azure webapps/functions/apis', 'bdd', 'bdd/specflow', 'ci/cd integration', 'code reviews', 'data validation ui testing', 'defect feedback quality improvements', 'development', 'nice-to-have powershell'; +4 more
- Warnings: none
