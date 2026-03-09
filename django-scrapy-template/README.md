# Django + Scrapy Tracker Template

A production-ready template for building data-tracking websites with integrated web scraping. Combines Django 6.0 (web framework + ORM + admin + REST API) with Scrapy 2.14 (spider engine) in a single project with Celery for scheduled scraping.

Pre-configured for political data tracking (politicians, congressional votes, executive decisions, campaign finance) but designed to be adapted to any domain.

## What Is Included

- **Django 6.0** with split settings (base/development/production)
- **Django REST Framework** with ReadOnly ViewSets, filtering, search, and ordering
- **Scrapy 2.14** integrated via management command (full Django ORM access in pipelines)
- **4 example spiders**: Congress.gov API, VoteSmart, OpenSecrets, Wikipedia bio enrichment
- **Celery + django-celery-beat** for scheduled spider runs
- **drf-spectacular** for auto-generated OpenAPI/Swagger docs
- **PostgreSQL** with full-text search (SearchVectorField + GinIndex)
- **11 Claude slash commands** for common operations
- **5 specialized subagents** pre-loaded with domain knowledge
- **3 skills** covering pipeline integration, data modeling, and API filtering

## Prerequisites

- Python 3.13+
- `uv` package manager (`pip install uv`)
- Docker (for PostgreSQL and Redis)
- Git

## Setup (8 Steps)

### Step 1: Install Dependencies

```bash
uv sync
```

### Step 2: Start Infrastructure

```bash
docker-compose up -d db redis
```

This starts PostgreSQL on port 5432 and Redis on port 6379.

### Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY` — generate with: `uv run python -c "import secrets; print(secrets.token_urlsafe(50))"`
- `CONGRESS_API_KEY` — get free key at https://api.congress.gov/sign-up/

### Step 4: Apply Migrations

```bash
uv run python manage.py migrate
```

### Step 5: Create Admin User

```bash
uv run python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
uv run python manage.py runserver
```

Visit:
- http://127.0.0.1:8000/admin/ — Django admin
- http://127.0.0.1:8000/api/ — REST API root
- http://127.0.0.1:8000/api/schema/swagger-ui/ — Swagger docs

### Step 7: Run Your First Spider

```bash
uv run python manage.py run_spider congress_votes --limit 50
```

This fetches up to 50 congressional members from the Congress.gov API and saves them to the database.

### Step 8: (Optional) Start Celery for Scheduled Scraping

In separate terminals:

```bash
# Worker
uv run celery -A config worker -l info

# Scheduler
uv run celery -A config beat -l info
```

## Slash Commands

| Command | Description |
|---|---|
| `/runserver` | Start the Django development server |
| `/migrate` | Apply pending database migrations |
| `/makemigrations` | Generate migrations from model changes |
| `/shell` | Open shell_plus with all models auto-imported |
| `/spider-run` | Run a named spider via management command |
| `/spider-create` | Scaffold a new spider with boilerplate |
| `/scrape-schedule` | Create or list Celery Beat periodic tasks |
| `/api-docs` | View Swagger UI or generate schema.yml |
| `/test` | Run pytest with coverage reporting |
| `/lint` | Run black, isort, and flake8 checks |
| `/data-export` | Export data to JSON or CSV |

## Subagents

Subagents activate automatically based on context, or you can invoke them explicitly.

| Agent | Triggers |
|---|---|
| `django-scrapy-expert` | Configuring Django-Scrapy connection, pipeline code, django.setup() issues |
| `data-modeler` | "need to track X", "add a model for Z", schema design questions |
| `spider-builder` | Creating new spiders, fixing parsing, handling pagination, JS pages |
| `orm-optimizer` | Slow queries, N+1 problems, debug toolbar showing many queries |
| `test-writer` | Creating new models, adding viewsets, writing pipeline code |

## Skills

Skills activate based on file types and described triggers.

| Skill | Use When |
|---|---|
| `scrapy-django-pipeline` | Adding a new spider that saves to the database |
| `tracker-data-model` | Extending to a new subject type or adapting to a new domain |
| `api-filter-builder` | Adding filters to a new viewset, implementing full-text search |

## Spider Development Quick Start

### 1. Create a Spider

Use the `/spider-create` command or create manually:

```python
# scrapy_spiders/spiders/my_spider.py
import scrapy
from scrapy_spiders.items import PoliticianItem
from scrapy_spiders.loaders import PoliticianLoader

class MySpider(scrapy.Spider):
    name = "my_spider"
    source_name = "My Source"
    source_url = "https://example.com"
    source_type = "government"
    reliability_score = 0.9

    start_urls = ["https://example.com/politicians"]

    def parse(self, response):
        loader = PoliticianLoader(item=PoliticianItem(), response=response)
        loader.add_css("name", "h2.name::text")
        loader.add_css("state", "span.state::text")
        loader.add_value("chamber", "senate")
        yield loader.load_item()
```

### 2. Test the Spider

```bash
uv run python manage.py run_spider my_spider --limit 5
```

### 3. Schedule It

```python
# In Django shell_plus
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

schedule, _ = IntervalSchedule.objects.get_or_create(every=24, period=IntervalSchedule.HOURS)
PeriodicTask.objects.create(
    name="Daily my_spider run",
    task="apps.scraper.tasks.run_spider_task",
    interval=schedule,
    args=json.dumps(["my_spider"]),
)
```

## API Usage Examples

### List Politicians

```bash
curl http://127.0.0.1:8000/api/politicians/
```

### Filter by State and Party

```bash
curl "http://127.0.0.1:8000/api/politicians/?state=CA&party=D"
```

### Search Politicians

```bash
curl "http://127.0.0.1:8000/api/politicians/?search=pelosi"
```

### Get Votes for a Politician

```bash
curl http://127.0.0.1:8000/api/politicians/1/votes/
```

### Filter Votes by Date Range

```bash
curl "http://127.0.0.1:8000/api/votes/?date_from=2024-01-01&date_to=2024-06-30&vote_choice=Nay"
```

### Get Campaign Finance Data

```bash
curl "http://127.0.0.1:8000/api/funding/?cycle_year=2024&min_amount=100000"
```

## Available Spiders

| Spider | Source | Data |
|---|---|---|
| `congress_votes` | Congress.gov API | Members + votes |
| `votesmart` | VoteSmart | Biographical data (stub) |
| `opensecrets` | OpenSecrets | Campaign finance (stub) |
| `wikipedia_bio` | Wikipedia | Bio text enrichment |

The Congress.gov spider works out of the box with a free API key. The VoteSmart and OpenSecrets spiders are stubs showing the integration pattern — implement the `parse()` method with site-specific logic.

## Directory Structure

```
django-scrapy-template/
├── .claude/                  # Claude Code configuration
│   ├── commands/             # 11 slash commands
│   ├── agents/               # 5 specialized subagents
│   ├── skills/               # 3 skills with reference docs
│   └── settings.json
├── config/                   # Django project settings
│   └── settings/base.py, development.py, production.py
├── apps/
│   ├── core/                 # TimeStampedModel abstract base
│   ├── tracker/              # Main data models + REST API
│   └── scraper/              # Celery tasks + management command
├── scrapy_spiders/           # Scrapy project
│   └── spiders/              # Individual spider files
├── templates/base.html
└── static/
```

## Customization Guide

### Adapting to a Non-Political Domain

The four-model pattern (Subject/Decision/AffectedGroup/Source) works for any tracking domain:

- **Corporate accountability**: Company, BoardDecision, StakeholderGroup, RevenueRecord
- **Academic research**: Researcher, Publication, AffectedCommunity, GrantRecord
- **Environmental**: Agency, Regulation, ImpactedSpecies, FundingSource

Steps to adapt:
1. Rename models in `apps/tracker/models.py`
2. Update `CLAUDE.md` with domain-specific context
3. Create new Scrapy Items in `scrapy_spiders/items.py`
4. Build domain-specific spiders

### Adding Authentication

The API is read-only and unauthenticated by default. To add JWT auth:

```bash
uv add djangorestframework-simplejwt
```

Then update `REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]` in `config/settings/base.py`.

### Enabling JavaScript Rendering

Uncomment the Playwright config in `scrapy_spiders/settings.py`, then install browsers:

```bash
uv run playwright install chromium
```

## Troubleshooting

**`No module named 'apps'` when running spider**
Always use `uv run python manage.py run_spider`, not `scrapy crawl`.

**`AppRegistryNotReady` error**
Django is being initialized twice. Check that no pipeline or spider code calls `django.setup()` when running via management command.

**`OperationalError: no such table`**
Run `uv run python manage.py migrate`.

**Celery tasks not running**
Ensure both the worker (`celery worker`) and scheduler (`celery beat`) are running.

**Spider finds no items**
Test with `uv run python manage.py run_spider spider_name --limit 5` and check logs. Verify `CONGRESS_API_KEY` is set for congress_votes.

## Resources

- [Django 6.0 Documentation](https://docs.djangoproject.com/en/6.0/)
- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Congress.gov API](https://api.congress.gov/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [factory-boy](https://factoryboy.readthedocs.io/)
