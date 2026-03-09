---
description: Design or adapt the four-model tracking pattern (Subject/Decision/AffectedGroup/Source) for a new domain. Use when extending the tracker to a new type of institution or entity, when the user wants to track a new category of decisions, or when adapting this template for non-political use cases.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Tracker Data Model Skill

The tracker uses a four-model pattern that is adaptable to any tracking domain.

## The Four-Model Pattern

```
Subject (Politician) --> Vote
                    --> Decision --M2M--> AffectedGroup
                    --> FundingRecord
Source --> (referenced by Vote, Decision, FundingRecord)
```

## Adapting to a New Domain

Replace "Politician" with your subject entity:

| Political Tracking | Corporate Tracking | Academic Tracking |
|---|---|---|
| Politician | Executive / Company | Researcher / Institution |
| Vote | Board Decision | Publication |
| Decision | Policy / Statement | Research Finding |
| AffectedGroup | Stakeholder Group | Affected Community |
| FundingRecord | Revenue Record | Grant Record |

## Adding a New Subject Type

```python
class NewSubject(TimeStampedModel):
    # Always include:
    name = models.CharField(max_length=255, db_index=True)
    external_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Domain-specific fields
    # ...

    # Full-text search (optional but recommended)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=["search_vector"])]
```

## Through Model Pattern for M2M with Metadata

Always use explicit through models when the M2M relationship has attributes:

```python
class NewSubjectAffectedGroup(TimeStampedModel):
    subject = models.ForeignKey(NewSubject, on_delete=models.CASCADE)
    affected_group = models.ForeignKey(AffectedGroup, on_delete=models.CASCADE)

    # Relationship metadata
    impact_type = models.CharField(max_length=10, choices=ImpactType.choices)
    impact_summary = models.TextField(blank=True)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        unique_together = [["subject", "affected_group"]]
```

## After Adapting

1. Run `uv run python manage.py makemigrations` then `migrate`
2. Update `apps/tracker/admin.py` with new model registration
3. Update `apps/tracker/serializers.py` with new serializer
4. Register viewset in `apps/tracker/viewsets.py` and `urls.py`
5. Add factories in `apps/tracker/tests/factories.py`
6. Create corresponding Scrapy Items in `scrapy_spiders/items.py`
