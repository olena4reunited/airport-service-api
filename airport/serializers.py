from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Ticket,
    Order,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class AirportRouteSerializer(AirportSerializer):
    class Meta:
        model = Airport
        fields = ["name", "closest_big_city"]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteListSerializer(RouteSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportRouteSerializer(read_only=True)
    destination = AirportRouteSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteFlightSerializer(RouteSerializer):
    source = AirportRouteSerializer(read_only=True)
    destination = AirportRouteSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ["source", "destination", "distance"]


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ["id", "name", "airplane_type", "capacity"]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")

    class Meta:
        model = Airplane
        fields = ["id", "name", "airplane_type", "capacity"]


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        source="airplane_type.name", read_only=True
    )

    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_row",
            "capacity",
        ]


class AirplaneFlightSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        source="airplane_type.name", read_only=True
    )

    class Meta:
        model = Airplane
        fields = ["name", "airplane_type"]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class CrewFlightSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = ["first_name", "last_name"]


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        ]


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(many=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "tickets_available",
        ]


class FlightRetrieveSerializer(FlightSerializer):
    route = RouteFlightSerializer(read_only=True)
    airplane = AirplaneFlightSerializer(read_only=True)
    crew = CrewFlightSerializer(many=True, read_only=True)
    taken_seats = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_seats",
        ]

    def get_taken_seats(self, obj):
        return (
            (ticket.row, ticket.seat)
            for ticket in obj.tickets.order_by("row", "seat")
        )


class FlightTicketSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(many=True)

    class Meta:
        model = Flight
        fields = [
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        ]


class TicketSerializer(serializers.ModelSerializer):
    flight = FlightTicketSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight"]


class TicketOrderSerializer(TicketSerializer):
    flight = FlightTicketSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["row", "seat", "flight"]


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]


class OrderListSerializer(OrderSerializer):
    tickets = TicketOrderSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]
