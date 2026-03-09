"""factory-boy factories for tracker models."""
import factory
from factory.django import DjangoModelFactory

from apps.tracker.models import AffectedGroup, Decision, FundingRecord, Politician, Source, Vote


class PoliticianFactory(DjangoModelFactory):
    class Meta:
        model = Politician

    name = factory.Sequence(lambda n: f"Politician {n}")
    party = Politician.Party.DEMOCRAT
    chamber = Politician.Chamber.SENATE
    state = "CA"
    bioguide_id = factory.Sequence(lambda n: f"P{n:06d}")


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    politician = factory.SubFactory(PoliticianFactory)
    bill_number = factory.Sequence(lambda n: f"H.R.{n}")
    bill_title = factory.Sequence(lambda n: f"Test Bill {n}")
    vote_date = factory.Faker("date_object")
    vote_choice = Vote.VoteChoice.YEA
    congress_session = 118


class AffectedGroupFactory(DjangoModelFactory):
    class Meta:
        model = AffectedGroup

    name = factory.Sequence(lambda n: f"Group {n}")
    category = AffectedGroup.Category.ECONOMIC


class DecisionFactory(DjangoModelFactory):
    class Meta:
        model = Decision

    politician = factory.SubFactory(PoliticianFactory)
    title = factory.Sequence(lambda n: f"Decision {n}")
    decision_type = Decision.DecisionType.PUBLIC_STATEMENT
    date_issued = factory.Faker("date_object")
    summary = factory.Faker("paragraph")


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source

    name = factory.Sequence(lambda n: f"Source {n}")
    url = factory.Sequence(lambda n: f"https://example.com/source-{n}")
    source_type = Source.SourceType.GOVERNMENT


class FundingRecordFactory(DjangoModelFactory):
    class Meta:
        model = FundingRecord

    politician = factory.SubFactory(PoliticianFactory)
    donor_name = factory.Faker("company")
    amount_cents = factory.Faker("random_int", min=100, max=500000)
    cycle_year = 2024
