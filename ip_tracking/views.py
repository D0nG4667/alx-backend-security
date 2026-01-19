from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render


def home(request):
    return render(request, "ip_tracking/home.html")


def get_rate(group, request):
    if request.user.is_authenticated:
        return "10/m"
    return "5/m"


@swagger_auto_schema(
    method="get",
    operation_description="Test Rate Limiting: 5/m anon, 10/m auth",
    responses={200: "Login Successful", 403: "Rate Limit Exceeded"},
)
@api_view(["GET"])
@permission_classes([AllowAny])
@ratelimit(key="ip", rate=get_rate, block=True)
def login(request):
    return Response({"message": "Login page - Rate limit check passed."})


@swagger_auto_schema(
    method="get",
    operation_description="Test Authentication: Only accessible to logged-in users",
    responses={200: "Access Granted", 401: "Unauthorized"},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def secure_data(request):
    return Response(
        {"message": "You have accessed protected data!", "user": request.user.username}
    )
