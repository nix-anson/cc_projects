---
description: Apply database migrations
argument-hint: '[target]'
---

Apply database migrations using Alembic.

If $1 is provided, upgrade to that specific revision. Otherwise, upgrade to latest (head).

```bash
alembic upgrade ${1:-head}
```

Use `head` for latest, `+1` for next migration, or specific revision hash.
