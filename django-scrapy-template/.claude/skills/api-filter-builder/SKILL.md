---
description: Build django-filter FilterSets and full-text search for tracker API endpoints. Use when adding filtering to a new viewset, extending existing filters with new fields, or implementing full-text search in apps/tracker/filters.py or apps/tracker/viewsets.py.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# API Filter Builder Skill

## Standard FilterSet Pattern

```python
# apps/tracker/filters.py
import django_filters
from .models import NewModel

class NewModelFilter(django_filters.FilterSet):
    # Exact match
    status = django_filters.CharFilter()

    # Case-insensitive contains
    name = django_filters.CharFilter(lookup_expr="icontains")

    # FK filter by ID
    politician = django_filters.NumberFilter()

    # Date range
    date_from = django_filters.DateFilter(field_name="date_issued", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date_issued", lookup_expr="lte")

    # Numeric range
    min_amount = django_filters.NumberFilter(field_name="amount_cents", lookup_expr="gte")

    # Multiple values (comma-separated): ?state=CA,TX,NY
    states = django_filters.BaseInFilter(field_name="state", lookup_expr="in")

    class Meta:
        model = NewModel
        fields = ["status", "politician"]
```

## Connecting to ViewSet

```python
class NewModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewModel.objects.select_related("politician")
    serializer_class = NewModelSerializer
    filterset_class = NewModelFilter          # django-filter
    search_fields = ["name", "description"]  # DRF SearchFilter (ILIKE)
    ordering_fields = ["date_issued", "name"]
```

Register the viewset in `apps/tracker/urls.py`:

```python
router.register("new-models", NewModelViewSet)
```

## Full-Text Search Setup

For PostgreSQL full-text search on Politician:

```python
# In a management command or shell:
from django.contrib.postgres.search import SearchVector
Politician.objects.update(
    search_vector=SearchVector("name", "bio", "state")
)

# In viewset, override get_queryset for ranked search:
from django.contrib.postgres.search import SearchQuery, SearchRank

def get_queryset(self):
    qs = super().get_queryset()
    query = self.request.query_params.get("search")
    if query:
        search_query = SearchQuery(query)
        qs = qs.filter(search_vector=search_query).annotate(
            rank=SearchRank("search_vector", search_query)
        ).order_by("-rank")
    return qs
```

## Filter Testing

```python
@pytest.mark.django_db
class TestNewModelFilter:
    def test_date_range_filter(self, client):
        NewModelFactory(date_issued="2024-01-01")
        NewModelFactory(date_issued="2024-06-01")
        response = client.get(
            reverse("newmodel-list"),
            {"date_from": "2024-03-01"}
        )
        assert response.data["count"] == 1

    def test_search_filter(self, client):
        PoliticianFactory(name="Test Person")
        response = client.get(reverse("politician-list"), {"search": "test"})
        assert response.data["count"] >= 1
```
