---
name: implementation
description: Implement approved Sổ Chi Tiêu changes while preserving requirements, architecture, database boundaries, and verifiable evidence.
---

# Implementation

Read the approved requirement, acceptance criteria, architecture, and database design relevant to the task. If specification is insufficient and the ambiguity changes externally visible behavior, stop and record the issue instead of inventing a rule.

Make the smallest coherent change. Keep user ownership filters on all financial data, secrets in environment variables, Gemini aggregate-only, and database changes migration-backed. Add or update tests, run scoped tests and build/lint-equivalent checks, review the diff, and append commands/results plus changed artifacts to `docs/ai-process-log.md`.

