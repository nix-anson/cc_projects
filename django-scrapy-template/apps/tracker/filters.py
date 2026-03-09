"""django-filter FilterSets for tracker API endpoints."""
import django_filters

from .models import Decision, FundingRecord, Politician, Vote


class PoliticianFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="iexact")
    party = django_filters.CharFilter(lookup_expr="iexact")
    chamber = django_filters.CharFilter(lookup_expr="iexact")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Politician
        fields = ["state", "party", "chamber", "name"]


class VoteFilter(django_filters.FilterSet):
    politician = django_filters.NumberFilter()
    bill_number = django_filters.CharFilter(lookup_expr="icontains")
    vote_choice = django_filters.CharFilter()
    congress_session = django_filters.NumberFilter()
    date_from = django_filters.DateFilter(field_name="vote_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="vote_date", lookup_expr="lte")

    class Meta:
        model = Vote
        fields = ["politician", "bill_number", "vote_choice", "congress_session"]


class DecisionFilter(django_filters.FilterSet):
    politician = django_filters.NumberFilter()
    decision_type = django_filters.CharFilter()
    date_from = django_filters.DateFilter(field_name="date_issued", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date_issued", lookup_expr="lte")

    class Meta:
        model = Decision
        fields = ["politician", "decision_type"]


class FundingFilter(django_filters.FilterSet):
    politician = django_filters.NumberFilter()
    cycle_year = django_filters.NumberFilter()
    donor_category = django_filters.CharFilter(lookup_expr="icontains")
    min_amount = django_filters.NumberFilter(field_name="amount_cents", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount_cents", lookup_expr="lte")

    class Meta:
        model = FundingRecord
        fields = ["politician", "cycle_year", "donor_category"]
