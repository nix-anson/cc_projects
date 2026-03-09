# Data Model Reference

## Django Field Choices for Tracker Models

```python
# Party choices
class Party(models.TextChoices):
    DEMOCRAT = "D", "Democrat"
    REPUBLICAN = "R", "Republican"
    INDEPENDENT = "I", "Independent"
    OTHER = "O", "Other"

# Chamber choices
class Chamber(models.TextChoices):
    SENATE = "senate", "Senate"
    HOUSE = "house", "House of Representatives"
    EXECUTIVE = "executive", "Executive"

# Impact types
class ImpactType(models.TextChoices):
    POSITIVE = "positive", "Positive"
    NEGATIVE = "negative", "Negative"
    MIXED = "mixed", "Mixed"
    NEUTRAL = "neutral", "Neutral"
    UNKNOWN = "unknown", "Unknown"
```

## External ID Fields

Always nullable for progressive data enrichment. Set `unique=True` so
`update_or_create` keyed on this field never creates duplicates:

```python
bioguide_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
votesmart_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
opensecrets_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
```

## PostgreSQL-Specific Features Used

- `SearchVectorField` + `GinIndex` for full-text search on Politician
- `django.contrib.postgres` in INSTALLED_APPS is required
- These features only work with PostgreSQL (not SQLite)
- Populate `search_vector` via a management command or signal after bulk inserts

## Updating search_vector in Shell

```python
from django.contrib.postgres.search import SearchVector
from apps.tracker.models import Politician

Politician.objects.update(
    search_vector=SearchVector("name", "bio", "state")
)
```

## Money Amounts

Store money as integer cents (`amount_cents = models.BigIntegerField()`),
never as floats. Display in templates or serializers as `amount_cents / 100`.
This avoids floating-point precision errors in aggregations.
