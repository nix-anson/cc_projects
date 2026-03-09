# API Filter Builder Reference

## django-filter Lookup Expressions

| Filter Type | lookup_expr | Example URL |
|---|---|---|
| Exact | (default) | `?party=D` |
| Case-insensitive exact | `iexact` | `?state=ca` |
| Contains | `icontains` | `?name=smith` |
| Greater than or equal | `gte` | `?date_from=2024-01-01` |
| Less than or equal | `lte` | `?date_to=2024-12-31` |
| In list | `in` (with BaseInFilter) | `?state=CA,TX,NY` |
| Year extraction | `year` | `?year=2024` |

## DRF Built-in Filters vs django-filter

- **DRF SearchFilter** (`search_fields`): Full-table ILIKE search across specified fields. Simple, no configuration needed. Adds `?search=` param.
- **django-filter** (`filterset_class`): Precise field-level filtering with type coercion. Use for structured queries.
- **DRF OrderingFilter** (`ordering_fields`): Client-controlled sort order via `?ordering=field` or `?ordering=-field`.

Use all three together for maximum API flexibility.

## Common Filter Patterns in This Project

```python
# Filter votes by congress session (exact integer)
congress_session = django_filters.NumberFilter()

# Filter by party with case insensitivity
party = django_filters.CharFilter(lookup_expr="iexact")

# Filter decisions by date range
date_from = django_filters.DateFilter(field_name="date_issued", lookup_expr="gte")
date_to = django_filters.DateFilter(field_name="date_issued", lookup_expr="lte")

# Filter funding by amount range
min_amount = django_filters.NumberFilter(field_name="amount_cents", lookup_expr="gte")
max_amount = django_filters.NumberFilter(field_name="amount_cents", lookup_expr="lte")
```

## URL Filter Examples for This API

```
# Politicians in California, Democrat party
GET /api/politicians/?state=CA&party=D

# Nay votes in the 118th Congress
GET /api/votes/?vote_choice=Nay&congress_session=118

# Votes for a specific politician
GET /api/votes/?politician=42

# Decisions between two dates
GET /api/decisions/?date_from=2024-01-01&date_to=2024-06-30

# Funding over $1000 in 2024
GET /api/funding/?cycle_year=2024&min_amount=100000

# Full-text search across politician names and bios
GET /api/politicians/?search=immigration
```
