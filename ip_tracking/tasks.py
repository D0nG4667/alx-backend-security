from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # 1. Flag IPs with > 100 requests in the last hour
    high_traffic_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=Count("id"))
        .filter(request_count__gt=100)
    )

    for item in high_traffic_ips:
        ip = item["ip_address"]
        count = item["request_count"]
        if not SuspiciousIP.objects.filter(
            ip_address=ip, reason__contains="High traffic"
        ).exists():
            SuspiciousIP.objects.create(
                ip_address=ip, reason=f"High traffic: {count} requests in last hour"
            )

    # 2. Flag IPs accessing sensitive paths
    sensitive_paths = ["/admin/", "/login/"]
    # Note: Using __contains or exact match depends on requirement.
    # Let's assume exact start or presence.

    suspicious_path_logs = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
        .values("ip_address", "path")
        .distinct()
    )

    # Note: This is simpler than regex for now. Can expand to "path__startswith='/admin'" if needed.

    for log in suspicious_path_logs:
        ip = log["ip_address"]
        path = log["path"]
        reason = f"Accessed sensitive path: {path}"

        # Avoid duplicate flagging for same reason roughly
        if not SuspiciousIP.objects.filter(
            ip_address=ip, reason__contains=path
        ).exists():
            SuspiciousIP.objects.create(ip_address=ip, reason=reason)
