# Django + Scrapy Tracker - Claude Code Configuration

## Project Overview

This is a combined Django 6.0 + Scrapy 2.14 project for building data-tracking websites with web scraping capabilities. The template is pre-configured for political data tracking (politicians, votes, decisions, campaign finance) but the patterns are adaptable to any domain.

**Key architectural principle**: Scrapy spiders run inside Django management commands. This keeps the Django ORM fully available in pipelines without any complex initialization dance.

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Web framework | Django 6.0 | ORM, admin, URL routing, views |
| REST API | djangorestframework 3.16 | JSON API with ViewSets |
| Scraping | Scrapy 2.14 | Spider engine |
| JS rendering | scrapy-playwright | JavaScript-rendered pages |
| Database | PostgreSQL + psycopg2 | Primary data store |
| Filtering | django-filter | Declarative API filters |
| Task queue | Celery + django-celery-beat | Scheduled spider runs |
| Broker | Redis | Celery broker and result backend |
| API docs | drf-spectacular | OpenAPI/Swagger |
| Dev tools | django-extensions, django-debug-toolbar | Development utilities |
| Testing | pytest-django, factory-boy | Test suite |
| Code quality | black, isort, flake8 | Formatting and linting |
| Config | python-decouple | .env management |
| Package manager | uv | Always use `uv run`, never `pip` or `python` directly |

## Critical Integration Rule

**ALWAYS run Scrapy via `manage.py run_spider`, NEVER via `scrapy crawl`.**

```bash
# CORRECT
uv run python manage.py run_spider congress_votes --limit 100

# WRONG - Django ORM will not be initialized
scrapy crawl congress_votes
```

This is because `apps/scraper/management/commands/run_spider.py` runs inside Django's management command framework, which initializes Django before Scrapy starts. The pipelines in `scrapy_spiders/pipelines.py` then have full ORM access.

The `scrapy_spiders/settings.py` file calls `django.setup()` to support the rare case of standalone Scrapy use, but this path is not the primary workflow.

**Scrapy 2.13+ async compatibility**: Both `scrapy_spiders/settings.py` and `run_spider.py` set `DJANGO_ALLOW_ASYNC_UNSAFE=true` before starting the crawler. This is required because Scrapy 2.13+ runs pipelines inside an async reactor context, which causes Django's ORM to raise `SynchronousOnlyOperation` without this flag. This is the correct fix — do not remove it.

## Project Structure

```
django-scrapy-template/
├── manage.py                         # Django entry point
├── pyproject.toml                    # uv dependencies
├── docker-compose.yml                # PostgreSQL + Redis + Celery
├── config/                           # Django project config
│   ├── __init__.py                   # Celery app import
│   ├── celery.py                     # Celery configuration
│   ├── settings/
│   │   ├── base.py                   # Shared settings
│   │   ├── development.py            # Dev overrides (debug toolbar)
│   │   └── production.py            # Production security settings
│   ├── urls.py                       # Root URL config
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/
│   │   └── models.py                 # TimeStampedModel abstract base
│   ├── tracker/                      # Main data app
│   │   ├── models.py                 # Politician, Vote, Decision, etc.
│   │   ├── admin.py                  # Django admin registrations
│   │   ├── serializers.py            # DRF serializers
│   │   ├── viewsets.py               # DRF ViewSets
│   │   ├── filters.py                # django-filter FilterSets
│   │   ├── urls.py                   # DRF router registration
│   │   └── tests/
│   │       ├── factories.py          # factory-boy factories
│   │       ├── test_models.py
│   │       └── test_api.py
│   └── scraper/
│       ├── tasks.py                  # Celery tasks (run_spider_task)
│       └── management/commands/
│           └── run_spider.py         # Management command
├── scrapy_spiders/                   # Scrapy project
│   ├── settings.py                   # Scrapy settings
│   ├── items.py                      # PoliticianItem, VoteItem, etc.
│   ├── loaders.py                    # ItemLoaders with processors
│   ├── pipelines.py                  # ValidationPipeline, DjangoORMPipeline
│   ├── middlewares.py                # RetryOnRateLimitMiddleware
│   └── spiders/
│       ├── congress_votes.py         # Congress.gov API
│       ├── votesmart.py              # VoteSmart (stub)
│       ├── opensecrets.py            # OpenSecrets (stub)
│       └── wikipedia_bio.py          # Wikipedia bio enrichment
├── templates/base.html
└── static/
```

## Core Data Models

All models inherit from `TimeStampedModel` (provides `created_at`, `updated_at`).

### Politician
Central entity. Key fields: `name`, `party`, `chamber`, `state`, `district`.
External IDs: `bioguide_id`, `votesmart_id`, `opensecrets_id` (nullable, used for scraped data cross-reference).
Full-text search: `search_vector` (SearchVectorField + GinIndex).

### Vote
Links `Politician` to a congressional vote. Unique constraint on `(politician, bill_number, vote_date)` for idempotent re-scraping.

### Decision
Represents executive orders, bill sponsorships, public statements. Links to `AffectedGroup` via `DecisionAffectedGroup` through model.

### DecisionAffectedGroup (Through Model)
Explicit through model for Decision <-> AffectedGroup M2M. Contains `impact_type`, `impact_summary`, `estimated_people_affected`.

### AffectedGroup
Groups of people affected by political decisions. Categories: economic, demographic, geographic, industry, environmental.

### FundingRecord
Campaign finance data. Amounts stored as integer cents (`amount_cents`) to avoid floating-point precision issues.

### Source
Data source reference with `reliability_score`. Each spider creates/references one Source record.

## Common Commands

All commands use `uv run`. Never use plain `python` or `pip`.

```bash
# Server
uv run python manage.py runserver

# Database
uv run python manage.py migrate
uv run python manage.py makemigrations
uv run python manage.py createsuperuser

# Enhanced shell (all models auto-imported)
uv run python manage.py shell_plus

# Scrapy
uv run python manage.py run_spider congress_votes
uv run python manage.py run_spider congress_votes --limit 100

# Testing
uv run pytest
uv run pytest --cov=apps --cov-report=term-missing

# Code quality
uv run black . && uv run isort .
uv run flake8 .

# Celery (separate terminals)
uv run celery -A config worker -l info
uv run celery -A config beat -l info

# Docker services
docker-compose up -d db redis
```

## Code Style and Conventions

### Python Style
- Follow PEP 8; Black formatter enforces 88 character line length
- Use type hints for function parameters where clarity helps
- Use descriptive names; avoid abbreviations except standard ones (pk, id, db)

### Model Conventions
- Inherit from `TimeStampedModel` — never add `created_at`/`updated_at` manually
- Use `models.TextChoices` for all enumeration fields; store human-readable short codes
- Add `__str__` to every model
- Define `class Meta` with `ordering` and `indexes`
- External IDs: `unique=True, null=True, blank=True` pattern
- Money: store as integer cents, display as dollars

### ORM Conventions
- Use `select_related()` for ForeignKey/OneToOne traversal
- Use `prefetch_related()` for ManyToMany and reverse FK
- Use `annotate()` for counts instead of Python-side aggregation
- Use `update_or_create()` keyed on external IDs in pipelines (idempotent)
- Use `exists()` instead of `count() > 0`

### Scrapy Conventions
- Each spider defines: `name`, `source_name`, `source_url`, `source_type`, `reliability_score`
- Use `ItemLoader` with processors instead of manual string cleaning in `parse()`
- `DjangoORMPipeline.open_spider()` creates the Source record once
- `ValidationPipeline` validates required fields; drops invalid items
- `update_or_create` in all pipeline save methods
- **Scrapy 2.14 pipeline API**: `open_spider` and `close_spider` no longer receive `spider` as a parameter. Use `from_crawler(cls, crawler)` and `self.crawler.spider` to access the spider instance. Similarly, `process_item(self, item)` is called without spider — the spider arg is deprecated.
- In tests, pass `FakeCrawler()` to `DjangoORMPipeline(crawler)` and call `pipeline.open_spider()` without arguments.

### API Conventions
- `ReadOnlyModelViewSet` for all data (read-only API)
- `filterset_class` from `django-filter` for structured filtering
- `search_fields` for full-text ILIKE via DRF SearchFilter
- `ordering_fields` for client-controlled sorting
- Pagination: 25 items per page (configurable in settings)
- Two serializers per entity: `*ListSerializer` (compact) and `*DetailSerializer` (full with nested)

## Security Considerations

1. `SECRET_KEY` must come from environment — never hardcode
2. `DEBUG = False` in production; use `config/settings/production.py`
3. HTTPS security headers are set in production settings
4. `ROBOTSTXT_OBEY = True` in Scrapy — always respect robots.txt
5. User-Agent identifies the bot with contact info
6. API is read-only (`ReadOnlyModelViewSet`) by default
7. Rate limiting via `AUTOTHROTTLE_ENABLED = True` and `DOWNLOAD_DELAY`
8. Never store raw API keys in code — use `.env` and `python-decouple`

## Performance Patterns

### ORM
- `PoliticianViewSet` annotates `vote_count` and `decision_count` in a single query
- `VoteViewSet` uses `select_related("politician", "source")`
- `DecisionViewSet` uses `prefetch_related("affected_groups")`
- GinIndex on `search_vector` for fast full-text search

### Scrapy
- `AUTOTHROTTLE_ENABLED = True` adapts to server response times
- `DOWNLOAD_DELAY = 1.5` seconds base delay
- `CONCURRENT_REQUESTS = 4` — conservative for government sites
- HTTP caching available via `HTTPCACHE_ENABLED` (commented out by default)

## Testing Strategy

- Framework: `pytest-django` with `factory-boy`
- `DJANGO_SETTINGS_MODULE = "config.settings.development"` in `pyproject.toml`
- Mark all DB tests with `@pytest.mark.django_db`
- Use factories for all data setup (never hardcode PKs)
- Test API endpoints: list, filter, retrieve, and custom actions
- Test pipeline: save, update (idempotency), and DropItem on validation failure

## Spider Development Guide

1. Create `scrapy_spiders/spiders/my_spider.py`
2. Set `name`, `source_name`, `source_url`, `source_type`, `reliability_score`
3. Implement `async def start()` (with API key from env) and `parse()`
4. Use `ItemLoader` with the appropriate Item class
5. Add new Item fields to `ValidationPipeline.REQUIRED_FIELDS`
6. Add pipeline handler in `DjangoORMPipeline.process_item()`
7. Test with `uv run python manage.py run_spider my_spider --limit 5`
8. Schedule via Celery Beat using `apps.scraper.tasks.run_spider_task`

## Setup Instructions

See `README.md` for step-by-step setup. Quick reference:

```bash
# 1. Install dependencies
uv sync

# 2. Start infrastructure
docker-compose up -d db redis

# 3. Configure environment
cp .env.example .env
# Edit .env with your SECRET_KEY and API keys

# 4. Initialize database
uv run python manage.py migrate
uv run python manage.py createsuperuser

# 5. Run server
uv run python manage.py runserver

# 6. Run a spider
uv run python manage.py run_spider congress_votes --limit 50
```

## API Documentation Links

- Django: https://docs.djangoproject.com/en/6.0/
- DRF: https://www.django-rest-framework.org/
- Scrapy: https://docs.scrapy.org/en/latest/
- django-filter: https://django-filter.readthedocs.io/
- drf-spectacular: https://drf-spectacular.readthedocs.io/
- Celery: https://docs.celeryq.dev/
- factory-boy: https://factoryboy.readthedocs.io/
- Congress.gov API: https://api.congress.gov/
