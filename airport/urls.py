from rest_framework.routers import DefaultRouter

from airport.views import AirportViewSet

router = DefaultRouter()

router.register("airports", AirportViewSet, basename="airport")

urlpatterns = []

app_name = "airport"
