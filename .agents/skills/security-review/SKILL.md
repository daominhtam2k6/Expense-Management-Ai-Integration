---
name: security-review
description: Conduct a read-only security review of Sổ Chi Tiêu across authentication, authorization, input, uploads, secrets, AI privacy, dependencies, and deployment.
---

# Security Review

Do not fix code during the review. Check injection, XSS, CSRF applicability, authentication, object-level authorization, password/token handling, reset flows, uploads, secrets, CORS/hosts, error leakage, dependency risk, and Gemini data boundaries. Verify every data query is scoped to the authenticated owner and that AI receives only documented aggregates.

Classify evidence-backed findings by severity and record limitations (including scans not run) in `docs/security-review.md`. A human must accept or remediate open HIGH/CRITICAL findings before the Security Gate is approved.

