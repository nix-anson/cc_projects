"""Spider for scraping congressional member and vote data from Congress.gov API."""
import logging
import os

import scrapy

from scrapy_spiders.items import PoliticianItem, VoteItem
from scrapy_spiders.loaders import PoliticianLoader, VoteLoader

logger = logging.getLogger(__name__)

CONGRESS_API_BASE = "https://api.congress.gov/v3"

PARTY_MAP = {
    "democratic": "D",
    "democrat": "D",
    "republican": "R",
    "independent": "I",
    "libertarian": "I",
    "green": "I",
}


class CongressVotesSpider(scrapy.Spider):
    """Scrape members and their votes from the Congress.gov API.

    First fetches all current members (yields PoliticianItem), then for each
    member fetches their voting history (yields VoteItem).

    Requires CONGRESS_API_KEY env var. Falls back to "DEMO_KEY" (heavily rate-limited).

    Usage:
        python manage.py run_spider congress_votes
        python manage.py run_spider congress_votes --limit 50
    """

    name = "congress_votes"
    source_name = "Congress.gov"
    source_url = "https://congress.gov"
    source_type = "government"
    reliability_score = 0.99

    def __init__(self, congress=118, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.congress = int(congress)
        self.api_key = os.environ.get("CONGRESS_API_KEY", "DEMO_KEY")

    async def start(self):
        url = (
            f"{CONGRESS_API_BASE}/member"
            f"?format=json&limit=250&currentMember=true&api_key={self.api_key}"
        )
        yield scrapy.Request(url, callback=self.parse_members)

    def parse_members(self, response):
        data = response.json()
        members = data.get("members", [])

        for member in members:
            bioguide_id = member.get("bioguideId")

            loader = PoliticianLoader(item=PoliticianItem())
            loader.add_value("name", self._parse_name(member))
            loader.add_value("party", self._parse_party(member.get("partyName", "")))
            loader.add_value("bioguide_id", bioguide_id)
            loader.add_value("state", member.get("state", ""))
            loader.add_value("chamber", self._parse_chamber(member.get("terms", [])))
            loader.add_value("official_url", member.get("officialWebsiteUrl", ""))
            yield loader.load_item()

            # Queue vote history for each member
            if bioguide_id:
                votes_url = (
                    f"{CONGRESS_API_BASE}/member/{bioguide_id}/votes"
                    f"?format=json&limit=50&api_key={self.api_key}"
                )
                yield scrapy.Request(
                    votes_url,
                    callback=self.parse_votes,
                    cb_kwargs={"bioguide_id": bioguide_id},
                    # Lower priority so all members are fetched before vote detail requests
                    priority=-1,
                )

        # Follow pagination for member list
        next_url = data.get("pagination", {}).get("next")
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_members)

    def parse_votes(self, response, bioguide_id):
        """Parse vote records for a single member."""
        data = response.json()
        votes_wrapper = data.get("votes", {})

        # API returns votes nested under "votes" > "vote" (list)
        vote_list = votes_wrapper.get("vote", [])
        if isinstance(vote_list, dict):
            # Single vote returned as dict, not list
            vote_list = [vote_list]

        for vote_record in vote_list:
            bill = vote_record.get("bill") or {}
            loader = VoteLoader(item=VoteItem())
            loader.add_value("politician_bioguide_id", bioguide_id)
            loader.add_value(
                "bill_number",
                bill.get("number") or vote_record.get("documentNumber", ""),
            )
            loader.add_value(
                "bill_title",
                bill.get("title") or vote_record.get("description", ""),
            )
            loader.add_value("vote_date", vote_record.get("date", ""))
            loader.add_value(
                "vote_choice", self._normalize_vote(vote_record.get("memberVoted", ""))
            )
            loader.add_value("congress_session", vote_record.get("congress", ""))
            loader.add_value("roll_call_number", vote_record.get("rollNumber", ""))
            loader.add_value("source_url", vote_record.get("url", ""))
            yield loader.load_item()

        # Follow vote pagination
        next_url = data.get("pagination", {}).get("next")
        if next_url:
            yield scrapy.Request(
                next_url,
                callback=self.parse_votes,
                cb_kwargs={"bioguide_id": bioguide_id},
                priority=-1,
            )

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _parse_name(self, member: dict) -> str:
        """Build a display name from the member dict.

        The list endpoint returns ``name`` as "Last, First" (e.g. "Adams, Alma S.").
        The detail endpoint may also have separate ``firstName``/``lastName`` fields.
        We prefer firstName+lastName when both are present, otherwise parse ``name``.
        """
        first = member.get("firstName", "").strip()
        last = member.get("lastName", "").strip()
        if first or last:
            return f"{first} {last}".strip()
        raw = member.get("name", "").strip()
        if "," in raw:
            last_part, first_part = raw.split(",", 1)
            return f"{first_part.strip()} {last_part.strip()}"
        return raw

    def _parse_party(self, party_name: str) -> str:
        """Map full party name to single-character code used in the Politician model."""
        key = party_name.lower().strip()
        return PARTY_MAP.get(key, "O")

    def _parse_chamber(self, terms) -> str:
        """Extract chamber from member terms list."""
        if not terms:
            return "other"
        latest = terms[-1] if isinstance(terms, list) else terms
        chamber_str = latest.get("chamber", "").lower()
        if "senate" in chamber_str:
            return "senate"
        elif "house" in chamber_str:
            return "house"
        return "other"

    def _normalize_vote(self, raw: str) -> str:
        """Normalize raw vote strings to VoteChoice values used in the Vote model."""
        mapping = {
            "yea": "Yea",
            "aye": "Yea",
            "yes": "Yea",
            "nay": "Nay",
            "no": "Nay",
            "present": "Present",
            "not voting": "NotVoting",
            "notvoting": "NotVoting",
            "": "NotVoting",
        }
        return mapping.get(raw.lower().strip(), "NotVoting")
