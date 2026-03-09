"""Scrapy Item definitions for tracker data."""
import scrapy


class PoliticianItem(scrapy.Item):
    """Scraped politician data."""

    name = scrapy.Field()
    party = scrapy.Field()
    chamber = scrapy.Field()
    state = scrapy.Field()
    district = scrapy.Field()
    bioguide_id = scrapy.Field()
    votesmart_id = scrapy.Field()
    opensecrets_id = scrapy.Field()
    bio = scrapy.Field()
    photo_url = scrapy.Field()
    official_url = scrapy.Field()
    term_start = scrapy.Field()
    term_end = scrapy.Field()


class VoteItem(scrapy.Item):
    """Scraped vote record."""

    politician_bioguide_id = scrapy.Field()  # FK lookup key
    bill_number = scrapy.Field()
    bill_title = scrapy.Field()
    vote_date = scrapy.Field()
    vote_choice = scrapy.Field()
    congress_session = scrapy.Field()
    roll_call_number = scrapy.Field()
    source_url = scrapy.Field()


class DecisionItem(scrapy.Item):
    """Scraped decision or policy action."""

    politician_bioguide_id = scrapy.Field()
    title = scrapy.Field()
    decision_type = scrapy.Field()
    date_issued = scrapy.Field()
    summary = scrapy.Field()
    full_text = scrapy.Field()
    source_url = scrapy.Field()


class FundingItem(scrapy.Item):
    """Scraped campaign finance record."""

    politician_opensecrets_id = scrapy.Field()
    donor_name = scrapy.Field()
    donor_category = scrapy.Field()
    amount_cents = scrapy.Field()
    cycle_year = scrapy.Field()
    source_url = scrapy.Field()
