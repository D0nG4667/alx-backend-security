import os
import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_security.settings")
django.setup()

from ip_tracking.models import RequestLog  # noqa: E402


def test_logging():
    print("Starting logging test...", flush=True)
    # Clean up previous logs for clarity
    RequestLog.objects.all().delete()
    print("Cleaned up existing logs.", flush=True)

    client = Client()
    # Simulate a request
    # By default, Client sets 127.0.0.1 as REMOTE_ADDR
    try:
        response = client.get("/")
        print(f"Request made, status code: {response.status_code}", flush=True)
    except Exception as e:
        print(f"Request failed: {e}", flush=True)

    # Check if logged
    logs = RequestLog.objects.all()
    count = logs.count()
    print(f"Total logs: {count}", flush=True)

    for log in logs:
        print(
            f"IP: {log.ip_address}, Path: {log.path}, Time: {log.timestamp}", flush=True
        )


if __name__ == "__main__":
    test_logging()
