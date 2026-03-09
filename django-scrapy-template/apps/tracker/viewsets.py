"""DRF ViewSets for tracker API."""
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import DecisionFilter, FundingFilter, PoliticianFilter, VoteFilter
from .models import AffectedGroup, Decision, FundingRecord, Politician, Source, Vote
from .serializers import (
    AffectedGroupSerializer,
    DecisionSerializer,
    FundingRecordSerializer,
    PoliticianDetailSerializer,
    PoliticianListSerializer,
    SourceSerializer,
    VoteSerializer,
)


class PoliticianViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Politician.objects.annotate(
        vote_count=Count("votes", distinct=True),
        decision_count=Count("decisions", distinct=True),
    ).order_by("name")
    filterset_class = PoliticianFilter
    search_fields = ["name", "state", "bio"]
    ordering_fields = ["name", "state", "party", "vote_count"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PoliticianDetailSerializer
        return PoliticianListSerializer

    @action(detail=True, methods=["get"])
    def votes(self, request, pk=None):
        politician = self.get_object()
        votes = politician.votes.all().order_by("-vote_date")[:50]
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def funding(self, request, pk=None):
        politician = self.get_object()
        records = politician.funding_records.all().order_by("-cycle_year")[:50]
        serializer = FundingRecordSerializer(records, many=True)
        return Response(serializer.data)


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.select_related("politician", "source").order_by("-vote_date")
    serializer_class = VoteSerializer
    filterset_class = VoteFilter
    search_fields = ["bill_number", "bill_title", "politician__name"]
    ordering_fields = ["vote_date", "politician__name", "bill_number"]


class DecisionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Decision.objects.select_related("politician", "source").prefetch_related(
        "affected_groups"
    ).order_by("-date_issued")
    serializer_class = DecisionSerializer
    filterset_class = DecisionFilter
    search_fields = ["title", "summary", "politician__name"]
    ordering_fields = ["date_issued", "politician__name", "decision_type"]


class AffectedGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AffectedGroup.objects.all()
    serializer_class = AffectedGroupSerializer
    search_fields = ["name", "description"]


class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    search_fields = ["name", "url"]


class FundingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FundingRecord.objects.select_related("politician", "source").order_by("-cycle_year")
    serializer_class = FundingRecordSerializer
    filterset_class = FundingFilter
    search_fields = ["politician__name", "donor_name", "donor_category"]
    ordering_fields = ["cycle_year", "amount_cents", "politician__name"]
