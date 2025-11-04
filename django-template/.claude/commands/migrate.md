---
description: Run Django database migrations
argument-hint: [--fake] [--fake-initial] [app_name] [migration_name]
allowed-tools: Bash(*), Read(*)
---

Run Django database migrations to apply pending changes to the database schema.

Arguments:
- $ARGUMENTS: All arguments passed to the migrate command

Common usage patterns:
- `/migrate` - Apply all pending migrations
- `/migrate app_name` - Migrate specific app
- `/migrate app_name migration_name` - Migrate to specific migration
- `/migrate --fake` - Mark migrations as applied without running them
- `/migrate --fake-initial` - Fake initial migrations

Execute: `python manage.py migrate $ARGUMENTS`

If there are any errors:
1. Check if there are unapplied migrations with `python manage.py showmigrations`
2. Review migration files for issues
3. Check database connectivity
4. Look for circular dependencies in migrations

After successful migration, show the migration status.
