"""URL routing for the tracker app."""
from rest_framework.routers import DefaultRouter

from .viewsets import (
    AffectedGroupViewSet,
    DecisionViewSet,
    FundingViewSet,
    PoliticianViewSet,
    SourceViewSet,
    VoteViewSet,
)

router = DefaultRouter()
router.register("politicians", PoliticianViewSet)
router.register("votes", VoteViewSet)
router.register("decisions", DecisionViewSet)
router.register("affected-groups", AffectedGroupViewSet)
router.register("sources", SourceViewSet)
router.register("funding", FundingViewSet)

urlpatterns = router.urls
