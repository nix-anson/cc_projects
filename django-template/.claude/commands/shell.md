---
description: Open Django interactive shell
argument-hint: [--plain] [-c command]
allowed-tools: Bash(*)
---

Open Django's interactive Python shell with project context loaded.

Arguments:
- $ARGUMENTS: All arguments passed to the shell command

Common usage patterns:
- `/shell` - Open enhanced shell (IPython if installed, otherwise standard)
- `/shell --plain` - Use standard Python shell
- `/shell -c "from myapp.models import MyModel; print(MyModel.objects.count())"` - Execute command

Execute: `python manage.py shell $ARGUMENTS`

The Django shell provides:
- All Django models and settings pre-imported
- Database access through ORM
- Testing queries and code snippets
- Debugging and exploration

If django-extensions is installed, you can use:
- `python manage.py shell_plus` - Auto-imports all models
- `python manage.py shell_plus --print-sql` - Show SQL queries

Common shell operations:
```python
# Import models
from myapp.models import MyModel

# Query database
MyModel.objects.all()
MyModel.objects.filter(name='example')
MyModel.objects.create(name='new item')

# Check settings
from django.conf import settings
print(settings.DEBUG)

# Test functions
from myapp.utils import my_function
my_function()
```

Tips:
- Use IPython for better shell experience (install with pip)
- Use shell_plus for auto-importing models
- Use --print-sql to debug query performance
- Exit with Ctrl+D or exit()
