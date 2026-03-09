"""Tests for tracker REST API endpoints."""
import pytest
from django.urls import reverse

from apps.tracker.models import Decision, Vote

from .factories import (
    AffectedGroupFactory,
    DecisionFactory,
    FundingRecordFactory,
    PoliticianFactory,
    VoteFactory,
)


# ── Politician ────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestPoliticianAPI:
    def test_list_politicians(self, client):
        PoliticianFactory.create_batch(5)
        response = client.get(reverse("politician-list"))
        assert response.status_code == 200
        assert response.data["count"] == 5

    def test_filter_by_state(self, client):
        PoliticianFactory.create_batch(3, state="CA")
        PoliticianFactory.create_batch(2, state="TX")
        response = client.get(reverse("politician-list"), {"state": "CA"})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_filter_by_party(self, client):
        PoliticianFactory.create_batch(2, party="D")
        PoliticianFactory.create_batch(3, party="R")
        response = client.get(reverse("politician-list"), {"party": "R"})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_retrieve_politician(self, client):
        politician = PoliticianFactory()
        VoteFactory.create_batch(5, politician=politician)
        response = client.get(reverse("politician-detail", args=[politician.pk]))
        assert response.status_code == 200
        assert response.data["name"] == politician.name

    def test_politician_votes_action(self, client):
        politician = PoliticianFactory()
        VoteFactory.create_batch(3, politician=politician)
        response = client.get(reverse("politician-votes", args=[politician.pk]))
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_politician_funding_action(self, client):
        politician = PoliticianFactory()
        FundingRecordFactory.create_batch(2, politician=politician)
        response = client.get(reverse("politician-funding", args=[politician.pk]))
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_404_for_missing_politician(self, client):
        response = client.get(reverse("politician-detail", args=[99999]))
        assert response.status_code == 404


# ── Vote ─────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestVoteAPI:
    def test_list_votes(self, client):
        VoteFactory.create_batch(4)
        response = client.get(reverse("vote-list"))
        assert response.status_code == 200
        assert response.data["count"] == 4

    def test_filter_by_vote_choice(self, client):
        VoteFactory.create_batch(3, vote_choice=Vote.VoteChoice.YEA)
        VoteFactory.create_batch(2, vote_choice=Vote.VoteChoice.NAY)
        response = client.get(reverse("vote-list"), {"vote_choice": "Yea"})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_filter_by_politician(self, client):
        p1 = PoliticianFactory()
        p2 = PoliticianFactory()
        VoteFactory.create_batch(2, politician=p1)
        VoteFactory.create_batch(3, politician=p2)
        response = client.get(reverse("vote-list"), {"politician": p1.pk})
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_filter_by_congress_session(self, client):
        VoteFactory.create_batch(2, congress_session=117)
        VoteFactory.create_batch(3, congress_session=118)
        response = client.get(reverse("vote-list"), {"congress_session": 118})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_retrieve_vote(self, client):
        vote = VoteFactory()
        response = client.get(reverse("vote-detail", args=[vote.pk]))
        assert response.status_code == 200
        assert response.data["bill_number"] == vote.bill_number


# ── Decision ──────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestDecisionAPI:
    def test_list_decisions(self, client):
        DecisionFactory.create_batch(3)
        response = client.get(reverse("decision-list"))
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_filter_by_decision_type(self, client):
        DecisionFactory.create_batch(2, decision_type=Decision.DecisionType.EXECUTIVE_ORDER)
        DecisionFactory.create_batch(1, decision_type=Decision.DecisionType.APPOINTMENT)
        response = client.get(
            reverse("decision-list"), {"decision_type": "executive_order"}
        )
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_filter_by_politician(self, client):
        p = PoliticianFactory()
        DecisionFactory.create_batch(2, politician=p)
        DecisionFactory.create_batch(3)
        response = client.get(reverse("decision-list"), {"politician": p.pk})
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_retrieve_decision(self, client):
        decision = DecisionFactory()
        response = client.get(reverse("decision-detail", args=[decision.pk]))
        assert response.status_code == 200
        assert response.data["title"] == decision.title


# ── AffectedGroup ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestAffectedGroupAPI:
    def test_list_affected_groups(self, client):
        AffectedGroupFactory.create_batch(3)
        response = client.get(reverse("affectedgroup-list"))
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_retrieve_affected_group(self, client):
        group = AffectedGroupFactory(name="Small Business Owners")
        response = client.get(reverse("affectedgroup-detail", args=[group.pk]))
        assert response.status_code == 200
        assert response.data["name"] == "Small Business Owners"


# ── FundingRecord ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFundingAPI:
    def test_list_funding(self, client):
        FundingRecordFactory.create_batch(4)
        response = client.get(reverse("fundingrecord-list"))
        assert response.status_code == 200
        assert response.data["count"] == 4

    def test_filter_by_cycle_year(self, client):
        FundingRecordFactory.create_batch(2, cycle_year=2022)
        FundingRecordFactory.create_batch(3, cycle_year=2024)
        response = client.get(reverse("fundingrecord-list"), {"cycle_year": 2024})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_filter_by_politician(self, client):
        p = PoliticianFactory()
        FundingRecordFactory.create_batch(3, politician=p)
        FundingRecordFactory.create_batch(2)
        response = client.get(reverse("fundingrecord-list"), {"politician": p.pk})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_retrieve_funding_record(self, client):
        record = FundingRecordFactory(donor_name="ACME Corp")
        response = client.get(reverse("fundingrecord-detail", args=[record.pk]))
        assert response.status_code == 200
        assert response.data["donor_name"] == "ACME Corp"
