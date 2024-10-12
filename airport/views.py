from django.contrib.auth.models import AnonymousUser
from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    TicketSerializer,
    RouteRetrieveSerializer,
    RouteListSerializer,
    AirplaneRetrieveSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderListSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Route.objects.all()

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("source", "destination")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer

        return RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Airplane.objects.all()

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("airplane_type")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneRetrieveSerializer

        return AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Flight.objects.all()

        if self.action == "list":
            queryset = (
                queryset.select_related(
                    "route__source",
                    "route__destination",
                    "airplane__airplane_type",
                )
                .prefetch_related(
                    "crew",
                )
                .annotate(
                    tickets_available=(
                        F("airplane__rows") * F("airplane__seats_in_row")
                        - Count("tickets")
                    )
                )
            )
        if self.action == "retrieve":
            queryset = queryset.select_related(
                "route__source",
                "route__destination",
                "airplane__airplane_type",
            ).prefetch_related(
                "crew",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerializer

        return FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Order.objects.none()

        return (
            Order.objects.prefetch_related("tickets")
            .filter(user=self.request.user, tickets__isnull=False)
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = TicketSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Ticket.objects.none()

        queryset = Ticket.objects.select_related("flight", "order").filter(
            order__user=self.request.user
        )

        return queryset
