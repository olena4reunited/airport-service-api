from django.db.models import F, Count
from django_filters import rest_framework as filters
from airport.models import Flight, Airport, Order


class FlightFilter(filters.FilterSet):
    departure_time = filters.DateTimeFilter(
        field_name="departure_time", lookup_expr="gte"
    )
    arrival_time = filters.DateTimeFilter(
        field_name="arrival_time", lookup_expr="lte"
    )
    route__source = filters.CharFilter(
        field_name="route__source__name", lookup_expr="icontains"
    )
    route__destination = filters.CharFilter(
        field_name="route__destination__name", lookup_expr="icontains"
    )
    tickets_available = filters.NumberFilter(method="filter_tickets_available")

    class Meta:
        model = Flight
        fields = [
            "departure_time",
            "arrival_time",
            "route__source",
            "route__destination",
            "tickets_available",
        ]

    def filter_tickets_available(self, queryset, name, value):
        return queryset.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        ).filter(tickets_available__gte=value)


class AirportFilter(filters.FilterSet):
    closest_big_city = filters.CharFilter(lookup_expr="icontains")
    name = filters.CharFilter(lookup_expr="icontains")
    routes = filters.NumberFilter(field_name="routes_from__id")

    class Meta:
        model = Airport
        fields = ["closest_big_city", "name", "routes"]


class OrderFilter(filters.FilterSet):
    created_at = filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )

    class Meta:
        model = Order
        fields = ["user", "created_at"]
