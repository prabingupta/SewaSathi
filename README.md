# SewaSaathi 🛠️

**SewaSaathi** is an AI-powered service marketplace connecting customers in Nepal with verified local service providers — electricians, plumbers, painters, tutors, and more.It implements a complete booking marketplace: registration and verification, service listings, real-time chat, reviews, notifications, and an admin analytics dashboard.

> स + Saathi = "Service Companion" — सS is the brand mark used throughout the UI.

---

## Live Features

| Module | What it does |
|---|---|
| **User Management** | Custom user model with three roles — Customer, Service Provider, Admin |
| **Service Provider Management** | Profile creation, document upload, admin verification workflow |
| **Service Management** | Admin-managed categories + provider-defined services with individual pricing |
| **Service Booking** | Full lifecycle: Pending → Accepted/Rejected → In Progress → Completed/Cancelled |
| **AI Recommendation** | Transparent weighted scoring (rating, review volume, experience, price) ranks Browse results |
| **Smart Search** | Search by name, skill, or area; filter by category |
| **Real-Time Chat** | Booking-scoped live chat via Django Channels + Redis (WebSockets) |
| **Payments** | eSewa ePay v2 integration — signed payment requests, HMAC-SHA256 verified callbacks |
| **Reviews & Ratings** | One review per completed booking; live average rating shown on listings |
| **GPS / Location** | Click-to-pin provider location using free OpenStreetMap + Leaflet (no API key needed) |
| **Notifications** | In-app bell with unread badge, dropdown preview, full notification history |
| **Admin Dashboard** | Chart.js analytics — bookings by status, top categories, revenue estimate, recent signups |

---

## Tech Stack

- **Backend:** Django 6.0 (Python 3.14)
- **Database:** SQLite (development) — swappable to PostgreSQL via `DATABASES` in `settings.py`
- **Real-time:** Django Channels 4 + Daphne (ASGI) + Redis (channel layer)
- **Frontend:** Server-rendered Django templates, Bootstrap 5 grid + fully custom CSS design system, vanilla JS
- **Maps:** Leaflet.js + OpenStreetMap (free, no API key)
- **Charts:** Chart.js
- **Payments:** eSewa ePay v2 (HMAC-SHA256 signed requests)

---

## Project Structure
sewasaathi/

├── accounts/         # Custom User model, auth (register/login/logout)

├── providers/         # ServiceProvider profiles, verification, location, browse/search

├── services/          # ServiceCategory + provider-defined Service listings

├── bookings/          # Booking model + full status workflow

├── reviews/           # Review model, one per completed booking

├── notifications/      # In-app Notification model + bell UI

├── chat/              # Real-time chat (Channels consumer, routing, models)

├── payments/          # eSewa integration (signature gen/verify, views)

├── dashboard/          # Staff-only analytics dashboard

├── core/               # Homepage

├── templates/          # All HTML templates, organized by app

├── static/css/         # Custom design system (style.css) + admin theme override

└── sewasaathi/          # Project settings, URLs, ASGI/WSGI entrypoints

Each app follows the same internal shape: `models.py`, `views.py`, `forms.py` (where relevant), `urls.py`, `admin.py`.

---

## Getting Started

### Prerequisites

- Python 3.11+ (developed on 3.14)
- [Redis](https://redis.io/) (required for real-time chat)
  - macOS: `brew install redis && brew services start redis`
  - Linux: `sudo apt install redis-server`

### Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/prabingupta/SewaSathi.git
cd SewaSathi

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Start Redis (separate terminal, if not running as a service)
redis-server

# 7. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site, or `http://127.0.0.1:8000/admin/` for the admin panel.

> **Note:** The server runs under Daphne (ASGI), not the default Django dev server — this is required for the real-time chat WebSocket support. You'll see `Starting ASGI/Daphne version ...` in the terminal output, which confirms it's working correctly.

### First-time data setup

After creating a superuser, log into `/admin/` and add a few **Service Categories** (e.g. Electrician, Plumber, Painter) under the **Services** section — the platform has no providers or services until categories exist for them to register under.

---

## Architecture Notes

A few deliberate design decisions, useful context for reviewing the code:

- **Custom `User` model from day one** (`accounts.User`, set via `AUTH_USER_MODEL`). Switching to a custom user model after the first migration is notoriously painful in Django, so this was set up before any other app existed.
- **Role-based access control is enforced at the view layer**, not just hidden in the UI — every protected view independently re-checks `request.user.role` or ownership (e.g. a provider can only manage their own bookings, even if they guess another booking's URL).
- **`PROTECT` vs `CASCADE` vs `SET_NULL`** are chosen deliberately per relationship: a `ServiceCategory` can't be deleted while providers reference it (`PROTECT`); a `Booking`'s `service` reference is nulled, not deleted, if a provider removes that service listing later (`SET_NULL`), preserving booking history.
- **The AI Recommendation Engine is a transparent weighted scoring formula** (rating 40%, review-volume confidence 20%, experience 20%, price 20%), not a trained ML model — chosen deliberately because the platform doesn't yet have enough booking volume for a trained model to learn meaningful patterns from. This is documented in `providers/models.py` on `ServiceProvider.recommendation_score()`.
- **Real-time chat uses Redis as the channel layer**, not the simpler in-memory option, specifically so it works correctly across multiple server processes in a real deployment (the in-memory layer only works within a single process).
- **Signature verification in the payment flow uses `hmac.compare_digest()`**, not a plain string comparison, to avoid timing-attack vulnerabilities when validating eSewa's callback signature.

---

## Known Limitations

- **eSewa payment testing**: the integration (signed request generation, HMAC-SHA256 verification, callback handling) is fully implemented and was confirmed to correctly reach eSewa's real UAT gateway with the right merchant code and amount. End-to-end testing of a completed transaction was blocked by instability in eSewa's shared public sandbox environment (login failures across multiple sets of their own documented test credentials, and a failed test registration attempt) — this is an external infrastructure issue, not a defect in the integration code.
- **Channel layer (Redis)** is configured for a single Redis instance, appropriate for development and demonstration. A production deployment serving real traffic would typically run Redis as a managed service (e.g. a hosting provider's Redis add-on).
- **AI Recommendation Engine** is a heuristic scoring formula rather than a trained model — appropriate given current data volume, with a clear upgrade path to a trained model (e.g. collaborative filtering) once sufficient booking/review history exists.

---

## Future Enhancements

- SMS notifications (currently in-app only)
- Trained recommendation model once sufficient usage data exists
- Production deployment with PostgreSQL + managed Redis
- Khalti as a secondary payment option

---

## Author

Prabin Kumar Gupta.
