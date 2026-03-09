"""Scrapy settings — Django is already initialized when run via management command."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
# Allow synchronous ORM calls from Scrapy's Twisted/async reactor (2.13+).
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# Configure Django before importing Django models in pipelines
import django

django.setup()

BOT_NAME = "tracker_spiders"

SPIDER_MODULES = ["scrapy_spiders.spiders"]
NEWSPIDER_MODULE = "scrapy_spiders.spiders"

# Scrapy-Django integration
SCRAPY_SETTINGS_MODULE = "scrapy_spiders.settings"

# Crawl responsibly
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = "TrackerBot/1.0 (research project; contact: your@email.com)"

# Auto-throttle for politeness
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Item pipelines
ITEM_PIPELINES = {
    "scrapy_spiders.pipelines.ValidationPipeline": 100,
    "scrapy_spiders.pipelines.DjangoORMPipeline": 300,
}

# Playwright for JS-rendered pages (optional)
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Caching (useful for development)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 86400
# HTTPCACHE_DIR = ".scrapy/cache"

LOG_LEVEL = "INFO"
