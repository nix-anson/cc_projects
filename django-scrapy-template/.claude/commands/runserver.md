---
description: Start the Django development server
---

Start the Django development server with auto-reload.

```bash
uv run python manage.py runserver
```

The server will be available at:
- App: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/schema/swagger-ui/

Make sure PostgreSQL and Redis are running first (via `docker-compose up -d db redis`).
