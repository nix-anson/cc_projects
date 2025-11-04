---
description: Run Django system checks for common issues
argument-hint: [--tag tags] [--deploy]
allowed-tools: Bash(*), Read(*)
---

Run Django's system check framework to identify common problems in your project.

Arguments:
- $ARGUMENTS: All arguments passed to the check command

Common usage patterns:
- `/check` - Run all system checks
- `/check --deploy` - Run deployment checks (production readiness)
- `/check --tag models` - Check specific category (models, urls, security, etc.)

Execute: `python manage.py check $ARGUMENTS`

The check command validates:
- Model field configuration
- Database configuration
- URL patterns
- Security settings
- Deprecated features
- Common misconfigurations

After running checks:
1. Report any errors or warnings found
2. Explain what each issue means
3. Suggest fixes for identified problems
4. If using --deploy, ensure production readiness

Common check categories:
- `models` - Model and field configuration
- `security` - Security settings and best practices
- `urls` - URL configuration issues
- `templates` - Template configuration
- `caches` - Cache configuration
- `database` - Database settings

Example output interpretation:
- **Errors (E)**: Must be fixed before running the app
- **Warnings (W)**: Should be addressed but not critical
- **Info (I)**: Informational messages

Best practices:
- Run checks before committing code
- Always run --deploy checks before production deployment
- Fix all errors, address warnings when possible
- Add checks to CI/CD pipeline
