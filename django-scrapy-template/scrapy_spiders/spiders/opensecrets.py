"""Spider for OpenSecrets campaign finance data."""
import scrapy

from scrapy_spiders.items import FundingItem


class OpenSecretsSpider(scrapy.Spider):
    """Scrape campaign finance data from OpenSecrets.

    Requires OPENSECRETS_API_KEY environment variable.
    """

    name = "opensecrets"
    source_name = "OpenSecrets"
    source_url = "https://opensecrets.org"
    source_type = "nonprofit"
    reliability_score = 0.9

    # Placeholder: implement using OpenSecrets API
    start_urls = []

    def parse(self, response):
        """Implement OpenSecrets-specific parsing here."""
        pass
