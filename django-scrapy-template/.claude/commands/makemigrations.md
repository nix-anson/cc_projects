---
description: Generate new Django migrations from model changes
argument-hint: "[app_name]"
---

Generate new migration files from model changes.

```bash
uv run python manage.py makemigrations $ARGUMENTS
```

After generating, review the migration file then apply with `/migrate`.

Tips:
- Run `uv run python manage.py makemigrations --check` to check without creating files
- Run `uv run python manage.py showmigrations` to see migration status
- Run `uv run python manage.py sqlmigrate tracker 0001` to preview SQL
