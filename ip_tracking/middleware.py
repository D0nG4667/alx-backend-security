from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ip_geolocation.utils import get_geolocation
from .models import RequestLog, BlockedIP


class IpTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP address
        ip_address = self.get_client_ip(request)

        # Check if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access Denied: Your IP is blacklisted.")

        # Log the request
        location = cache.get(f"ip_geo_{ip_address}")
        if not location:
            try:
                location = get_geolocation(request)
                cache.set(f"ip_geo_{ip_address}", location, 86400)  # Cache for 24 hours
            except Exception:
                location = None

        country = location.get("country", {}).get("name") if location else None
        city = location.get("city") if location else None

        RequestLog.objects.create(
            ip_address=ip_address, path=request.path, country=country, city=city
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
