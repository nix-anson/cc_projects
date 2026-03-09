"""Django admin configuration for tracker models."""
from django.contrib import admin

from .models import (
    AffectedGroup,
    Decision,
    DecisionAffectedGroup,
    FundingRecord,
    Politician,
    Source,
    Vote,
)


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    fields = ("bill_number", "bill_title", "vote_date", "vote_choice")
    readonly_fields = ("created_at",)


class DecisionInline(admin.TabularInline):
    model = Decision
    extra = 0
    fields = ("title", "decision_type", "date_issued")


class FundingInline(admin.TabularInline):
    model = FundingRecord
    extra = 0
    fields = ("donor_name", "donor_category", "amount_cents", "cycle_year")


class DecisionAffectedGroupInline(admin.TabularInline):
    model = DecisionAffectedGroup
    extra = 0
    fields = ("affected_group", "impact_type", "impact_summary", "estimated_people_affected")


@admin.register(Politician)
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ("name", "party", "chamber", "state", "district", "bioguide_id")
    list_filter = ("party", "chamber", "state")
    search_fields = ("name", "bioguide_id", "state")
    inlines = [VoteInline, DecisionInline, FundingInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("politician", "bill_number", "vote_date", "vote_choice", "congress_session")
    list_filter = ("vote_choice", "congress_session")
    search_fields = ("politician__name", "bill_number", "bill_title")
    date_hierarchy = "vote_date"
    readonly_fields = ("created_at", "updated_at")


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ("politician", "title", "decision_type", "date_issued")
    list_filter = ("decision_type",)
    search_fields = ("politician__name", "title", "summary")
    date_hierarchy = "date_issued"
    inlines = [DecisionAffectedGroupInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(AffectedGroup)
class AffectedGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "url", "reliability_score")
    list_filter = ("source_type",)
    search_fields = ("name", "url")


@admin.register(FundingRecord)
class FundingRecordAdmin(admin.ModelAdmin):
    list_display = ("politician", "donor_name", "amount_cents", "cycle_year")
    list_filter = ("cycle_year", "donor_category")
    search_fields = ("politician__name", "donor_name")
    readonly_fields = ("created_at", "updated_at")
