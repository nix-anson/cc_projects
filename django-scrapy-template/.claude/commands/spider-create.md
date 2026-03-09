---
description: Scaffold a new Scrapy spider with DjangoORM pipeline boilerplate
argument-hint: "<spider_name> <source_url>"
---

Create a new spider file with the standard DjangoORM integration boilerplate.

Spider name: $1
Source URL: $2

Create the file `scrapy_spiders/spiders/$1.py` with this template:

```python
"""Spider for scraping data from $2."""
import scrapy

from scrapy_spiders.items import PoliticianItem  # or VoteItem, FundingItem
from scrapy_spiders.loaders import PoliticianLoader


class $1Spider(scrapy.Spider):
    """Scrape data from $2.

    Usage:
        python manage.py run_spider $1 --limit 50
    """

    name = "$1"
    source_name = "Source Name"
    source_url = "$2"
    source_type = "government"  # government, news, nonprofit, academic, other
    reliability_score = 0.9

    start_urls = ["$2"]

    def parse(self, response):
        # TODO: Implement parsing logic
        # loader = PoliticianLoader(item=PoliticianItem(), response=response)
        # loader.add_css("name", "h1::text")
        # yield loader.load_item()
        pass
```

After creating the spider:
1. Implement the `parse` method with site-specific selectors
2. Add the item type to `ValidationPipeline.REQUIRED_FIELDS` in `scrapy_spiders/pipelines.py` if needed
3. Test with: `uv run python manage.py run_spider $1 --limit 5`
