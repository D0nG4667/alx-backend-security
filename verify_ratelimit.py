import os
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_security.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User


def test_rate_limit():
    print("Starting Rate Limit Verification...", flush=True)
    client = Client()

    # Test Anonymous User (Limit: 5/m)
    print("\n[Test] Anonymous User (Limit: 5/m)", flush=True)
    for i in range(1, 8):
        response = client.get("/login/")
        print(f"Request {i}: Status {response.status_code}", flush=True)
        if response.status_code == 403:
            print("SUCCESS: Anonymous request blocked correctly.", flush=True)
            break
        time.sleep(0.1)
    else:
        print(
            "FAILURE: Anonymous requests were not blocked after 5 attempts.", flush=True
        )

    # Test Authenticated User (Limit: 10/m) (Optional: verify helper actually returns '10/m' logic)
    # Creating a user
    username = "testuser_ratelimit"
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password="password")

    user = User.objects.get(username=username)
    client.force_login(user)

    # Note: Rate limits might be per IP, so if we use same IP (client default), we might already be blocked if key='ip'.
    # If key='ip', both users share the limit bucket if coming from same IP.
    # The requirement said "10 requests/minute (authenticated), 5 (anonymous)".
    # If the key is 'ip', then authenticated status just changes the limit *number* for that IP.
    # Since we likely just exhausted the IP bucket with anonymous requests (count > 5),
    # we might need to wait or mock IP for second test.
    # Client(REMOTE_ADDR='...') can simulate different IP.

    print("\n[Test] Authenticated User (Limit: 10/m) from DIFFERENT IP", flush=True)
    client_auth = Client(REMOTE_ADDR="127.0.0.2")  # Different IP
    client_auth.force_login(user)

    for i in range(1, 13):
        response = client_auth.get("/login/")
        print(f"Auth Request {i}: Status {response.status_code}", flush=True)
        if response.status_code == 403:
            if i > 10:
                print(
                    "SUCCESS: Authenticated request blocked after 10 attempts.",
                    flush=True,
                )
            else:
                print(
                    f"FAILURE: Authenticated request blocked too early (at {i}).",
                    flush=True,
                )
            break
        time.sleep(0.1)
    else:
        print(
            "FAILURE: Authenticated requests were not blocked after 10 attempts.",
            flush=True,
        )


if __name__ == "__main__":
    test_rate_limit()
