# Quickstart Workspace

A Workspai-managed RapidKit Core example with two production-style FastAPI
services.

**Related Articles:**
- Medium: [From Zero to Production FastAPI with RapidKit: Build a Real E-Commerce API](https://medium.com/@rapidkit/from-zero-to-production-fastapi-with-rapidkit-build-a-real-e-commerce-api-80390a34ffe3)
- Dev.to: [Build a Production-Ready FastAPI E-Commerce API with RapidKit (Step-by-Step)](https://dev.to/rapidkit/build-a-production-ready-fastapi-e-commerce-api-with-rapidkit-step-by-step-llm)
- Source repository: https://github.com/rapidkitlabs/rapidkit-examples/tree/main/quickstart-workspace

**Projects in this workspace:**
- [product-api](product-api/README.md) - Production-pattern FastAPI with auth, database, caching, and monitoring
- [ecommerce-api](ecommerce-api/README.md) - Production-style e-commerce backend with catalog/cart/checkout flow

---

## Start after clone or download

Run these commands from `quickstart-workspace`, the directory containing
`.workspai-workspace`:

```bash
npx workspai workspace sync
npx workspai workspace contract inspect
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
npx workspai doctor workspace --json
```

The first sync registers this workspace on the current machine and discovers
both existing projects. Do not import or adopt the workspace itself; its
portable markers already identify it. To add another project, use `import` when
it should be copied into this workspace or `adopt` when it must remain in place:

```bash
npx workspai import ../existing-api --workspace . --json
npx workspai adopt ../external-api --workspace . --dry-run --json
npx workspai adopt ../external-api --workspace . --json
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
  --workspace quickstart-workspace \
  --project product-api \
  --project ecommerce-api
cd quickstart-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
```

### 2. Start Infrastructure

```bash
# From workspace root
cd ecommerce-api
docker-compose up -d postgres redis
```

**Services started:**
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

### 3. Run the API

```bash
cd ecommerce-api
cp .env.example .env
npx workspai init
npx workspai dev -p 8001
```

**API running at:** http://localhost:8001

**Endpoints:**
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health
- Metrics: http://localhost:8001/metrics

---

## 🎯 What's Included

### product-api

Production-pattern FastAPI with:
- ✅ JWT Authentication (register, login, refresh)
- ✅ PostgreSQL with SQLAlchemy (async & sync)
- ✅ Redis caching with connection pooling
- ✅ CORS & Security Headers
- ✅ Structured logging with request tracking
- ✅ Health checks & Prometheus metrics
- ✅ Testing setup with pytest
- ✅ Docker & docker-compose
- ✅ CI/CD templates (GitHub Actions)

**Modules installed:**
- `settings` - Multi-source configuration
- `auth_core` - Password hashing & JWT tokens
- `db_postgres` - PostgreSQL integration
- `redis` - Redis caching
- `cors` - CORS middleware
- `security_headers` - Security headers
- `logging` - Structured logging
- `deployment` - Production configs

### ecommerce-api

Production-style FastAPI commerce backend with:
- ✅ Product catalog endpoints
- ✅ Cart and checkout workflow
- ✅ PostgreSQL + Redis modules installed
- ✅ Auth core and security headers
- ✅ Health endpoints + structured logging
- ✅ Docker + tests + Ruff

**Modules installed:**
- `settings`
- `logging`
- `deployment`
- `middleware`
- `db_postgres`
- `auth_core`
- `redis`
- `security_headers`

---

## 📁 Workspace Structure

```
quickstart-workspace/
├── README.md              # This file
├── pyproject.toml         # Workspace dependencies
├── poetry.toml           # Poetry config
├── .venv/                # Shared virtual environment
├── product-api/          # FastAPI quickstart demo
└── ecommerce-api/        # FastAPI commerce demo
    ├── src/
    │   ├── main.py       # FastAPI app
    │   ├── routing/      # API routes
    │   ├── modules/      # RapidKit modules
    │   └── health/       # Health checks
    ├── tests/            # Test suite
    ├── config/           # Module configs
    ├── docker-compose.yml
    ├── Dockerfile
    ├── .env.example
    └── Makefile
```

---

## 🚀 Development Workflow

### Add More Modules

```bash
cd product-api

# Add email module
npx workspai add module email

# Add monitoring
npx workspai add module observability.core

# Add rate limiting
npx workspai add module rate_limit
```

### Run Tests

```bash
cd product-api
npx workspai test

# With coverage
pytest --cov=src tests/
```

### Environment Configuration

```bash
# Generate secure secrets
export RAPIDKIT_AUTH_CORE_PEPPER="$(openssl rand -base64 48)"

# Configure database
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/product_db"

# Configure Redis
export REDIS_URL="redis://localhost:6379/0"
```

### Docker Deployment

```bash
cd product-api

# Build and run everything
docker-compose up --build

# Run in background
docker-compose up -d
```

---

## 🔍 Health Check

Validate the workspace setup:

```bash
npx workspai doctor workspace
```

**Checks:**
- Python version (3.10+)
- Poetry installation
- RapidKit Core version
- Virtual environment status
- Project dependencies
- Module configurations

---

## 📊 Key Features Demo

### 1. Authentication

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123"}'
```

### 2. Database Operations

```python
from src.modules.free.database.db_postgres.postgres import get_postgres_db
from sqlalchemy import select

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_postgres_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### 3. Redis Caching

```python
from src.modules.free.cache.redis import redis_dependency

@router.get("/data/{key}")
async def get_cached(key: str, redis=Depends(redis_dependency)):
    cached = await redis.get(key)
    if cached:
        return {"value": cached, "cached": True}
    # Fetch from DB and cache...
```

### 4. Health Endpoints

```bash
# Basic health
curl http://localhost:8000/health

# Module health
curl http://localhost:8000/api/health/module/postgres
curl http://localhost:8000/api/health/module/redis
curl http://localhost:8000/api/health/module/auth-core

# Prometheus metrics
curl http://localhost:8000/metrics
```

---

## 🎓 Learn More

**Tutorial Timeline (from article):**
- **0:00** - Prerequisites check
- **0:30** - Create project
- **1:00** - Install dependencies
- **1:30** - First run & API docs
- **2:00** - Add settings & auth modules
- **2:30** - Add database (PostgreSQL)
- **3:00** - Add Redis caching
- **3:30** - Add CORS & security
- **4:00** - Add logging & monitoring
- **4:30** - Write tests
- **5:00** - Deploy configuration

**Result:** A runnable production-pattern API for learning and extension. Apply
the documented hardening and verification gates before a real deployment.

---

## 📚 Resources

- 📦 **npm CLI:** https://www.npmjs.com/package/workspai
- 🐍 **Python Core:** https://pypi.org/project/rapidkit-core/
- 🧩 **VS Code Extension:** https://marketplace.visualstudio.com/items?itemName=rapidkit.rapidkit-vscode
- 🌐 **Website:** https://www.getrapidkit.com
- 📖 **Documentation:** https://www.workspai.dev/docs

---

## 💡 Next Steps

1. **Explore the code** - Check [product-api/README.md](product-api/README.md) and [ecommerce-api/README.md](ecommerce-api/README.md)
2. **Add features** - Install more modules as needed
3. **Customize** - Modify generated code for your use case
4. **Deploy** - Use provided Docker configs
5. **Scale** - Add more projects to this workspace

---

## ❓ Troubleshooting

### Port Already in Use

```bash
# Workspai can select a free port when the default is unavailable
npx workspai dev

# Or specify port manually
npx workspai dev -p 8001
```

### Database Connection Issues

```bash
# Check if Postgres is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker-compose ps

# Test connection
docker-compose exec redis redis-cli ping
```

### Module Issues

```bash
# Validate setup
npx workspai doctor

# Reinstall dependencies
cd product-api
poetry install
```

---

**Built with Workspai and RapidKit Core.**

If you encounter issues:

1. Ensure Python 3.10+ is installed: `python3 --version`
2. Check RapidKit installation: `npx workspai --version`
3. Run diagnostics: `npx workspai doctor`
4. Visit RapidKit documentation or GitHub issues
