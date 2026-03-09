"""Core tracker domain models."""
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from apps.core.models import TimeStampedModel


class AffectedGroup(TimeStampedModel):
    """A group of people affected by political decisions."""

    class Category(models.TextChoices):
        ECONOMIC = "economic", "Economic"
        DEMOGRAPHIC = "demographic", "Demographic"
        GEOGRAPHIC = "geographic", "Geographic"
        INDUSTRY = "industry", "Industry"
        ENVIRONMENTAL = "environmental", "Environmental"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Source(TimeStampedModel):
    """Data source reference."""

    class SourceType(models.TextChoices):
        GOVERNMENT = "government", "Government"
        NEWS = "news", "News"
        NONPROFIT = "nonprofit", "Non-Profit"
        ACADEMIC = "academic", "Academic"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=1000)
    source_type = models.CharField(max_length=20, choices=SourceType.choices)
    reliability_score = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Politician(TimeStampedModel):
    """Represents an elected official or political figure."""

    class Party(models.TextChoices):
        DEMOCRAT = "D", "Democrat"
        REPUBLICAN = "R", "Republican"
        INDEPENDENT = "I", "Independent"
        OTHER = "O", "Other"

    class Chamber(models.TextChoices):
        SENATE = "senate", "Senate"
        HOUSE = "house", "House of Representatives"
        EXECUTIVE = "executive", "Executive"
        OTHER = "other", "Other"

    # Identity
    name = models.CharField(max_length=255, db_index=True)
    party = models.CharField(max_length=1, choices=Party.choices)
    chamber = models.CharField(max_length=10, choices=Chamber.choices)
    state = models.CharField(max_length=2, db_index=True)
    district = models.CharField(max_length=10, blank=True)

    # External IDs for cross-referencing scraped data
    bioguide_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    votesmart_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    opensecrets_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Bio
    bio = models.TextField(blank=True)
    photo_url = models.URLField(max_length=500, blank=True)
    official_url = models.URLField(max_length=500, blank=True)
    term_start = models.DateField(null=True, blank=True)
    term_end = models.DateField(null=True, blank=True)

    # Full-text search
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"{self.name} ({self.party}-{self.state})"


class Vote(TimeStampedModel):
    """A politician's vote on a specific bill or resolution."""

    class VoteChoice(models.TextChoices):
        YEA = "Yea", "Yea"
        NAY = "Nay", "Nay"
        PRESENT = "Present", "Present"
        NOT_VOTING = "NotVoting", "Not Voting"

    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, related_name="votes")
    bill_number = models.CharField(max_length=50, db_index=True)
    bill_title = models.CharField(max_length=500)
    vote_date = models.DateField(db_index=True)
    vote_choice = models.CharField(max_length=10, choices=VoteChoice.choices)
    congress_session = models.IntegerField(null=True, blank=True)
    roll_call_number = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-vote_date"]
        unique_together = [["politician", "bill_number", "vote_date"]]

    def __str__(self):
        return f"{self.politician.name} — {self.bill_number} ({self.vote_choice})"


class Decision(TimeStampedModel):
    """A significant decision, executive action, or policy position."""

    class DecisionType(models.TextChoices):
        EXECUTIVE_ORDER = "executive_order", "Executive Order"
        BILL_SPONSORSHIP = "bill_sponsorship", "Bill Sponsorship"
        PUBLIC_STATEMENT = "public_statement", "Public Statement"
        COMMITTEE_ACTION = "committee_action", "Committee Action"
        APPOINTMENT = "appointment", "Appointment"
        OTHER = "other", "Other"

    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, related_name="decisions")
    title = models.CharField(max_length=500)
    decision_type = models.CharField(max_length=20, choices=DecisionType.choices)
    date_issued = models.DateField(db_index=True)
    summary = models.TextField()
    full_text = models.TextField(blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    affected_groups = models.ManyToManyField(
        AffectedGroup,
        through="DecisionAffectedGroup",
        related_name="decisions",
        blank=True,
    )

    class Meta:
        ordering = ["-date_issued"]

    def __str__(self):
        return f"{self.politician.name} — {self.title}"


class DecisionAffectedGroup(TimeStampedModel):
    """Through model for Decision <-> AffectedGroup with impact metadata."""

    class ImpactType(models.TextChoices):
        POSITIVE = "positive", "Positive"
        NEGATIVE = "negative", "Negative"
        MIXED = "mixed", "Mixed"
        NEUTRAL = "neutral", "Neutral"
        UNKNOWN = "unknown", "Unknown"

    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    affected_group = models.ForeignKey(AffectedGroup, on_delete=models.CASCADE)
    impact_type = models.CharField(
        max_length=10, choices=ImpactType.choices, default=ImpactType.UNKNOWN
    )
    impact_summary = models.TextField(blank=True)
    estimated_people_affected = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = [["decision", "affected_group"]]

    def __str__(self):
        return f"{self.decision} -> {self.affected_group} ({self.impact_type})"


class FundingRecord(TimeStampedModel):
    """Campaign finance / funding data for a politician."""

    politician = models.ForeignKey(
        Politician, on_delete=models.CASCADE, related_name="funding_records"
    )
    donor_name = models.CharField(max_length=500)
    donor_category = models.CharField(max_length=255, blank=True)
    amount_cents = models.BigIntegerField()
    cycle_year = models.IntegerField(db_index=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-cycle_year", "-amount_cents"]

    def __str__(self):
        return (
            f"{self.politician.name} <- {self.donor_name} "
            f"${self.amount_cents / 100:.2f} ({self.cycle_year})"
        )
