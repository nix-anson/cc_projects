---
description: Create or list Celery Beat periodic tasks for spider scheduling
argument-hint: "<spider_name> <interval_hours>"
---

Manage scheduled spider runs using Celery Beat.

## List all scheduled spider tasks

```bash
uv run python manage.py shell_plus --quiet-load -c "
from django_celery_beat.models import PeriodicTask
tasks = PeriodicTask.objects.filter(task='apps.scraper.tasks.run_spider_task')
if tasks.exists():
    for t in tasks:
        print(f'{t.name}: every {t.interval}  enabled={t.enabled}')
else:
    print('No spider tasks scheduled yet.')
"
```

## Schedule a new spider (example: congress_votes every 24 hours)

Replace `congress_votes` and `24` with your spider name and desired interval.

```bash
uv run python manage.py shell_plus --quiet-load -c "
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

SPIDER = 'congress_votes'   # ← change this
HOURS  = 24                 # ← change this

schedule, _ = IntervalSchedule.objects.get_or_create(
    every=HOURS,
    period=IntervalSchedule.HOURS,
)
task, created = PeriodicTask.objects.update_or_create(
    name=f'Run {SPIDER} spider every {HOURS}h',
    defaults={
        'task': 'apps.scraper.tasks.run_spider_task',
        'interval': schedule,
        'args': json.dumps([SPIDER]),
        'enabled': True,
    }
)
print(f\"{'Created' if created else 'Updated'}: {task.name}\")
"
```

## Disable a scheduled task

```bash
uv run python manage.py shell_plus --quiet-load -c "
from django_celery_beat.models import PeriodicTask
PeriodicTask.objects.filter(
    task='apps.scraper.tasks.run_spider_task'
).update(enabled=False)
print('All spider tasks disabled.')
"
```

## Available spiders to schedule

- `congress_votes` — Members + votes from Congress.gov API
- `wikipedia_bio` — Enrich politician bios from Wikipedia
- `votesmart` — VoteSmart biographical data (stub, requires implementation)
- `opensecrets` — Campaign finance from OpenSecrets (stub, requires implementation)

Make sure Celery Beat is running before schedules take effect:
```bash
uv run celery -A config beat -l info
```
