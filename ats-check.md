# ATS Check

Generated from ats_check.py.
CV sources checked: 8
Interviews contexts loaded: 133
Vacancy context matched: 8
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

- Average scored fit: **77%**
- Median scored fit: **77%**
- Strong matches (>=80%): **1**
- Medium matches (65-79%): **7**
- Weak matches (<65%): **0**
- Unscored because context is missing: **0**

## Ranked Results

| CV | Context | Overall | JD keywords | Stack | Prominence | Evidence | Structure | PDF | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| prequel-automation-qa-java | Prequel | 82% | 70% | 100% | 91% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| rogii-fullstack-qa | ROGII | 79% | 57% | 100% | 100% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| inqud-qa-manual-automation | INQUD | 78% | 58% | 100% | 94% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| cat-digital-senior-qa-java | CAT Digital / Caterpillar | 77% | 58% | 100% | 90% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| nova-team-qa-automation-python | Nova Team | 77% | 55% | 100% | 94% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| hirify-fintech-ai-qa | Fintech Platform via Hirify | 76% | 48% | 100% | 100% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| actimind-qa-python-ai | Actimind | 74% | 50% | 100% | 88% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |
| hirify-lead-qa-csharp | Hidden Company via Hirify | 71% | 46% | 100% | 75% | 100% | 17% | 100% | missing section: additional tools / technologies; missing section: experience; missing section: identity / positioning |

## Detailed Findings

### hirify-lead-qa-csharp

- Context: Hidden Company via Hirify (exact), source /Users/yauhenisheima/Sources/Interviews/companies/hirify-lead-qa-csharp/company.json
- Overall: **71%**; JD keywords: 46%; stack: 100%; prominence: 75%
- Matched skills: 'api', 'c#', 'ci/cd', 'playwright', 'python', 'sql'
- Missing skills: none
- Missing JD keywords: '000 usd gross/month', '000-8', '3+ playwright similar', '3+ python automation', '6+ c# automation', '8+ qa', 'actions', 'api/messaging/telecom', 'definition', 'english', 'english c1+. listed 4', 'github'; +7 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### actimind-qa-python-ai

- Context: Actimind (exact), source /Users/yauhenisheima/Sources/Interviews/companies/actimind-qa-python-ai/company.json
- Overall: **74%**; JD keywords: 50%; stack: 100%; prominence: 88%
- Matched skills: 'api', 'ci/cd', 'docker', 'playwright', 'python', 'sql', 'typescript'
- Missing skills: none
- Missing JD keywords: '200 usd', 'analysis/design', 'commercial', 'commercial qa 1 year', 'english a2+', 'grafana', 'locust', 'middle', 'middle qa engineer', 'pytest', 'python/ai', 'requests'; +4 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### hirify-fintech-ai-qa

- Context: Fintech Platform via Hirify (exact), source /Users/yauhenisheima/Sources/Interviews/companies/hirify-fintech-ai-qa/company.json
- Overall: **76%**; JD keywords: 48%; stack: 100%; prominence: 100%
- Matched skills: 'api', 'ci/cd', 'playwright', 'selenium', 'sql'
- Missing skills: none
- Missing JD keywords: '000-3', '2-4', '750 usd/month', 'ai-assisted automation', 'ai-assisted automation framework scratch', 'europe', 'hands-on', 'manual qa', 'mid-level', 'mid-level qa engineer', 'plans/cases', 'remote'; +3 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### cat-digital-senior-qa-java

- Context: CAT Digital / Caterpillar (exact), source /Users/yauhenisheima/Sources/Interviews/companies/cat-digital-senior-qa-java/company.json
- Overall: **77%**; JD keywords: 58%; stack: 100%; prominence: 90%
- Matched skills: 'azure', 'sql', 'typescript'
- Missing skills: none
- Missing JD keywords: '400 usd gross', '6+ automation manual testing', '600-6', 'aws/junit/karate', 'backend qa', 'backend services issues investigation', 'degree', 'degree required', 'junit 5', 'outside', 'outside russia/belarus', 'required'; +3 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### nova-team-qa-automation-python

- Context: Nova Team (exact), source /Users/yauhenisheima/Sources/Interviews/companies/nova-team-qa-automation-python/company.json
- Overall: **77%**; JD keywords: 55%; stack: 100%; prominence: 94%
- Matched skills: 'api', 'ci/cd', 'python', 'sql', 'test automation'
- Missing skills: none
- Missing JD keywords: '000 usd', 'backend/api automation python pytest', 'backend/api qa', 'except', 'framework support', 'georgia', 'kibana', 'logs metrics. listed 3', 'manual debugging/exploratory tasks', 'middle+/senior', 'middle+/senior qa automation', 'relocation'; +2 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### inqud-qa-manual-automation

- Context: INQUD (exact), source /Users/yauhenisheima/Sources/Interviews/companies/inqud-qa-manual-automation/company.json
- Overall: **78%**; JD keywords: 58%; stack: 100%; prominence: 94%
- Matched skills: 'api', 'ci/cd', 'playwright', 'postman', 'selenium', 'sql', 'test automation'
- Missing skills: none
- Missing JD keywords: '800 usd', '800-2', 'approach', 'code-based', 'crypto', 'e2e', 'grafana/datadog', 'manual qa', 'playwright/cypress/selenium', 'postgresql/clickhouse', 'test strategy risk-based testing', 'transactional systems'; +1 more
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### rogii-fullstack-qa

- Context: ROGII (exact), source /Users/yauhenisheima/Sources/Interviews/companies/rogii-fullstack-qa/company.json
- Overall: **79%**; JD keywords: 57%; stack: 100%; prominence: 100%
- Matched skills: 'api', 'ci/cd', 'playwright', 'typescript'
- Missing skills: none
- Missing JD keywords: '000-2', '4+ web qa', '700 usd', 'ai tools', 'design/process', 'experience.', 'frontend backend testing', 'listed', 'microservices', 'test design/process understanding', 'typescript + playwright', 'understanding'
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary', 'low JD keyword coverage'

### prequel-automation-qa-java

- Context: Prequel (exact), source /Users/yauhenisheima/Sources/Interviews/companies/prequel-automation-qa-java/company.json
- Overall: **82%**; JD keywords: 70%; stack: 100%; prominence: 91%
- Matched skills: 'api', 'ci/cd', 'selenium', 'test automation', 'typescript'
- Missing skills: none
- Missing JD keywords: '500 usd gross', 'ai tools', 'api mobile e2e tests', 'automation qa 1 year', 'framework support', 'middle', 'middle automation qa engineer', 'mobile/web automation via appium/selenide', 'via', 'web automation'
- Warnings: 'missing section: additional tools / technologies', 'missing section: experience', 'missing section: identity / positioning', 'missing section: main stack', 'missing section: short recruiter summary'
