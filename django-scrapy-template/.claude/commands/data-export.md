---
description: Export tracker data to JSON or CSV format
argument-hint: "<model> [--format json|csv] [--output filename]"
---

Export tracker data using Django's dumpdata or custom export.

Export via Django dumpdata:

```bash
# Export all tracker data
uv run python manage.py dumpdata tracker --indent 2 > tracker_export.json

# Export specific models
uv run python manage.py dumpdata tracker.politician tracker.vote --indent 2 > politicians_votes.json
```

Or use the shell for custom CSV export:

```bash
uv run python manage.py shell_plus --quiet-load -c "
import csv
from apps.tracker.models import Vote

with open('votes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['politician', 'bill', 'date', 'choice', 'session'])
    for v in Vote.objects.select_related('politician').all():
        writer.writerow([v.politician.name, v.bill_number, v.vote_date, v.vote_choice, v.congress_session])
print('Exported votes.csv')
"
```

Export funding data:

```bash
uv run python manage.py shell_plus --quiet-load -c "
import csv
from apps.tracker.models import FundingRecord

with open('funding.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['politician', 'donor', 'category', 'amount_dollars', 'cycle_year'])
    for r in FundingRecord.objects.select_related('politician').all():
        writer.writerow([r.politician.name, r.donor_name, r.donor_category, r.amount_cents / 100, r.cycle_year])
print('Exported funding.csv')
"
```
