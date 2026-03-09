---
description: Open Django shell_plus with all models auto-imported
---

Open an enhanced Django shell with all models pre-imported.

```bash
uv run python manage.py shell_plus
```

All tracker models are available: `Politician`, `Vote`, `Decision`, `AffectedGroup`, `DecisionAffectedGroup`, `FundingRecord`, `Source`.

Useful queries to try:

```python
# Count all politicians by party
from django.db.models import Count
Politician.objects.values('party').annotate(count=Count('id'))

# Recent votes for a politician
Politician.objects.get(name__icontains='pelosi').votes.order_by('-vote_date')[:10]

# Decisions affecting economic groups
Decision.objects.filter(affected_groups__category='economic').distinct()

# Top funders for a cycle year
FundingRecord.objects.filter(cycle_year=2024).order_by('-amount_cents')[:20]
```
