from django.contrib.auth.models import AnonymousUser
from django_filters import rest_framework as filters
from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airport.filters import AirportFilter, OrderFilter, FlightFilter
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
from airport.pagination import CustomPagination
from airport.schemas.airport_schemas import (
    airplane_type_schema,
    airplane_schema,
    crew_schema,
    flight_schema,
    order_schema,
    ticket_schema,
    airport_schema,
    route_schema,
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


@airport_schema
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter


@route_schema
class RouteViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination

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


@airplane_type_schema
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = CustomPagination


@airplane_schema
class AirplaneViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination

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


@crew_schema
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = CustomPagination


@flight_schema
class FlightViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        queryset = Flight.objects.all()

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "route__source",
                "route__destination",
                "airplane__airplane_type",
                "crew",
            ).annotate(
                tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
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


@order_schema
class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination

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

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter


@ticket_schema
class TicketViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = TicketSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Ticket.objects.none()

        queryset = Ticket.objects.select_related("flight", "order").filter(
            order__user=self.request.user
        )

        return queryset
