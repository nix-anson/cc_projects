"""Celery tasks for running Scrapy spiders."""
from celery import shared_task
from django.core.management import call_command


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def run_spider_task(self, spider_name: str, limit: int = 0):
    """Run a Scrapy spider as a Celery task.

    Args:
        spider_name: Name of the spider to run (e.g., 'congress_votes')
        limit: Maximum items to scrape (0 = unlimited)
    """
    try:
        kwargs = {"spider": spider_name}
        if limit:
            kwargs["limit"] = limit
        call_command("run_spider", **kwargs)
    except Exception as exc:
        raise self.retry(exc=exc)
