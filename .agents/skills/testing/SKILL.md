---
name: testing
description: Plan, implement, execute, and report requirement-traceable tests for the Sổ Chi Tiêu backend and frontend.
---

# Testing

Read requirements, stories, and acceptance criteria. Cover positive, negative, boundary, authorization/ownership, error, and integration paths. Never weaken expectations merely to make a test pass.

Run backend tests with `python -m pytest -q`, frontend tests with `npm.cmd test -- --coverage`, and the production frontend build when relevant. Report exact observed results and date in `docs/test-report.md`; do not copy stale counts. Map gaps to requirement IDs in `docs/test-plan.md`.

