---
name: database-design
description: Design and review the Sổ Chi Tiêu relational schema, migrations, constraints, indexes, ownership boundaries, and traceability.
---

# Database Design

Read approved requirements, architecture, SQLAlchemy models, and Alembic migrations. Check entities, relationships, normalization, PK/FK, nullability, uniqueness, checks, indexes, money precision, deletion behavior, and per-user isolation.

Document gaps separately from the implemented schema. Do not change application code. Update `docs/database-design.md`; schema changes must use an Alembic migration and require the Database Gate in `docs/human-gates.md` before implementation.

