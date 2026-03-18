from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import SignupSerializer, SigninSerializer, UserSerializer, UpdateProfileSerializer


class LoginRateThrottle(AnonRateThrottle):
    rate = "10/hour"
    scope = "login"


def _token_response(user):
    """Return {token, user} payload used by frontend."""
    refresh = RefreshToken.for_user(user)
    return {
        "token": str(refresh.access_token),
        "user": UserSerializer(user).data,
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        errors = serializer.errors
        # Flatten errors to match frontend expectations: {errors:[{path,msg}]}
        flat = []
        for field, msgs in errors.items():
            for msg in msgs:
                flat.append({"path": field, "msg": str(msg)})
        return Response({"errors": flat}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    email = serializer.validated_data["email"]
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email is already registered."}, status=status.HTTP_409_CONFLICT)

    user = serializer.save()
    return Response(_token_response(user), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def signin(request):
    serializer = SigninSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "Invalid email or password."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(_token_response(user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({"user": UserSerializer(request.user).data})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UpdateProfileSerializer(data=request.data, context={"request": request})
    if not serializer.is_valid():
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    user = request.user
    if "name" in serializer.validated_data:
        user.name = serializer.validated_data["name"]
    if "email" in serializer.validated_data:
        new_email = serializer.validated_data["email"]
        if new_email != user.email and User.objects.filter(email=new_email).exists():
            return Response({"error": "Email is already registered."}, status=status.HTTP_409_CONFLICT)
        user.email = new_email
    try:
        user.save()
    except IntegrityError:
        return Response({"error": "Email is already registered."}, status=status.HTTP_409_CONFLICT)

    return Response({"user": UserSerializer(user).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    password = request.data.get("password", "")
    user = request.user
    if not user.check_password(password):
        return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
    user.delete()
    return Response({"success": True})

