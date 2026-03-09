"""Django management command to run Scrapy spiders."""
import os

from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Run a Scrapy spider by name"

    def add_arguments(self, parser):
        parser.add_argument("spider", type=str, help="Name of the spider to run")
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Maximum number of items to scrape (0 = unlimited)",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="",
            help="Output file path (e.g., data.json)",
        )

    def handle(self, *args, **options):
        spider_name = options["spider"]
        limit = options["limit"]
        output = options["output"]

        # Ensure DJANGO_SETTINGS_MODULE is set for Scrapy pipeline
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
        # Allow synchronous ORM calls from Scrapy's Twisted/async reactor.
        # Scrapy 2.13+ runs pipelines in an async context; without this flag
        # Django raises SynchronousOnlyOperation on every ORM call.
        os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

        settings = get_project_settings()

        if limit:
            settings.set("CLOSESPIDER_ITEMCOUNT", limit)

        if output:
            settings.set("FEEDS", {output: {"format": "json"}})

        process = CrawlerProcess(settings)

        try:
            process.crawl(spider_name)
            process.start()
            self.stdout.write(
                self.style.SUCCESS(f"Spider '{spider_name}' completed successfully.")
            )
        except KeyError:
            raise CommandError(
                f"Spider '{spider_name}' not found. "
                f"Check scrapy_spiders/spiders/ for available spiders."
            )
