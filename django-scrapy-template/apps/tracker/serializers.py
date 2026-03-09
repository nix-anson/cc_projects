"""DRF serializers for tracker models."""
from rest_framework import serializers

from .models import (
    AffectedGroup,
    Decision,
    DecisionAffectedGroup,
    FundingRecord,
    Politician,
    Source,
    Vote,
)


class AffectedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectedGroup
        fields = ["id", "name", "category", "description"]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "name", "url", "source_type", "reliability_score"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            "id",
            "politician",
            "bill_number",
            "bill_title",
            "vote_date",
            "vote_choice",
            "congress_session",
            "roll_call_number",
            "source",
            "created_at",
        ]


class DecisionAffectedGroupSerializer(serializers.ModelSerializer):
    affected_group = AffectedGroupSerializer(read_only=True)

    class Meta:
        model = DecisionAffectedGroup
        fields = ["affected_group", "impact_type", "impact_summary", "estimated_people_affected"]


class DecisionSerializer(serializers.ModelSerializer):
    affected_groups_detail = DecisionAffectedGroupSerializer(
        source="decisionaffectedgroup_set", many=True, read_only=True
    )

    class Meta:
        model = Decision
        fields = [
            "id",
            "politician",
            "title",
            "decision_type",
            "date_issued",
            "summary",
            "full_text",
            "source",
            "affected_groups_detail",
            "created_at",
        ]


class PoliticianListSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    decision_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Politician
        fields = [
            "id",
            "name",
            "party",
            "chamber",
            "state",
            "district",
            "photo_url",
            "official_url",
            "term_start",
            "term_end",
            "vote_count",
            "decision_count",
        ]


class PoliticianDetailSerializer(serializers.ModelSerializer):
    recent_votes = VoteSerializer(source="votes", many=True, read_only=True)
    recent_decisions = DecisionSerializer(source="decisions", many=True, read_only=True)

    class Meta:
        model = Politician
        fields = [
            "id",
            "name",
            "party",
            "chamber",
            "state",
            "district",
            "bioguide_id",
            "votesmart_id",
            "opensecrets_id",
            "bio",
            "photo_url",
            "official_url",
            "term_start",
            "term_end",
            "recent_votes",
            "recent_decisions",
            "created_at",
            "updated_at",
        ]


class FundingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingRecord
        fields = [
            "id",
            "politician",
            "donor_name",
            "donor_category",
            "amount_cents",
            "cycle_year",
            "source",
        ]
