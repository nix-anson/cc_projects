---
description: Apply pending Django database migrations
---

Apply all pending migrations to the database.

```bash
uv run python manage.py migrate
```

If you are setting up for the first time, also create a superuser:

```bash
uv run python manage.py createsuperuser
```

To check migration status before applying:

```bash
uv run python manage.py showmigrations
```
