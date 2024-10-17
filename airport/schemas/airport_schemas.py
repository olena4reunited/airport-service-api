from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
)
from rest_framework import status
from airport.serializers import (
    AirportSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    CrewSerializer,
    OrderListSerializer,
    OrderSerializer,
    TicketSerializer,
    RouteSerializer,
    FlightSerializer,
    AirplaneSerializer,
)


route_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of routes with optional filtering.",
        responses={
            status.HTTP_200_OK: RouteListSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListRoutesResponse",
                description="An example response for listing routes.",
                value=[
                    {
                        "id": 1,
                        "source": {"id": 1, "name": "JFK Airport"},
                        "destination": {"id": 2, "name": "LAX Airport"},
                        "distance": 3971,
                    },
                    {
                        "id": 2,
                        "source": {"id": 3, "name": "ORD Airport"},
                        "destination": {"id": 4, "name": "DFW Airport"},
                        "distance": 802,
                    },
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new route.",
        request=RouteSerializer,
        responses={
            status.HTTP_201_CREATED: RouteRetrieveSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateRouteRequest",
                description="An example request to create a new route.",
                value={"source": 1, "destination": 2, "distance": 3971},
                request_only=True,
            ),
            OpenApiExample(
                name="CreateRouteResponse",
                description="An example response after creating a route.",
                value={
                    "id": 3,
                    "source": {"id": 1, "name": "JFK Airport"},
                    "destination": {"id": 2, "name": "LAX Airport"},
                    "distance": 3971,
                },
                response_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific route.",
        responses={
            status.HTTP_200_OK: RouteRetrieveSerializer,
            status.HTTP_404_NOT_FOUND: "Route not found",
        },
        examples=[
            OpenApiExample(
                name="RetrieveRouteResponse",
                description="An example response for retrieving a route.",
                value={
                    "id": 1,
                    "source": {"id": 1, "name": "JFK Airport"},
                    "destination": {"id": 2, "name": "LAX Airport"},
                    "distance": 3971,
                },
                response_only=True,
            )
        ],
    ),
    update=extend_schema(
        description="Update an existing route.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: RouteRetrieveSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Route not found",
        },
        examples=[
            OpenApiExample(
                name="UpdateRouteRequest",
                description="An example request to update a route.",
                value={"source": 1, "destination": 2, "distance": 4000},
                request_only=True,
            ),
            OpenApiExample(
                name="UpdateRouteResponse",
                description="An example response after updating a route.",
                value={
                    "id": 1,
                    "source": {"id": 1, "name": "JFK Airport"},
                    "destination": {"id": 2, "name": "LAX Airport"},
                    "distance": 4000,
                },
                response_only=True,
            ),
        ],
    ),
    partial_update=extend_schema(
        description="Partially update an existing route.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: RouteRetrieveSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Route not found",
        },
        examples=[
            OpenApiExample(
                name="PartiallyUpdateRouteRequest",
                description="An example request to partially update a route.",
                value={"distance": 3900},
                request_only=True,
            ),
            OpenApiExample(
                name="PartiallyUpdateRouteResponse",
                description="An example response after partially updating a route.",
                value={
                    "id": 1,
                    "source": {"id": 1, "name": "JFK Airport"},
                    "destination": {"id": 2, "name": "LAX Airport"},
                    "distance": 3900,
                },
                response_only=True,
            ),
        ],
    ),
    delete=extend_schema(
        description="Delete a specific route.",
        responses={
            status.HTTP_204_NO_CONTENT: "Route deleted successfully",
            status.HTTP_404_NOT_FOUND: "Route not found",
        },
        examples=[
            OpenApiExample(
                name="DeleteRouteResponse",
                description="An example response after deleting a route.",
                value=None,
                response_only=True,
            )
        ],
    ),
)


airport_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of airports with optional filtering.",
        responses={
            status.HTTP_200_OK: AirportSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListAirportsResponse",
                description="An example response for listing airports.",
                value=[
                    {
                        "id": 1,
                        "name": "JFK Airport",
                        "closest_big_city": "New York",
                    },
                    {
                        "id": 2,
                        "name": "LAX Airport",
                        "closest_big_city": "Los Angeles",
                    },
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Register a new airport.",
        request=AirportSerializer,
        responses={
            status.HTTP_201_CREATED: AirportSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateAirportRequest",
                description="An example request to create a new airport.",
                value={"name": "New Airport", "closest_big_city": "New City"},
                request_only=True,
            ),
            OpenApiExample(
                name="CreateAirportResponse",
                description="An example response after creating an airport.",
                value={
                    "id": 3,
                    "name": "New Airport",
                    "closest_big_city": "New City",
                },
                response_only=True,
            ),
        ],
    ),
)


flight_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of flights with optional filtering by departure time, arrival time, and available tickets.",
        parameters=[
            {
                "name": "departure_time",
                "required": False,
                "type": "string",
                "format": "date-time",
                "description": "Filter flights departing after this time.",
            },
            {
                "name": "arrival_time",
                "required": False,
                "type": "string",
                "format": "date-time",
                "description": "Filter flights arriving before this time.",
            },
            {
                "name": "route__source",
                "required": False,
                "type": "string",
                "description": "Filter flights by the source airport name.",
            },
            {
                "name": "route__destination",
                "required": False,
                "type": "string",
                "description": "Filter flights by the destination airport name.",
            },
            {
                "name": "tickets_available",
                "required": False,
                "type": "integer",
                "description": "Filter flights by the minimum number of available tickets.",
            },
        ],
        responses={
            status.HTTP_200_OK: FlightListSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListFlightsResponse",
                description="An example response for listing flights.",
                value=[
                    {
                        "id": 1,
                        "route": "JFK - LAX",
                        "airplane": "Boeing 737",
                        "departure_time": "2023-10-20T15:30:00Z",
                        "arrival_time": "2023-10-20T18:00:00Z",
                        "tickets_available": 30,
                    }
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new flight.",
        request=FlightSerializer,
        responses={
            status.HTTP_201_CREATED: FlightSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateFlightRequest",
                description="An example request to create a new flight.",
                value={
                    "route": 1,
                    "airplane": 1,
                    "departure_time": "2023-10-20T15:30:00Z",
                    "arrival_time": "2023-10-20T18:00:00Z",
                    "crew": [1, 2],
                },
                request_only=True,
            ),
            OpenApiExample(
                name="CreateFlightResponse",
                description="An example response after creating a flight.",
                value={
                    "id": 1,
                    "route": 1,
                    "airplane": 1,
                    "departure_time": "2023-10-20T15:30:00Z",
                    "arrival_time": "2023-10-20T18:00:00Z",
                },
                response_only=True,
            ),
        ],
    ),
)


airplane_type_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of airplane types.",
        responses={
            status.HTTP_200_OK: AirplaneTypeSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListAirplaneTypesResponse",
                description="An example response for listing airplane types.",
                value=[
                    {"id": 1, "name": "Boeing 737"},
                    {"id": 2, "name": "Airbus A320"},
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_201_CREATED: AirplaneTypeSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateAirplaneTypeRequest",
                description="An example request to create a new airplane type.",
                value={"name": "Boeing 747"},
                request_only=True,
            ),
            OpenApiExample(
                name="CreateAirplaneTypeResponse",
                description="An example response after creating an airplane type.",
                value={"id": 3, "name": "Boeing 747"},
                response_only=True,
            ),
        ],
    ),
)


airplane_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of airplanes with optional filtering.",
        responses={
            status.HTTP_200_OK: AirplaneListSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListAirplanesResponse",
                description="An example response for listing airplanes.",
                value=[
                    {
                        "id": 1,
                        "name": "Boeing 737",
                        "airplane_type": "Boeing 737",
                        "capacity": 180,
                    }
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new airplane.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_201_CREATED: AirplaneSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateAirplaneRequest",
                description="An example request to create a new airplane.",
                value={
                    "name": "Boeing 787",
                    "rows": 10,
                    "seats_in_row": 6,
                    "airplane_type": 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                name="CreateAirplaneResponse",
                description="An example response after creating an airplane.",
                value={
                    "id": 2,
                    "name": "Boeing 787",
                    "rows": 10,
                    "seats_in_row": 6,
                    "capacity": 60,
                },
                response_only=True,
            ),
        ],
    ),
)


crew_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of crew members.",
        responses={
            status.HTTP_200_OK: CrewSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListCrewResponse",
                description="An example response for listing crew members.",
                value=[{"id": 1, "name": "John Doe", "role": "Pilot"}],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new crew member.",
        request=CrewSerializer,
        responses={
            status.HTTP_201_CREATED: CrewSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateCrewRequest",
                description="An example request to create a new crew member.",
                value={"name": "Jane Smith", "role": "Co-Pilot"},
                request_only=True,
            ),
            OpenApiExample(
                name="CreateCrewResponse",
                description="An example response after creating a crew member.",
                value={"id": 2, "name": "Jane Smith", "role": "Co-Pilot"},
                response_only=True,
            ),
        ],
    ),
)


order_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of orders associated with the logged-in user.",
        responses={
            status.HTTP_200_OK: OrderListSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListOrdersResponse",
                description="An example response for listing user orders.",
                value=[
                    {
                        "id": 1,
                        "created_at": "2023-10-10T12:00:00Z",
                        "tickets": [
                            {"row": 1, "seat": 1, "flight": "Flight ID 1"}
                        ],
                    }
                ],
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        description="Create a new order.",
        request=OrderSerializer,
        responses={
            status.HTTP_201_CREATED: OrderSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        examples=[
            OpenApiExample(
                name="CreateOrderRequest",
                description="An example request to create a new order.",
                value={"tickets": [1, 2]},
                request_only=True,
            ),
            OpenApiExample(
                name="CreateOrderResponse",
                description="An example response after creating an order.",
                value={
                    "id": 2,
                    "created_at": "2023-10-10T12:00:00Z",
                    "tickets": [],
                },
                response_only=True,
            ),
        ],
    ),
)


ticket_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of tickets associated with the logged-in user's orders.",
        responses={
            status.HTTP_200_OK: TicketSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                name="ListTicketsResponse",
                description="An example response for listing user tickets.",
                value=[
                    {
                        "id": 1,
                        "row": 1,
                        "seat": 1,
                        "flight": {
                            "id": 1,
                            "route": "JFK - LAX",
                            "departure_time": "2023-10-20T15:30:00Z",
                        },
                    }
                ],
                response_only=True,
            )
        ],
    ),
)
