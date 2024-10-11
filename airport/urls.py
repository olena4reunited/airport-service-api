from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
)

router = DefaultRouter()

router.register(r"airports", AirportViewSet, basename="airport")
router.register(r"routes", RouteViewSet, basename="route")
router.register(
    r"airplane_types", AirplaneTypeViewSet, basename="airplane-type"
)
router.register(r"airplanes", AirplaneViewSet, basename="airplane")
router.register(r"crews", CrewViewSet, basename="crew")

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
