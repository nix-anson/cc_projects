---
description: Create new Django migrations from model changes
argument-hint: [app_name] [--empty] [--name migration_name]
allowed-tools: Bash(*), Read(*), Write(*)
---

Create new Django migrations based on model changes detected in the project.

Arguments:
- $ARGUMENTS: All arguments passed to makemigrations command

Common usage patterns:
- `/makemigrations` - Create migrations for all apps with changes
- `/makemigrations app_name` - Create migrations for specific app
- `/makemigrations --empty app_name` - Create empty migration for custom operations
- `/makemigrations --name migration_name app_name` - Create migration with specific name

Execute: `python manage.py makemigrations $ARGUMENTS`

After creating migrations:
1. Review the generated migration files to ensure correctness
2. Check for any potential issues (circular dependencies, data loss warnings)
3. Show the created migration file path and content summary
4. Remind about running `/migrate` to apply the migrations

Best practices:
- Always review generated migrations before applying
- Use descriptive names for custom migrations
- Consider data migrations for complex schema changes
- Test migrations on development database first
