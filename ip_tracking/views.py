from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit


def get_rate(group, request):
    if request.user.is_authenticated:
        return "10/m"
    return "5/m"


@ratelimit(key="ip", rate=get_rate, block=True)
def login(request):
    return HttpResponse("Login page - Rate limit check passed.")
