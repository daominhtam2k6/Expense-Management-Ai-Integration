---
name: requirements-analysis
description: Analyze requirements for Sổ Chi Tiêu and produce traceable requirements, stories, acceptance criteria, and unresolved issues before design or implementation.
---

# Requirements Analysis

Read `docs/customer-requirement.md` and existing product documentation. Separate confirmed requirements, assumptions, and unresolved questions. Do not write code or silently derive business rules from the current implementation.

Use stable IDs (`FR-*`, `NFR-*`, `US-*`, `AC-*`). Trace each story and acceptance criterion to requirements. Update `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md`, and `docs/requirements-issues.md`.

Stop before architecture or implementation when an unresolved issue materially changes behavior. Record a human decision in `docs/human-gates.md`; never mark a gate approved on the user's behalf.

