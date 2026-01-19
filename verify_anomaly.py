import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_security.settings")
django.setup()

from ip_tracking.models import RequestLog, SuspiciousIP
from ip_tracking.tasks import detect_anomalies


def test_anomaly_detection():
    print("Starting Anomaly Detection Verification...", flush=True)

    # 1. Setup Data
    RequestLog.objects.all().delete()
    SuspiciousIP.objects.all().delete()

    now = timezone.now()

    # Case A: High Traffic IP (105 requests)
    ip_high = "192.168.1.100"
    logs = [
        RequestLog(ip_address=ip_high, path="/home", timestamp=now) for _ in range(105)
    ]
    RequestLog.objects.bulk_create(logs)
    print(f"Seeded 105 logs for {ip_high}", flush=True)

    # Case B: Sensitive Path IP
    ip_sensitive = "192.168.1.101"
    RequestLog.objects.create(ip_address=ip_sensitive, path="/admin/", timestamp=now)
    print(f"Seeded sensitive path log for {ip_sensitive}", flush=True)

    # Case C: Normal IP
    ip_normal = "192.168.1.102"
    RequestLog.objects.create(ip_address=ip_normal, path="/home", timestamp=now)
    print(f"Seeded normal log for {ip_normal}", flush=True)

    # 2. Run Task
    print("Running detect_anomalies task...", flush=True)
    detect_anomalies()

    # 3. Verify Results
    suspicious = SuspiciousIP.objects.all()
    print(f"Total Suspicious IPs found: {suspicious.count()}", flush=True)
    for s in suspicious:
        print(f" - {s.ip_address}: {s.reason}", flush=True)

    # Assertions
    if suspicious.filter(ip_address=ip_high).exists():
        print("SUCCESS: High traffic IP was flagged.", flush=True)
    else:
        print("FAILURE: High traffic IP was NOT flagged.", flush=True)

    if suspicious.filter(ip_address=ip_sensitive).exists():
        print("SUCCESS: Sensitive path IP was flagged.", flush=True)
    else:
        print("FAILURE: Sensitive path IP was NOT flagged.", flush=True)

    if not suspicious.filter(ip_address=ip_normal).exists():
        print("SUCCESS: Normal IP was NOT flagged.", flush=True)
    else:
        print("FAILURE: Normal IP WAS flagged incorrectly.", flush=True)


if __name__ == "__main__":
    test_anomaly_detection()
