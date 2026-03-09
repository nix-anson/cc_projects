"""Tests for tracker models."""
import pytest

from apps.tracker.models import DecisionAffectedGroup

from .factories import AffectedGroupFactory, DecisionFactory, PoliticianFactory, VoteFactory


@pytest.mark.django_db
class TestPoliticianModel:
    def test_str_representation(self):
        p = PoliticianFactory(name="Jane Smith", party="D", state="CA")
        assert str(p) == "Jane Smith (D-CA)"

    def test_vote_relationship(self):
        politician = PoliticianFactory()
        VoteFactory.create_batch(3, politician=politician)
        assert politician.votes.count() == 3


@pytest.mark.django_db
class TestDecisionAffectedGroup:
    def test_through_model(self):
        decision = DecisionFactory()
        group = AffectedGroupFactory()
        dg = DecisionAffectedGroup.objects.create(
            decision=decision,
            affected_group=group,
            impact_type=DecisionAffectedGroup.ImpactType.POSITIVE,
            estimated_people_affected=1000000,
        )
        assert dg.impact_type == "positive"
        assert decision.affected_groups.count() == 1
