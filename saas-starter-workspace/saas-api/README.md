# saas-api

Product API for SaaS applications with authentication, subscriptions, and team management. Domain-driven FastAPI service generated with [RapidKit](https://github.com/rapidkitlabs/rapidkit-core).

**Related:** Part of [saas-starter-workspace](../README.md) - Production SaaS architecture with 4 microservices.

---

## ⚡ Quick Start

```bash
# Load the project-aware RapidKit CLI
source .rapidkit/activate

# Bootstrap dependencies (creates .venv + installs Poetry deps)
rapidkit init

# Copy env templates and install hooks/tooling
./bootstrap.sh

# Start development server
rapidkit dev
# Or: make dev

# Run tests
rapidkit test
# Or: make test

# Type-check and lint
make typecheck
make lint

# Run supply-chain and dependency audits
make audit
```

**API running at:** http://localhost:8000

**Endpoints:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Module Health: http://localhost:8000/api/health/module/*

> **Tip:** Re-source `.rapidkit/activate` when opening a new shell to keep the project-local `rapidkit` launcher on your PATH.

> **Tip:** Re-run `rapidkit init` when dependencies change. Use `SKIP_INIT=1 make install` if you only need to refresh tooling/hooks.

---

## 🎯 Features

### Authentication & User Management

- **Dual Authentication:**
  - JWT Bearer tokens (stateless, mobile/API clients)
  - Session cookies (server-side, web browsers)
  - Single resolution function handles both strategies

- **User Operations:**
  - `POST /api/auth/register` - Register with email/password
  - `POST /api/auth/login` - Login and get tokens
  - `GET /api/auth/me` - Get current user profile
  - `GET /api/users/profile` - Get detailed profile
  - `PUT /api/users/profile` - Update profile fields

### Subscription Management

- **Subscription Plans:**
  - `GET /api/subscriptions/plans` - List available plans
  - `POST /api/subscriptions/checkout` - Initiate checkout flow
  - Starter ($19/mo), Growth ($79/mo), Scale ($249/mo)

### Team Management

- **Team Operations:**
  - `POST /api/teams` - Create team/organization
  - `GET /api/teams` - List user's teams
  - Multi-tenant foundation ready

### Security

- **Password Hashing:** PBKDF2 with 100,000 iterations
- **Rate Limiting:** Configurable per-endpoint limits
- **Session Management:** Server-side validation with Redis-ready infrastructure
- **OAuth Ready:** Scaffolding for Google, GitHub, etc.

---

## 📦 Installed Modules

### Core Modules

**`auth_core`** - Cryptographic authentication primitive
- PBKDF2 password hashing (100K iterations, salted)
- HMAC token signing with pepper
- FastAPI dependencies: `hash_password`, `verify_password`, `issue_token`
- Health: `/api/health/module/auth-core`

**`auth_session`** - Server-side session management
- Cookie-based session tokens
- Session creation and verification
- Configurable cookie settings (secure, httponly, samesite)
- Health: `/api/health/module/session`

**`auth_oauth`** - OAuth provider integration
- Google, GitHub, Microsoft scaffolding
- State verification
- Token exchange flows
- Health: `/api/health/module/oauth`

**`users_core`** - User management service
- User CRUD operations
- Email uniqueness enforcement
- Service layer with DTOs
- Health: `/api/health/module/users-core`

**`users_profiles`** - User profile management
- Profile CRUD with validation
- Timezone, biography, display name
- Profile service facade
- Health: `/api/health/module/users-profiles`

**`rate_limiting`** - Request rate limiting
- Per-user, per-IP, or per-endpoint limits
- Configurable rules and costs
- FastAPI dependency injection
- Health: `/api/health/module/rate-limit`

---

## 📁 Project Structure

```
saas-api/
├── src/
│   ├── main.py              # Application entrypoint with injection markers
│   ├── app/
│   │   ├── main.py          # FastAPI factory
│   │   ├── application/     # Use cases and service contracts
│   │   ├── domain/          # Aggregates, entities, value objects
│   │   ├── infrastructure/  # Adapters and repositories
│   │   ├── presentation/    # API routers and dependencies
│   │   └── shared/          # Cross-cutting primitives
│   ├── routing/
│   │   ├── __init__.py      # Router assembly
│   │   ├── saas.py          # Business logic (485 lines)
│   │   │                    # - Auth (register, login, me)
│   │   │                    # - Subscriptions (plans, checkout)
│   │   │                    # - Teams (create, list)
│   │   ├── health.py        # Health check routes
│   │   └── notes.py         # Example feature
│   ├── modules/
│   │   └── free/
│   │       ├── auth/
│   │       │   ├── core/    # auth_core module
│   │       │   ├── session/ # auth_session module
│   │       │   └── oauth/   # auth_oauth module
│   │       ├── users/
│   │       │   ├── users_core/
│   │       │   └── users_profiles/
│   │       └── security/
│   │           └── rate_limiting/
│   └── health/              # Canonical health routes
├── tests/
│   ├── test_auth.py
│   ├── test_subscriptions.py
│   └── test_teams.py
├── config/                  # Module configurations
├── .env.example             # Environment template
├── docker-compose.yml       # PostgreSQL, Redis setup
├── Dockerfile
├── Makefile
└── pyproject.toml
```

### DDD Layer Overview

- **Domain** – Pure business rules (`src/app/domain`)
- **Application** – Use cases and service orchestration (`src/app/application`)
- **Infrastructure** – Database adapters and external services (`src/app/infrastructure`)
- **Presentation** – FastAPI routers and HTTP layer (`src/app/presentation`)

**Module injection system:**
```python
# <<<inject:imports>>> - Modules add imports here
# <<<inject:startup>>> - Module startup hooks
# <<<inject:shutdown>>> - Module cleanup hooks
# <<<inject:routes>>> - Module routes mounted here
```

---

## 🔧 Example Usage

### Register and Login

```python
import requests

BASE = 'http://localhost:8000/api'

# Register user
r = requests.post(f'{BASE}/auth/register', json={
    'email': 'user@example.com',
    'password': 'SecurePass123!',
    'full_name': 'John Doe'
})
print(r.json())
# {
#   "user": {"id": "usr_123", "email": "user@example.com", ...},
#   "access_token": "eyJhbGc...",
#   "token_type": "bearer"
# }

# Use token
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

me = requests.get(f'{BASE}/auth/me', headers=headers)
print(me.json())
```

### Subscription Flow

```python
# List plans
plans = requests.get(f'{BASE}/subscriptions/plans')
print(plans.json())
# [
#   {"id": "starter", "name": "Starter", "price_monthly": 19, ...},
#   {"id": "growth", "name": "Growth", "price_monthly": 79, ...}
# ]

# Start checkout
checkout = requests.post(f'{BASE}/subscriptions/checkout',
    json={'plan_id': 'starter'},
    headers=headers
)
print(checkout.json())
```

### Team Management

```python
# Create team
team = requests.post(f'{BASE}/teams',
    json={'name': 'Engineering Team'},
    headers=headers
)
print(team.json())

# List teams
teams = requests.get(f'{BASE}/teams', headers=headers)
print(teams.json())
```

---

## 🚀 Add More Modules

```bash
source .rapidkit/activate

# Add database
rapidkit add module db_postgres

# Add Redis caching
rapidkit add module redis

# Add email notifications
rapidkit add module email

# Add monitoring
rapidkit add module observability.core
```

**After adding modules:**
1. Update `.env` with module configuration
2. Run `rapidkit init` to install dependencies
3. Restart dev server: `rapidkit dev`

---

## 🔐 Environment Configuration

**`.env` template:**
```bash
# Auth Configuration
RAPIDKIT_AUTH_CORE_PEPPER="your_pepper_here_base64_48_chars"
RAPIDKIT_AUTH_CORE_TOKEN_EXPIRY_MINUTES=60

# Session Configuration
RAPIDKIT_SESSION_SECRET="your_session_secret_here"
RAPIDKIT_SESSION_COOKIE_NAME="saas_session"
RAPIDKIT_SESSION_COOKIE_SECURE=false  # true in production
RAPIDKIT_SESSION_COOKIE_HTTPONLY=true
RAPIDKIT_SESSION_COOKIE_SAMESITE="lax"

# Rate Limiting
RAPIDKIT_RATE_LIMIT_DEFAULT="100/minute"

# OAuth (optional)
RAPIDKIT_OAUTH_GOOGLE_CLIENT_ID=""
RAPIDKIT_OAUTH_GOOGLE_CLIENT_SECRET=""
```

**Generate secrets:**
```bash
# Auth pepper (48 chars base64)
openssl rand -base64 48

# Session secret (32 chars base64)
openssl rand -base64 32
```

---

## 🧪 Testing

```bash
# Run all tests
rapidkit test

# With coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_auth.py -v

# Test with markers
pytest -m "auth" -v
```

**Test structure:**
- `tests/test_auth.py` - Authentication flow tests
- `tests/test_subscriptions.py` - Subscription endpoint tests
- `tests/test_teams.py` - Team management tests
- `tests/conftest.py` - Shared fixtures

---

## 🏗️ Production Deployment

### Docker

```bash
# Build image
docker build -t saas-api:latest .

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

Set these in production:
```bash
RAPIDKIT_AUTH_CORE_PEPPER=<strong-random-value>
RAPIDKIT_SESSION_SECRET=<strong-random-value>
RAPIDKIT_SESSION_COOKIE_SECURE=true
DATABASE_URL=postgresql://user:pass@postgres:5432/saas_db
REDIS_URL=redis://redis:6379/0
```

### Health Checks

Configure load balancer/orchestrator:
- **Liveness:** `GET /health` (200 = alive)
- **Readiness:** `GET /api/health/readyz` (200 = ready)
- **Module Health:** `GET /api/health/module/<module-name>`

---

## 📚 Learn More

**Architecture guides:**
- [Building Production SaaS Architecture (Medium)](https://medium.com/@rapidkit/building-production-saas-architecture-13)
- [Code Walkthrough (Dev.to)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-13)
- [Workspace Overview](../README.md)

**Implementation details:**
- Dual authentication pattern (JWT + sessions)
- DDD structure with module injection
- Service layer isolation
- PBKDF2 password hashing

**RapidKit documentation:**
- [Modules Catalog](https://getrapidkit.com/docs/modules)
- [CLI Reference](https://getrapidkit.com/docs/cli)
- [Deployment Guide](https://getrapidkit.com/docs/deployment)

---

## 🛠️ Troubleshooting

**Import errors after adding modules:**
```bash
rapidkit init
```

**Port already in use:**
```bash
# Run on different port
rapidkit dev --port 8080
```

**Module health check fails:**
```bash
# Check module configuration
curl http://localhost:8000/api/health/module/auth-core
```

**Need help?**
- Documentation: https://getrapidkit.com/docs
- GitHub Issues: https://github.com/rapidkitlabs/rapidkit-core/issues
- Community: https://discord.gg/rapidkit
