# Pipeline Integration Reference

## Common Errors and Fixes

### `django.core.exceptions.AppRegistryNotReady`
**Cause**: Django not initialized before model import.
**Fix**: Import models inside method, not at module level, OR ensure running via `manage.py run_spider`.

### `No module named 'apps'`
**Cause**: PYTHONPATH does not include project root.
**Fix**: Always use `manage.py run_spider`, never `scrapy crawl` directly.

### `OperationalError: no such table`
**Cause**: Migrations not applied.
**Fix**: `uv run python manage.py migrate`

### `DropItem` fired unexpectedly
**Cause**: Required field missing from spider output.
**Fix**: Check `ValidationPipeline.REQUIRED_FIELDS` matches your Item fields.

## Pipeline Order

Pipelines run in order of their priority number (lower number = runs earlier):

```python
ITEM_PIPELINES = {
    "scrapy_spiders.pipelines.ValidationPipeline": 100,   # First: validate
    "scrapy_spiders.pipelines.DjangoORMPipeline": 300,    # Second: save to DB
}
```

## Testing Pipelines Without Running Full Spider

```python
import pytest
from scrapy_spiders.pipelines import DjangoORMPipeline
from scrapy_spiders.items import VoteItem
from apps.tracker.models import Source

@pytest.mark.django_db
def test_pipeline_saves_vote():
    pipeline = DjangoORMPipeline()
    pipeline.source, _ = Source.objects.get_or_create(
        name="Test Spider",
        defaults={"url": "http://test.com", "source_type": "other"}
    )
    item = VoteItem(
        politician_bioguide_id="A000001",
        bill_number="H.R.1",
        vote_date="2024-01-15",
        vote_choice="Yea",
    )
    # Must have a politician in DB first
    result = pipeline.process_item(item, spider=None)
    assert result is not None
```

## Source Metadata Convention

Each spider should define these class attributes, used by `DjangoORMPipeline.open_spider`:

```python
class MySpider(scrapy.Spider):
    name = "my_spider"
    source_name = "My Source Name"    # Displayed in admin
    source_url = "https://source.com" # Source homepage
    source_type = "government"        # government|news|nonprofit|academic|other
    reliability_score = 0.9           # 0.0 to 1.0
```
