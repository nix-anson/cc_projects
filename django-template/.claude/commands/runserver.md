---
description: Start Django development server
argument-hint: [port] [--noreload] [--nothreading]
allowed-tools: Bash(*)
---

Start the Django development server for local development.

Arguments:
- $ARGUMENTS: All arguments passed to runserver command

Common usage patterns:
- `/runserver` - Start server on default port 8000
- `/runserver 8080` - Start server on specific port
- `/runserver 0.0.0.0:8000` - Make server accessible from network
- `/runserver --noreload` - Disable auto-reload on file changes
- `/runserver --nothreading` - Disable threading

Execute: `python manage.py runserver $ARGUMENTS`

The server will run in the foreground. You can access it at:
- http://127.0.0.1:8000/ (or specified port)
- If using 0.0.0.0, accessible from other devices on your network

Notes:
- Development server automatically reloads on code changes
- Not suitable for production use - use gunicorn or uwsgi instead
- Press Ctrl+C to stop the server
- Check ALLOWED_HOSTS in settings if you get Bad Request errors

Common issues:
- "Port already in use" - Try a different port or kill the process
- "Bad Request (400)" - Add your host to ALLOWED_HOSTS in settings
