---
description: Run a named Scrapy spider via Django management command
argument-hint: "<spider_name> [--limit N] [--output file.json]"
---

Run a Scrapy spider using the Django management command (keeps Django ORM available).

Available spiders:
- `congress_votes` — Fetch members and votes from Congress.gov API
- `votesmart` — Biographical data from VoteSmart
- `opensecrets` — Campaign finance from OpenSecrets
- `wikipedia_bio` — Enrich politician bios from Wikipedia

```bash
uv run python manage.py run_spider $ARGUMENTS
```

Examples:

```bash
# Run with item limit
uv run python manage.py run_spider congress_votes --limit 100

# Run and export to file
uv run python manage.py run_spider congress_votes --output data.json

# Enrich bios from Wikipedia
uv run python manage.py run_spider wikipedia_bio
```

IMPORTANT: Always use `manage.py run_spider`, not `scrapy crawl` directly. The management command ensures Django is properly initialized so the ORM pipeline can save data.
