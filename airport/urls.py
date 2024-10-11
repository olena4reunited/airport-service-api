from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import AirportViewSet, RouteViewSet

router = DefaultRouter()

router.register("airports", AirportViewSet, basename="airport")
router.register("routes", RouteViewSet, basename="route")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "airport"
