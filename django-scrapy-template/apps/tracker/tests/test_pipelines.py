"""Tests for Scrapy pipeline integration with Django ORM."""
import pytest
from scrapy.exceptions import DropItem

from apps.tracker.models import Politician, Source, Vote

from .factories import PoliticianFactory, SourceFactory


def make_pipeline():
    """Helper: instantiate and open a DjangoORMPipeline with a test Source."""
    from scrapy_spiders.pipelines import DjangoORMPipeline

    class FakeSpider:
        name = "test_spider"
        source_name = "Test Source"
        source_url = "https://test.example.com"
        source_type = "government"
        reliability_score = 0.9

    class FakeCrawler:
        spider = FakeSpider()

    pipeline = DjangoORMPipeline(FakeCrawler())
    pipeline.open_spider()
    return pipeline


@pytest.mark.django_db
class TestValidationPipeline:
    def test_drops_politician_missing_name(self):
        from scrapy_spiders.items import PoliticianItem
        from scrapy_spiders.pipelines import ValidationPipeline

        pipeline = ValidationPipeline()
        item = PoliticianItem(chamber="senate", state="CA")  # missing name
        with pytest.raises(DropItem):
            pipeline.process_item(item, spider=None)

    def test_drops_vote_missing_bill_number(self):
        from scrapy_spiders.items import VoteItem
        from scrapy_spiders.pipelines import ValidationPipeline

        pipeline = ValidationPipeline()
        item = VoteItem(
            politician_bioguide_id="A000001",
            vote_date="2024-01-01",
            vote_choice="Yea",
        )  # missing bill_number
        with pytest.raises(DropItem):
            pipeline.process_item(item, spider=None)

    def test_passes_valid_politician(self):
        from scrapy_spiders.items import PoliticianItem
        from scrapy_spiders.pipelines import ValidationPipeline

        pipeline = ValidationPipeline()
        item = PoliticianItem(name="Jane Smith", chamber="senate", state="CA")
        result = pipeline.process_item(item, spider=None)
        assert result is item


@pytest.mark.django_db
class TestDjangoORMPipeline:
    def test_open_spider_creates_source(self):
        pipeline = make_pipeline()
        assert Source.objects.filter(name="Test Source").exists()

    def test_saves_politician(self):
        from scrapy_spiders.items import PoliticianItem

        pipeline = make_pipeline()
        item = PoliticianItem(
            name="Test Senator",
            party="D",
            chamber="senate",
            state="CA",
            bioguide_id="T000001",
        )
        pipeline.process_item(item, spider=None)
        assert Politician.objects.filter(bioguide_id="T000001").exists()
        p = Politician.objects.get(bioguide_id="T000001")
        assert p.name == "Test Senator"
        assert p.state == "CA"

    def test_politician_update_is_idempotent(self):
        """Running the pipeline twice with the same bioguide_id updates, not duplicates."""
        from scrapy_spiders.items import PoliticianItem

        pipeline = make_pipeline()
        item = PoliticianItem(
            name="Test Senator",
            party="D",
            chamber="senate",
            state="CA",
            bioguide_id="T000002",
        )
        pipeline.process_item(item, spider=None)
        pipeline.process_item(item, spider=None)
        assert Politician.objects.filter(bioguide_id="T000002").count() == 1

    def test_saves_vote(self):
        from scrapy_spiders.items import VoteItem

        pipeline = make_pipeline()
        politician = PoliticianFactory(bioguide_id="T000003")
        item = VoteItem(
            politician_bioguide_id="T000003",
            bill_number="H.R.1234",
            bill_title="Test Bill",
            vote_date="2024-03-15",
            vote_choice="Yea",
            congress_session=118,
            roll_call_number=42,
        )
        pipeline.process_item(item, spider=None)
        assert Vote.objects.filter(politician=politician, bill_number="H.R.1234").exists()

    def test_vote_drops_when_politician_missing(self):
        from scrapy_spiders.items import VoteItem

        pipeline = make_pipeline()
        item = VoteItem(
            politician_bioguide_id="NONEXISTENT",
            bill_number="H.R.9999",
            bill_title="Ghost Bill",
            vote_date="2024-01-01",
            vote_choice="Nay",
        )
        with pytest.raises(DropItem):
            pipeline.process_item(item, spider=None)

    def test_vote_update_is_idempotent(self):
        """Same vote scraped twice creates only one record."""
        from scrapy_spiders.items import VoteItem

        pipeline = make_pipeline()
        PoliticianFactory(bioguide_id="T000004")
        item = VoteItem(
            politician_bioguide_id="T000004",
            bill_number="S.100",
            bill_title="Senate Bill",
            vote_date="2024-05-01",
            vote_choice="Nay",
        )
        pipeline.process_item(item, spider=None)
        pipeline.process_item(item, spider=None)
        assert Vote.objects.filter(bill_number="S.100").count() == 1
