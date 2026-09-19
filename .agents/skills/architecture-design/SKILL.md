---
name: architecture-design
description: Design or revise the Sổ Chi Tiêu architecture from human-approved requirements with explicit rationale and traceability.
---

# Architecture Design

Read the requirements artifacts and require an approved Requirements Gate in `docs/human-gates.md`. If absent, produce a draft only and identify the blocker.

Describe components, responsibilities, dependencies, data flow, external services, trust boundaries, and requirement coverage. Preserve the chosen FastAPI, React, SQLAlchemy, PostgreSQL/SQLite, Gemini, Resend, and Tauri constraints unless a human approves a change. Do not implement code. Update `docs/architecture.md` and `docs/architecture-decisions.md`.

