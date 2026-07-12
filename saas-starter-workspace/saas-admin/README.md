# saas-admin

Admin operations API for internal tools, user management, and support workflows. Domain-driven FastAPI service generated with [RapidKit](https://github.com/rapidkitlabs/rapidkit-core).

**Related:** Part of [saas-starter-workspace](../README.md) - Production SaaS architecture with 4 microservices.

---

## ⚡ Quick Start

```bash
# Bootstrap dependencies
npx workspai init

# Copy env templates and install hooks/tooling
./bootstrap.sh

# Start development server on port 8001
npx workspai dev --port 8001
# Or: make dev

# Run tests
npx workspai test

# Type-check and lint
make typecheck
make lint
```

**API running at:** http://localhost:8001

**Endpoints:**
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health
- Module Health: http://localhost:8001/api/health/module/*

> **Tip:** Run on port 8001 to avoid conflicts with `saas-api` (port 8000).

---

## 🎯 Implemented Features

### Admin Operations

- **User Management:**
  - List all users with filtering
  - Disable a user account
  - Record the action in an in-memory audit log

- **Internal Dashboards:**
  - User status metrics
  - Subscription inventory
  - Monthly recurring revenue summary
  - Authenticated admin health

### Security

- **Admin Authentication:**
  - Dedicated admin login
  - Bearer tokens carrying an explicit admin role
  - Admin role verification on protected routes

- **Access Control:**
  - Admin-only endpoints
  - Audit recording for user disable operations

### Extension Ideas (Not Implemented)

- User impersonation
- Support ticket integration
- Persistent audit storage
- Fine-grained permission policies

---

## 📦 Installed Modules

### Core Modules

**`auth_core`** - Authentication primitive
- PBKDF2 password hashing (100K iterations)
- Token signing and verification
- Health: `/api/health/module/auth-core`

**`auth_session`** - Session management
- Cookie-based sessions
- Server-side validation
- Health: `/api/health/module/session`

**`users_core`** - User service
- User CRUD operations
- Email uniqueness
- Health: `/api/health/module/users-core`

**`settings`** - Configuration management
- Multi-source config (env, yaml, custom)
- Hot-reload in development
- Health: `/api/health/module/settings`

---

## 📁 Project Structure

```
saas-admin/
├── src/
│   ├── main.py              # Application entrypoint
│   ├── app/
│   │   ├── main.py          # FastAPI factory
│   │   ├── application/     # Use cases
│   │   ├── domain/          # Business entities
│   │   ├── infrastructure/  # External adapters
│   │   └── presentation/    # API layer
│   ├── routing/
│   │   ├── __init__.py      # Router assembly
│   │   ├── saas_admin.py    # Implemented admin routes
│   │   ├── health.py        # Health checks
│   │   └── notes.py         # Example feature
│   ├── modules/
│   │   └── free/
│   │       ├── auth/
│   │       ├── users/
│   │       └── settings/
│   └── health/
├── tests/
│   ├── test_admin_ops.py
│   └── conftest.py
├── config/
├── .env.example
├── docker-compose.yml
└── Makefile
```

### DDD Architecture

Same clean architecture as `saas-api`:
- **Domain** – Business rules
- **Application** – Use case orchestration
- **Infrastructure** – External services
- **Presentation** – HTTP API layer

---

## 🔧 Example Usage

### Admin User Management

```python
import requests

BASE = 'http://localhost:8001/api'

# Admin login
r = requests.post(f'{BASE}/admin/auth/login', json={
    'email': 'admin@example.com',
    'password': 'AdminPass123!'
})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# List all users
users = requests.get(f'{BASE}/admin/users', headers=headers)
print(users.json())

# Disable a user and record an audit event
result = requests.put(f'{BASE}/admin/users/usr_123/ban', headers=headers)
print(result.json())

# Read subscription and revenue summaries
subscriptions = requests.get(f'{BASE}/admin/subscriptions', headers=headers)
revenue = requests.get(f'{BASE}/admin/metrics/revenue', headers=headers)
```

### Health Monitoring

```python
# Check admin API health
health = requests.get(f'{BASE}/health')
print(health.json())

# Check module health
auth_health = requests.get(f'{BASE}/api/health/module/auth-core')
print(auth_health.json())
```

---

## 🚀 Add More Modules

```bash

# Add database for audit logs
npx workspai add module db_postgres

# Add Redis for session storage
npx workspai add module redis

# Add email for admin notifications
npx workspai add module email

# Add monitoring
npx workspai add module observability.core
```

---

## 🔐 Environment Configuration

**`.env` template:**
```bash
# Auth Configuration (same as saas-api)
RAPIDKIT_AUTH_CORE_PEPPER="your_pepper_here"
RAPIDKIT_SESSION_SECRET="your_session_secret"

# Admin-specific
ADMIN_AUTH_REQUIRED=true
ADMIN_ALLOWED_EMAILS="admin@example.com,support@example.com"
```

**Generate secrets:**
```bash
openssl rand -base64 48  # Auth pepper
openssl rand -base64 32  # Session secret
```

---

## 🧪 Testing

```bash
# Run all tests
npx workspai test

# Test admin operations
pytest tests/test_admin_ops.py -v

# With coverage
pytest --cov=src tests/
```

---

## 🏗️ Production Deployment

### Isolation Strategy

**Why separate admin API?**
- Customer traffic doesn't affect admin operations
- Different authentication/authorization rules
- Independent scaling
- Enhanced security (internal network only)

### Docker

```bash
docker build -t saas-admin:latest .
docker-compose up -d
```

### Network Security

**Production best practices:**
- Deploy admin API on internal network
- Require VPN/bastion for access
- Use different JWT secrets than product API
- Enable audit logging for all operations

---

## 📚 Learn More

**Architecture guides:**
- [Workspace Overview](../README.md)
- [Building Production SaaS Architecture (Medium)](https://medium.com/@rapidkit/building-production-saas-architecture-13)

**Related services:**
- [saas-api](../saas-api/README.md) - Product API
- [saas-webhooks](../saas-webhooks/README.md) - Webhook processor
- [saas-nest](../saas-nest/README.md) - NestJS service

**RapidKit documentation:**
- [Modules Catalog](https://www.workspai.dev/docs/cli/modules)
- [CLI Reference](https://www.workspai.dev/docs/cli)

---

## 🛠️ Troubleshooting

**Port conflict with saas-api:**
```bash
# Always run admin API on port 8001
npx workspai dev --port 8001
```

**Authentication issues:**
```bash
# Use same secrets as saas-api
# Check .env matches saas-api/.env
```

**Need help?**
- Documentation: https://getrapidkit.com/docs
- GitHub Issues: https://github.com/rapidkitlabs/rapidkit-core/issues
