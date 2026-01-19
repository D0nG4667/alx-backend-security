# ALX Backend Security 🛡️

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Distributed_Task_Queue-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-In_Memory_Store-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-API_Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

**ALX Backend Security** is a robust Django-based security framework designed to track, analyze, and protect against suspicious IP activity. It features real-time blocking, geolocation tracking, rate limiting, and background anomaly detection using Celery.

---

## 🚀 Features

### 1. 🔍 IP Logging & Geolocation
- **Middleware-based logging**: Captures every request's IP, path, and timestamp.
- **Geolocation**: Automatically resolves IP addresses to Country and City using `django-ip-geolocation`.
- **Optimization**: Implements intelligent 24-hour caching to minimize external API calls and latency.

### 2. ⛔ Access Control (Blacklisting)
- **Real-time Blocking**: Middleware checks every request against a `BlockedIP` database.
- **Immediate Rejection**: Blocked IPs receive a `403 Forbidden` response instantly.
- **Management Command**: Easily block IPs via CLI: `python manage.py block_ip <ip_address>`.

### 3. 🚦 Rate Limiting
- **Throttling**: Protects sensitive endpoints (e.g., login) from abuse.
- **Dynamic Limits**:
  - **Authenticated Users**: 10 requests/minute.
  - **Anonymous Users**: 5 requests/minute.
- **Response**: Triggers `403 Forbidden` when limits are exceeded.

### 4. 🧠 Anomaly Detection (Celery)
- **Background Analysis**: Runs hourly tasks to analyze traffic patterns.
- **Automatic Flagging**:
  - **High Volume**: Flags IPs exceeding 100 requests/hour.
  - **Sensitive Access**: Flags IPs probing `/admin/` or `/login/` endpoints.
- **Reporting**: Stores incidents in the `SuspiciousIP` model with detailed reasons.

### 5. 📚 API Documentation
- **Swagger UI**: Interactive documentation available at `/swagger/`.
- **ReDoc**: Alternative documentation view at `/redoc/`.

---

## 🛠️ Tech Stack

- **Framework**: Django 6.0 (Python 3.12)
- **Task Queue**: Celery 5.x
- **Message Broker**: Redis
- **Database**: PostgreSQL (Production) / SQLite (Dev)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Deployment**: Render (Gunicorn + Whitenoise)

---

## 💻 Local Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/alx-backend-security.git
    cd alx-backend-security
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

4.  **Start Services**
    - **Django Server**:
      ```bash
      python manage.py runserver
      ```
    - **Celery Worker** (requires Redis running locally):
      ```bash
      celery -A alx_backend_security worker -l info
      ```

---

## ☁️ Deployment (Render)

This project is configured for **Render Blueprint** deployment.

1.  **Push to GitHub**.
2.  **Create Blueprint**: In Render, select "New Blueprint" and connect your repo.
3.  **Auto-Configuration**: Render will detect `render.yaml` and set up:
    - **Web Service** (Django App)
    - **Redis** (for Caching & Celery)
    - **PostgreSQL** (Database)

### 🔑 Credentials & Admin
For ephemeral deployments (SQLite/Free Tier):
- A default superuser is created automatically on deployment.
- **Username**: `admin`
- **Password**: `admin`

---

## 📝 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Elegant Dashboard Home |
| `GET` | `/swagger/` | Interactive API Docs |
| `GET` | `/login/` | Test Endpoint (Rate Limited) |
| `GET` | `/secure-data/` | Authenticated Test Endpoint |
| `GET` | `/admin/` | Admin Control Panel |

---

## 📄 License

This project is licensed under the MIT License.
