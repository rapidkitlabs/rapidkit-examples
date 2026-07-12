# SaaS Starter Workspace

A Workspai-managed multi-service SaaS example with FastAPI, NestJS, and
webhook processing.

**Related Articles:**
- Medium: [Building Production SaaS Architecture: Deep Dive into Multi-Service Implementation](https://rapidkit.medium.com/building-production-saas-architecture-deep-dive-into-multi-service-implementation-8a838f36e4ad)
- Dev.to: [Build Production SaaS: Code Walkthrough (FastAPI + NestJS + Webhooks)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-4c7c)
- Source repository: https://github.com/rapidkitlabs/rapidkit-examples/tree/main/saas-starter-workspace

**Projects in this workspace:**
- [saas-api](saas-api/README.md) - Product API with auth, subscriptions, teams (FastAPI + DDD)
- [saas-admin](saas-admin/README.md) - Admin operations & user management (FastAPI + DDD)
- [saas-nest](saas-nest/README.md) - Polyglot microservice for framework parity (NestJS)
- [saas-webhooks](saas-webhooks/README.md) - Stripe-style webhook processing with replay (FastAPI)

---

## Start after clone or download

First restore the three Python projects' generated Core module payloads from
the repository root, then enter `saas-starter-workspace`:

```bash
npm run hydrate:core -- \
  --workspace saas-starter-workspace \
  --project saas-api \
  --project saas-admin \
  --project saas-webhooks
cd saas-starter-workspace
npx workspai workspace sync
npx workspai workspace contract inspect
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
npx workspai doctor workspace --json
```

The first sync registers this workspace on the current machine and discovers
all four services. Do not import or adopt the workspace itself; its portable
markers already identify it.

To add another service, use import to copy it into this workspace or adopt to
leave it at its existing path:

```bash
npx workspai import ../existing-service --workspace . --json
npx workspai adopt ../external-service --workspace . --dry-run --json
npx workspai adopt ../external-service --workspace . --json
npx workspai workspace sync
```

Complete baseline, diff, impact, verify, agent context, agent-sync, explain, and
CI workflow: [Workspace onboarding](../WORKSPACE_ONBOARDING.md).

---

## ⚡ Quick Start

### 1. Clone & Setup Workspace

```bash
# Clone the examples repository
git clone https://github.com/rapidkitlabs/rapidkit-examples.git
cd rapidkit-examples
npm run hydrate:core -- \
  --workspace saas-starter-workspace \
  --project saas-api \
  --project saas-admin \
  --project saas-webhooks
cd saas-starter-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
```

### 2. Validate Workspace Health

```bash
# Check all 4 projects are detected
npx workspai doctor workspace
```

**Illustrative output shape:**
```
✓ Workspace: saas-starter-workspace
✓ Projects: 4/4 detected
  - saas-api (FastAPI, 6 modules)
  - saas-admin (FastAPI, 4 modules)
  - saas-nest (NestJS, 5 modules)
  - saas-webhooks (FastAPI, 3 modules)
✓ Contract: passed
```

Exact health findings depend on the current machine, installed runtimes, and
freshness of generated evidence. Treat the structured doctor verdict as the
authority.

### 3. Launch All Services

**Terminal 1 — Product API (port 8000):**
```bash
cd saas-api
cp .env.example .env
npx workspai init
npx workspai dev
```

**Terminal 2 — Admin API (port 8001):**
```bash
cd saas-admin
cp .env.example .env
npx workspai init
npx workspai dev --port 8001
```

**Terminal 3 — NestJS Service (port 8002):**
```bash
cd saas-nest
cp .env.example .env
npx workspai init
npx workspai dev --port 8002
```

**Terminal 4 — Webhook Processor (port 8003):**
```bash
cd saas-webhooks
cp .env.example .env
npx workspai init
npx workspai dev --port 8003
```

**Services running at:**
- Product API: http://localhost:8000 ([docs](http://localhost:8000/docs))
- Admin API: http://localhost:8001 ([docs](http://localhost:8001/docs))
- NestJS API: http://localhost:8002 ([docs](http://localhost:8002/docs))
- Webhooks: http://localhost:8003 ([docs](http://localhost:8003/docs))

---

## 🎯 What's Included

### Architecture Pattern

**Service-separated SaaS backend:**
- **Product API** handles user-facing operations
- **Admin API** isolates internal tooling
- **NestJS Service** demonstrates polyglot architecture
- **Webhook Processor** dedicated billing event handler

**Why this pattern:**
- Webhook crashes don't kill user signups
- Admin operations isolated from customer traffic
- Independent scaling and deployment
- Framework flexibility (FastAPI + NestJS)

### saas-api (Product API)

Production-pattern FastAPI with:
- ✅ JWT Authentication + Session Cookies (dual auth)
- ✅ User registration & login
- ✅ Subscription plans & checkout flows
- ✅ Team/organization management
- ✅ OAuth integration scaffolding
- ✅ Rate limiting
- ✅ DDD architecture (domain/application/infrastructure)

**Modules installed:**
- `auth_core` - PBKDF2 password hashing (100K iterations)
- `auth_session` - Server-side session management
- `auth_oauth` - OAuth provider integration
- `users_core` - User management service
- `users_profiles` - User profile service
- `rate_limiting` - Request rate limiting

### saas-admin (Admin Operations)

Internal admin API with:
- ✅ User impersonation capabilities
- ✅ Admin dashboard endpoints
- ✅ Audit trail foundations
- ✅ Support team tooling
- ✅ Same auth modules as product API
- ✅ DDD architecture

**Modules installed:**
- `auth_core`
- `auth_session`
- `users_core`
- `settings`

### saas-nest (Framework Parity)

NestJS service demonstrating:
- ✅ TypeScript + NestJS patterns
- ✅ Shared authentication flow with FastAPI
- ✅ Module-based architecture
- ✅ Health check endpoints
- ✅ Swagger/OpenAPI documentation

**Modules installed:**
- `auth-core` (NestJS)
- `users-core` (NestJS)
- `settings` (NestJS)

### saas-webhooks (Billing Events)

Dedicated webhook processor with:
- ✅ Stripe signature verification (HMAC-SHA256)
- ✅ Event log persistence
- ✅ **Replay capability** (critical for billing corrections)
- ✅ Background task processing
- ✅ Idempotency checks
- ✅ Retry logic with failure tracking

**Key features:**
- Send event → Verify signature → Log → Process async
- Replay failed events without calling Stripe
- Audit trail for all billing events

---

## 📁 Workspace Structure

```
saas-starter-workspace/
├── README.md              # This file
├── pyproject.toml         # Workspace dependencies
├── poetry.toml           # Poetry config
├── .venv/                # Shared virtual environment
├── saas-api/             # Product API (FastAPI + DDD)
│   ├── src/
│   │   ├── main.py       # Entry point with injection markers
│   │   ├── app/          # DDD layers
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   ├── infrastructure/
│   │   │   └── presentation/
│   │   ├── routing/      # Business logic routers
│   │   │   └── saas.py   # Auth, subscriptions, teams (485 lines)
│   │   └── modules/      # RapidKit modules
│   ├── tests/
│   ├── docker-compose.yml
│   └── Makefile
├── saas-admin/           # Admin API (FastAPI + DDD)
│   ├── src/
│   │   ├── main.py
│   │   ├── app/          # Same DDD structure
│   │   └── routing/
│   └── tests/
├── saas-nest/            # NestJS service
│   ├── src/
│   │   ├── main.ts
│   │   ├── app.module.ts
│   │   ├── auth/         # Auth controllers & services
│   │   └── modules/      # RapidKit NestJS modules
│   ├── test/
│   └── package.json
└── saas-webhooks/        # Webhook processor
    ├── src/
    │   ├── main.py
    │   └── routing/
    │       └── webhooks.py  # Webhook logic (210 lines)
    └── tests/
```

---

## 🚀 Development Workflow

### Test Complete User Flow

```python
# test_saas_flow.py
import requests

BASE = 'http://127.0.0.1:8000/api'

# Register user
r = requests.post(f'{BASE}/auth/register', json={
    'email': 'user@example.com',
    'password': 'SecurePass123!',
    'full_name': 'Test User'
})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Get profile
me = requests.get(f'{BASE}/auth/me', headers=headers)
print(f"User: {me.json()}")

# List subscription plans
plans = requests.get(f'{BASE}/subscriptions/plans')
print(f"Plans: {plans.json()}")

# Create team
team = requests.post(f'{BASE}/teams', 
    json={'name': 'Engineering'},
    headers=headers
)
print(f"Team: {team.json()}")
```

### Test Webhook Processing

```bash
# Send Stripe-style webhook
curl -X POST http://127.0.0.1:8003/api/webhooks/stripe \
  -H 'Content-Type: application/json' \
  -d '{
    "id": "evt_test_123",
    "type": "customer.subscription.updated",
    "data": {"subscription_id": "sub_abc", "status": "active"}
  }'

# View webhook logs
curl http://127.0.0.1:8003/api/webhooks/logs | jq

# Replay event (critical for billing corrections)
curl -X POST http://127.0.0.1:8003/api/webhooks/replay/evt_test_123
```

### Run Tests

```bash
# Test individual services
cd saas-api
npx workspai test
cd ..

cd saas-admin
npx workspai test
cd ..

cd saas-nest
npx workspai test
cd ..

cd saas-webhooks
npx workspai test
cd ..

# Or test all services
for svc in saas-api saas-admin saas-nest saas-webhooks; do
  echo "Testing $svc..."
  cd "$svc"
  npx workspai test
  cd ..
done
```

### Add More Modules

```bash
cd saas-api

# Add database
npx workspai add module db_postgres

# Add Redis caching
npx workspai add module redis

# Add email notifications
npx workspai add module email
```

---

## 🔐 Environment Configuration

### Generate Secrets

```bash
# Auth secrets
export RAPIDKIT_AUTH_CORE_PEPPER="$(openssl rand -base64 48)"
export RAPIDKIT_SESSION_SECRET="$(openssl rand -base64 32)"

# Stripe webhook secret (get from Stripe Dashboard)
export STRIPE_WEBHOOK_SECRET="whsec_your_actual_secret"
```

### Configure Services

**saas-api/.env:**
```bash
RAPIDKIT_AUTH_CORE_PEPPER=your_pepper_here
RAPIDKIT_SESSION_SECRET=your_session_secret
RAPIDKIT_SESSION_COOKIE_NAME=saas_session
RAPIDKIT_SESSION_COOKIE_SECURE=false  # true in production
```

**saas-webhooks/.env:**
```bash
STRIPE_WEBHOOK_SECRET=whsec_test_local
WEBHOOKS_MAX_RETRIES=3
WEBHOOKS_NOTIFY_EMAIL=billing@example.com
```

---

## 🏗️ Production Hardening

Before deploying:

**1. Replace In-Memory Storage:**
```python
# Current (demo):
_EVENTS: dict[str, WebhookLogEntry] = {}

# Production:
# Add db_postgres module and persist to PostgreSQL
```

**2. Add Infrastructure:**
```bash
# PostgreSQL for persistence
docker-compose up -d postgres

# Redis for sessions
docker-compose up -d redis
```

**3. Security:**
- [ ] Enable Stripe signature verification
- [ ] Rotate JWT secrets per environment
- [ ] Configure CORS for production domains
- [ ] Add rate limiting on public endpoints

**4. Observability:**
- [ ] Add structured logging with correlation IDs
- [ ] Integrate APM (Sentry, DataDog)
- [ ] Set up webhook event retention policies
- [ ] Configure alerting on failed payment events

---

## 📚 Learn More

**Implementation guides:**
- [Architecture Deep Dive (Medium)](https://medium.com/@rapidkit/building-production-saas-architecture-13)
- [Code Walkthrough (Dev.to)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-13)

**Key patterns explained:**
- Dual authentication (JWT + session cookies)
- DDD structure with module injection
- Webhook signature verification
- Event replay for billing corrections
- Service separation patterns

**RapidKit documentation:**
- [CLI Reference](https://www.workspai.dev/docs/cli)
- [Modules Catalog](https://www.workspai.dev/docs/cli/modules)
- [Deployment Guide](https://www.workspai.dev/docs/guides)

---

## 🛠️ Troubleshooting

**"Module not found" errors:**
```bash
cd <project>
npx workspai init
```

**Services won't start:**
```bash
# Check health
npx workspai doctor workspace

# Verify ports are available
lsof -i :8000-8003
```

**Webhook signature verification fails:**
```bash
# Set test secret for local development
export STRIPE_WEBHOOK_SECRET="whsec_test"

# Or disable verification (local only)
# Remove stripe-signature header from curl
```

**Need help?**
- Documentation: https://getrapidkit.com/docs
- GitHub Issues: https://github.com/rapidkitlabs/rapidkit-core/issues
- Community: https://discord.gg/rapidkit
