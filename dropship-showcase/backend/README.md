# Dropship — Django Backend

Django + PostgreSQL REST API backend for the G.O.L.D Dropship Showcase.

## Quick Start

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 14+

### 2. Install dependencies

```bash
cd dropship-showcase/backend
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your actual values
```

### 4. Create database

```bash
psql -U postgres -c "CREATE DATABASE dropship;"
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
# Development
python manage.py runserver 8000

# Production (with gunicorn)
gunicorn dropship_backend.wsgi:application --bind 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/api/`.
Django Admin panel at `http://localhost:8000/admin/`.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key (required in production) | insecure default |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Full PostgreSQL URL (overrides individual DB vars) | — |
| `DB_NAME` | Database name | `dropship` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | — |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `JWT_LIFETIME_DAYS` | JWT access token lifetime in days | `7` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:5173` |

## API Endpoints

### Auth (`/api/auth/`)
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/signup/` | — | Register a new user |
| POST | `/signin/` | — | Sign in, returns JWT |
| GET | `/me/` | ✓ Bearer | Get current user |
| PATCH | `/me/update/` | ✓ Bearer | Update profile |
| POST | `/me/delete/` | ✓ Bearer | Delete account |

### Cart (`/api/cart/`)
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/` | ✓ | Get cart items |
| POST | `/` | ✓ | Add / upsert item |
| DELETE | `/` | ✓ | Clear cart |
| PUT | `/<product_id>/` | ✓ | Update quantity |
| DELETE | `/<product_id>/` | ✓ | Remove item |

### Wishlist (`/api/wishlist/`)
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/` | ✓ | Get wishlist product IDs |
| POST | `/toggle/` | ✓ | Toggle a product |
| POST | `/sync/` | ✓ | Sync local wishlist |

### Orders (`/api/orders/`)
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/` | ✓ | List user's orders |
| POST | `/` | ✓ | Place a new order |
| GET | `/<order_number>/` | ✓ | Order detail |

### Health
| Method | Path | Description |
|---|---|---|
| GET | `/api/health/` | Service health check |
