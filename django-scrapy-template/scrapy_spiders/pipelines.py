"""Scrapy pipelines -- save items to Django ORM.

Django is already initialized when run via management command.
Do NOT call django.setup() here; it is done in scrapy_spiders/settings.py.
"""
import logging

from scrapy.exceptions import DropItem

from apps.tracker.models import FundingRecord, Politician, Source, Vote
from scrapy_spiders.items import FundingItem, PoliticianItem, VoteItem

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """Validate required fields before saving."""

    REQUIRED_FIELDS = {
        PoliticianItem: ["name", "chamber", "state"],
        VoteItem: ["politician_bioguide_id", "bill_number", "vote_date", "vote_choice"],
        FundingItem: ["politician_opensecrets_id", "donor_name", "amount_cents"],
    }

    def process_item(self, item, spider=None):
        item_type = type(item)
        required = self.REQUIRED_FIELDS.get(item_type, [])
        for field in required:
            if not item.get(field):
                raise DropItem(
                    f"Missing required field '{field}' in {item_type.__name__}"
                )
        return item


class DjangoORMPipeline:
    """Save scraped items to the Django database via ORM.

    Uses update_or_create for idempotent re-runs.
    """

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self):
        # Scrapy 2.14+: access spider via self.crawler.spider (spider arg removed)
        spider = self.crawler.spider
        self.source, _ = Source.objects.get_or_create(
            name=getattr(spider, "source_name", spider.name),
            defaults={
                "url": getattr(spider, "source_url", ""),
                "source_type": getattr(spider, "source_type", "government"),
                "reliability_score": getattr(spider, "reliability_score", 0.9),
            },
        )

    def process_item(self, item, spider=None):
        if isinstance(item, PoliticianItem):
            return self._save_politician(item)
        elif isinstance(item, VoteItem):
            return self._save_vote(item)
        elif isinstance(item, FundingItem):
            return self._save_funding(item)
        return item

    def _save_politician(self, item):
        politician, created = Politician.objects.update_or_create(
            bioguide_id=item.get("bioguide_id"),
            defaults={
                "name": item["name"],
                "party": item.get("party", "O"),
                "chamber": item.get("chamber", "other"),
                "state": item.get("state", ""),
                "district": item.get("district", ""),
                "bio": item.get("bio", ""),
                "photo_url": item.get("photo_url", ""),
                "official_url": item.get("official_url", ""),
            },
        )
        action = "Created" if created else "Updated"
        logger.info(f"{action} politician: {politician.name}")
        return item

    def _save_vote(self, item):
        try:
            politician = Politician.objects.get(
                bioguide_id=item["politician_bioguide_id"]
            )
        except Politician.DoesNotExist:
            raise DropItem(
                f"Politician with bioguide_id={item['politician_bioguide_id']} not found"
            )

        vote, created = Vote.objects.update_or_create(
            politician=politician,
            bill_number=item["bill_number"],
            vote_date=item["vote_date"],
            defaults={
                "bill_title": item.get("bill_title", ""),
                "vote_choice": item["vote_choice"],
                "congress_session": item.get("congress_session"),
                "roll_call_number": item.get("roll_call_number"),
                "source": self.source,
            },
        )
        action = "Created" if created else "Updated"
        logger.info(f"{action} vote: {politician.name} -- {vote.bill_number}")
        return item

    def _save_funding(self, item):
        try:
            politician = Politician.objects.get(
                opensecrets_id=item["politician_opensecrets_id"]
            )
        except Politician.DoesNotExist:
            raise DropItem(
                f"Politician with opensecrets_id={item['politician_opensecrets_id']} not found"
            )

        record, created = FundingRecord.objects.update_or_create(
            politician=politician,
            donor_name=item["donor_name"],
            cycle_year=item["cycle_year"],
            defaults={
                "donor_category": item.get("donor_category", ""),
                "amount_cents": item["amount_cents"],
                "source": self.source,
            },
        )
        action = "Created" if created else "Updated"
        logger.info(f"{action} funding: {politician.name} <- {record.donor_name}")
        return item
