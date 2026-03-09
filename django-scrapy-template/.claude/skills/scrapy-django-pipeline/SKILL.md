---
description: Connect a new Scrapy spider to the Django ORM. Use when adding a new spider that needs to save data to the database, implementing update_or_create patterns, or fixing django.setup() initialization errors in scrapy_spiders/pipelines.py or any spider file.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Scrapy-Django Pipeline Integration Skill

When connecting a new spider to Django ORM, follow this exact pattern:

## Step 1: Define Items in `scrapy_spiders/items.py`

```python
class NewDataItem(scrapy.Item):
    external_id = scrapy.Field()              # For update_or_create key
    politician_bioguide_id = scrapy.Field()   # FK lookup
    field_one = scrapy.Field()
    field_two = scrapy.Field()
    source_url = scrapy.Field()
```

## Step 2: Add Pipeline Handler in `scrapy_spiders/pipelines.py`

```python
def process_item(self, item, spider):
    if isinstance(item, NewDataItem):
        return self._save_new_data(item)
    # ... existing handlers

def _save_new_data(self, item):
    try:
        politician = Politician.objects.get(bioguide_id=item["politician_bioguide_id"])
    except Politician.DoesNotExist:
        raise DropItem(f"Politician not found: {item['politician_bioguide_id']}")

    obj, created = NewModel.objects.update_or_create(
        external_id=item["external_id"],
        defaults={
            "politician": politician,
            "field_one": item.get("field_one", ""),
            "source": self.source,
        },
    )
    logger.info(f"{'Created' if created else 'Updated'}: {obj}")
    return item
```

## Step 3: Add Validation

In `ValidationPipeline.REQUIRED_FIELDS`:

```python
NewDataItem: ["external_id", "politician_bioguide_id", "field_one"],
```

## Critical Rules

- **NEVER** call `django.setup()` in pipeline code — Django is already initialized when running via `manage.py run_spider`
- **ALWAYS** use `update_or_create` keyed on stable external IDs for idempotent re-runs
- **ALWAYS** create `Source` in `open_spider`, not in `process_item` (once per run, not per item)
- **ALWAYS** raise `DropItem` for validation failures, never silently skip
- **ALWAYS** run via `manage.py run_spider`, not `scrapy crawl` directly

See `reference.md` for troubleshooting guide.
