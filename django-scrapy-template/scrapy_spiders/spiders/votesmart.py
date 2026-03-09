"""Spider for VoteSmart public data."""
import scrapy

from scrapy_spiders.items import PoliticianItem


class VoteSmartSpider(scrapy.Spider):
    """Scrape biographical data from VoteSmart.

    Note: VoteSmart requires API key for full access.
    This spider demonstrates the integration pattern.
    """

    name = "votesmart"
    source_name = "VoteSmart"
    source_url = "https://votesmart.org"
    source_type = "nonprofit"
    reliability_score = 0.85

    # Placeholder: implement using VoteSmart API
    start_urls = []

    def parse(self, response):
        """Implement VoteSmart-specific parsing here."""
        pass
