---
description: Create Alembic database migration
argument-hint: '<message>'
---

Create a new database migration using Alembic.

$1 is required and should be a descriptive message for the migration.

```bash
alembic revision --autogenerate -m "$1"
```

Remember to review the generated migration file in `alembic/versions/` before applying it.
