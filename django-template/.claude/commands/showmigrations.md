---
description: Display Django migration status for all apps
argument-hint: [app_name] [--list] [--plan]
allowed-tools: Bash(*), Read(*)
---

Show the status of all migrations in the project.

Arguments:
- $ARGUMENTS: All arguments passed to showmigrations command

Common usage patterns:
- `/showmigrations` - Show all migrations with applied status
- `/showmigrations app_name` - Show migrations for specific app
- `/showmigrations --list` - List format (default)
- `/showmigrations --plan` - Show planned migration order

Execute: `python manage.py showmigrations $ARGUMENTS`

The output shows:
- [X] - Migration has been applied
- [ ] - Migration is pending
- Migration names and order

After displaying migrations:
1. Identify any unapplied migrations
2. Check for migration conflicts
3. Look for out-of-order migrations
4. Suggest running `/migrate` if there are pending migrations

Use cases:
- Check which migrations need to be applied
- Verify migration state before deployment
- Debug migration issues
- Confirm migrations were applied successfully

Common scenarios:
- All checked - Database is up to date
- Some unchecked - Run `/migrate` to apply pending migrations
- Gaps in checked migrations - Possible migration conflict

If issues found:
- Unapplied migrations - Run `/migrate`
- Conflicting migrations - Resolve conflicts manually
- Missing migrations - Check if migrations were created

Best practices:
- Check migration status before deploying
- Keep development and production databases in sync
- Document custom migrations
- Review migration plan before applying
