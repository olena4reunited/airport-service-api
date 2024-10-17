from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
)
from rest_framework import status
from user.serializers import UserSerializer


user_create_schema = extend_schema_view(
    post=extend_schema(
        description="Register a new user with the specified details. Users must provide a valid email and password.",
        request=UserSerializer,
        responses={
            status.HTTP_201_CREATED: UserSerializer,
            status.HTTP_400_BAD_REQUEST: {
                "description": "Bad Request",
                "examples": [
                    {
                        "id": "error",
                        "email": ["This field may not be blank."],
                        "password": ["This field may not be blank."],
                    }
                ],
            },
        },
        examples=[
            OpenApiExample(
                name="CreateUserRequest",
                description="An example request to create a user.",
                value={
                    "email": "example@example.com",
                    "password": "password123",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="CreateUserResponse",
                description="An example response after successfully creating a user.",
                value={
                    "id": 1,
                    "email": "example@example.com",
                    "is_active": True,
                    "is_staff": False,
                },
                response_only=True,
            ),
        ],
    )
)

user_manage_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve user data by user ID. Returns the details of the user including their email and status.",
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_404_NOT_FOUND: "User not found. Ensure the user ID is valid.",
        },
        examples=[
            OpenApiExample(
                name="GetUserResponse",
                description="An example response to get user data.",
                value={
                    "id": 1,
                    "email": "example@example.com",
                    "is_active": True,
                    "is_staff": False,
                },
                response_only=True,
            )
        ],
    ),
    put=extend_schema(
        description="Update the user's data. All fields must be provided. Ensure that the email is unique.",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: {
                "description": "Bad Request",
                "examples": [
                    {
                        "email": ["This field must be unique."],
                        "password": ["This field may not be blank."],
                    }
                ],
            },
            status.HTTP_404_NOT_FOUND: "User not found. Ensure the user ID is valid.",
        },
        examples=[
            OpenApiExample(
                name="UpdateUserRequest",
                description="An example request to update user data.",
                value={
                    "email": "updated@example.com",
                    "password": "newpassword123",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="UpdateUserResponse",
                description="An example response after successfully updating user data.",
                value={
                    "id": 1,
                    "email": "updated@example.com",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2023-10-16T12:34:56Z",
                },
                response_only=True,
            ),
        ],
    ),
    patch=extend_schema(
        description="Partially update user data. Only fields provided will be updated.",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: {
                "description": "Bad Request",
                "examples": [{"email": ["This field must be unique."]}],
            },
            status.HTTP_404_NOT_FOUND: "User not found. Ensure the user ID is valid.",
        },
        examples=[
            OpenApiExample(
                name="PartiallyUpdateUserRequest",
                description="An example request to partially update user data.",
                value={"email": "partialupdate@example.com"},
                request_only=True,
            ),
            OpenApiExample(
                name="PartiallyUpdateUserResponse",
                description="An example response after partially updating user data.",
                value={
                    "id": 1,
                    "email": "partialupdate@example.com",
                    "is_active": True,
                    "is_staff": False,
                },
                response_only=True,
            ),
        ],
    ),
)
