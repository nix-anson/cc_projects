"""Spider for scraping politician biographies from Wikipedia."""
import scrapy


class WikipediaBioSpider(scrapy.Spider):
    """Scrape politician bios from Wikipedia.

    Used to enrich existing Politician records with bio text.
    """

    name = "wikipedia_bio"
    source_name = "Wikipedia"
    source_url = "https://wikipedia.org"
    source_type = "other"
    reliability_score = 0.7

    async def start(self):
        """Fetch politicians missing bios from the database."""
        from apps.tracker.models import Politician

        politicians = Politician.objects.filter(bio="").values("name", "bioguide_id")
        for p in politicians[:50]:  # Limit for politeness
            name_slug = p["name"].replace(" ", "_")
            url = f"https://en.wikipedia.org/wiki/{name_slug}"
            yield scrapy.Request(
                url,
                callback=self.parse_bio,
                cb_kwargs={"bioguide_id": p["bioguide_id"]},
            )

    def parse_bio(self, response, bioguide_id):
        # Extract first paragraph from Wikipedia article
        paragraphs = response.css("#mw-content-text p::text").getall()
        bio = " ".join(p.strip() for p in paragraphs[:3] if p.strip())

        if bio:
            from apps.tracker.models import Politician

            Politician.objects.filter(bioguide_id=bioguide_id).update(bio=bio[:2000])
