# RapidKit Examples

[![Part of RapidKit Platform](https://img.shields.io/badge/Part%20of-RapidKit%20Workspace%20Platform-0f172a?logo=github)](https://github.com/rapidkitlabs/rapidkit)

Official example projects for RapidKit.

This repository contains production-style reference implementations that accompany RapidKit tutorials and articles.

It is also the public discovery layer for Pro workspaces. Pro showcase pages live under [`pro-showcase`](pro-showcase), but paid source code, customer archives, and release evidence stay private in `rapidkit-examples-pro`.

## Product Standard

This repository follows the RapidKit + Workspai workspace product operating standard:

- Free examples are cloneable and useful on their own.
- Pro showcases are public, source-free, and honest about availability.
- Catalog promotion happens only after a Workspai manifest is backed by a real example or release candidate.
- Product planning is managed separately; this repository is the public publication surface, not a backlog.

Machine-readable index: [`examples.json`](examples.json)

Public Pro showcase: [`pro-showcase`](pro-showcase)

## Part of the RapidKit Ecosystem

RapidKit Examples is the adoption layer of the platform.

| Layer | Repository |
|---|---|
| Ecosystem Hub | [getrapidkit/rapidkit](https://github.com/rapidkitlabs/rapidkit) |
| CLI | [getrapidkit/rapidkit-npm](https://github.com/rapidkitlabs/rapidkit-npm) |
| IDE | [getrapidkit/rapidkit-vscode](https://github.com/rapidkitlabs/rapidkit-vscode) |
| Core Engine | [getrapidkit/rapidkit-core](https://github.com/rapidkitlabs/rapidkit-core) |

> **One-click start:** Install the [RapidKit VS Code Extension](https://marketplace.visualstudio.com/items?itemName=rapidkit.rapidkit-vscode), open the **RapidKit Welcome** panel, and clone any example workspace directly into your environment — no CLI commands needed.

---

## 🚀 Featured Examples

### 1. Quickstart Workspace (⚡ Beginner)

**Path:** [quickstart-workspace](quickstart-workspace)

**Description:** Production-ready FastAPI in 5 minutes

**Includes:**
- `product-api` (FastAPI): Complete API with auth, database, caching, monitoring
- JWT Authentication (register, login, refresh)
- PostgreSQL with SQLAlchemy (async & sync)
- Redis caching with connection pooling
- CORS & Security Headers
- Structured logging & Prometheus metrics
- Docker & CI/CD templates

**Modules:** `settings`, `auth_core`, `db_postgres`, `redis`, `cors`, `security_headers`, `logging`, `deployment`

**Articles:**
- Medium: [From Zero to Production FastAPI with RapidKit: Build a Real E-Commerce API](https://medium.com/@rapidkit/from-zero-to-production-fastapi-with-rapidkit-build-a-real-e-commerce-api-80390a34ffe3)
- Dev.to: [Build a Production-Ready FastAPI E-Commerce API with RapidKit (Step-by-Step)](https://dev.to/rapidkit/build-a-production-ready-fastapi-e-commerce-api-with-rapidkit-step-by-step-llm)

---

### 2. AI Agent Workspace (🤖 Intermediate)

**Path:** [my-ai-workspace](my-ai-workspace)

**Description:** Multi-provider AI assistant with FastAPI and NestJS

**Includes:**
- `ai-agent` (FastAPI): Multi-provider AI assistant (echo/template/OpenAI-ready)
- `ai-agent-nest` (NestJS): Parity implementation with `ai_assistant` module
- Streaming + caching endpoints
- Health checks & support ticket workflow
- Integrated tests and module status checks

**Modules:** `ai_assistant`, `settings`, `logging`

**Articles:**
- Medium: [Build Your First AI Agent with RapidKit in 10 Minutes](https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d)
- Dev.to: [Build Your First AI Agent with RapidKit in 10 Minutes](https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6)

---

### 3. SaaS Starter Workspace (🏢 Advanced)

**Path:** [saas-starter-workspace](saas-starter-workspace)

**Description:** Complete multi-project SaaS backend foundation with FastAPI + NestJS + webhooks.

**Includes:**
- `saas-api` (FastAPI): Main API for auth, profiles, subscriptions, billing, teams
- `saas-admin` (FastAPI): Admin backend for user moderation and metrics
- `saas-nest` (NestJS): Framework parity implementation + shared module health routes
- `saas-webhooks` (FastAPI): Stripe webhook intake, logs, replay, retry-oriented processing

**Modules:** `settings`, `logging`, `db_postgres`, `redis`, `auth_core`, `oauth`, `session`, `users_core`, `users_profiles`, `stripe_payment`, `cart`, `inventory`, `security_headers`, `rate_limiting`, `celery`, `email`, `notifications`

**Articles:**
- Medium: [Building Production SaaS Architecture: Deep Dive into Multi-Service Implementation](https://rapidkit.medium.com/building-production-saas-architecture-deep-dive-into-multi-service-implementation-8a838f36e4ad)
- Dev.to: [Build Production SaaS: Code Walkthrough (FastAPI + NestJS + Webhooks)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-4c7c)

---

## 💡 VS Code Extension (Recommended)

**The fastest way to work with RapidKit workspaces.**

### 🎯 Why Use the Extension?

Skip manual cloning and setup. The [RapidKit VS Code Extension](https://marketplace.visualstudio.com/items?itemName=rapidkit.rapidkit-vscode) provides a complete integrated development experience for RapidKit projects.

### ✨ Key Features

**1. One-Click Workspace Import**
- **Clone from GitHub** — Paste any RapidKit workspace URL, clone instantly
- **Import Downloaded Workspaces** — Drag & drop `.zip` files or browse local folders
- **Welcome Page** — Visual gallery of all available example workspaces

**2. Integrated Project Management**
- **Run/Stop Services** — Start development servers from the sidebar
- **View Logs** — Real-time log streaming in integrated terminal
- **Health Checks** — Monitor module status with visual indicators
- **Port Management** — Auto-detect and resolve port conflicts

**3. Module Management**
- **Install Modules** — GUI wizard for adding modules (auth, database, AI, etc.)
- **Configure Settings** — Visual editors for module configurations
- **Module Status** — See which modules are installed and their health

**4. Development Tools**
- **RapidKit Terminal** — Integrated terminal with command autocomplete
- **Quick Actions** — Run migrations, tests, or custom scripts with one click
- **Project Templates** — Scaffolding wizards for new projects
- **Multi-Project Workspaces** — Manage multiple services simultaneously

**5. Testing & Debugging**
- **Run Tests** — Execute test suites from the sidebar
- **Debug Configuration** — Pre-configured debug profiles
- **Coverage Reports** — View test coverage inline

### 📦 Installation

**Option 1: From VS Code**
1. Open VS Code
2. Go to Extensions (`Cmd/Ctrl+Shift+X`)
3. Search for "RapidKit"
4. Click **Install**

**Option 2: Command Line**
```bash
code --install-extension rapidkit.rapidkit-vscode
```

**Option 3: Direct Download**
- Visit: https://marketplace.visualstudio.com/items?itemName=rapidkit.rapidkit-vscode
- Click "Install"

### 🚀 Quick Start with Extension

**Import This Repository:**

1. Open VS Code
2. Open Command Palette (`Cmd/Ctrl+Shift+P`)
3. Type: **RapidKit: Import Workspace**
4. Paste: `https://github.com/rapidkitlabs/rapidkit-examples.git`
5. Select workspace (quickstart-workspace, my-ai-workspace, or saas-starter-workspace)
6. Click **Import & Setup**

**That's it!** The extension will:
- Clone the repository
- Install dependencies
- Configure environment
- Open the workspace
- Show available services in the sidebar

**Run a Project:**

1. Open RapidKit sidebar (left panel)
2. Expand "Projects"
3. Click ▶️ next to any project (e.g., `product-api`)
4. Extension starts the dev server automatically
5. Click 🌐 to open in browser

### 🎬 Example Workflow

**Scenario: Run the SaaS Starter Workspace**

```
Command Palette → RapidKit: Import Workspace
→ Paste: https://github.com/rapidkitlabs/rapidkit-examples.git
→ Select: saas-starter-workspace
→ Click: Import & Setup
```

**After import:**
- Sidebar shows 4 projects: `saas-api`, `saas-admin`, `saas-nest`, `saas-webhooks`
- Click ▶️ on `saas-api` → Dev server starts on port 8000
- Click ▶️ on `saas-admin` → Starts on port 8001
- Click 🌐 → Opens Swagger docs automatically
- Click 📊 → View logs in integrated terminal

**Need to add a module?**
- Right-click project → **Install Module**
- Select module (e.g., `stripe_payment`)
- Extension installs and configures automatically
- Service restarts with new module

### 📱 Extension UI Overview

**Sidebar Panels:**
- **📦 Workspaces** — All imported workspaces
- **🎯 Projects** — Services within active workspace
- **🧩 Modules** — Installed modules with status indicators
- **⚙️ Settings** — Quick access to configurations
- **📝 Logs** — Real-time log viewer

**Status Bar:**
- **RapidKit CLI Version** — Click to check for updates
- **Active Workspace** — Current workspace name
- **Running Services** — Count of active dev servers

### 🔧 Advanced Features

**1. Workspace Health Check:**
- Right-click workspace → **Run Health Check**
- Extension validates Python, Poetry, dependencies, modules
- Shows actionable fixes for any issues

**2. Module Configuration:**
- Click any module in sidebar
- Visual editor for `config/{module}.toml` files
- Autocomplete for configuration options

**3. Custom Scripts:**
- Define scripts in `pyproject.toml`:
  ```toml
  [tool.rapidkit.scripts]
  seed-db = "python scripts/seed_database.py"
  migrate = "alembic upgrade head"
  ```
- Run from Command Palette: **RapidKit: Run Script**

**4. Multi-Workspace Support:**
- Open multiple RapidKit workspaces side-by-side
- Switch between workspaces in dropdown
- Each workspace has independent service states

### 🆚 Extension vs Manual Setup

| Task | Manual | With Extension |
|------|--------|----------------|
| Clone workspace | 4 commands | 1 click |
| Install dependencies | 3 commands per project | Automatic |
| Start dev server | Terminal, type commands | Click ▶️ |
| Check logs | Switch terminals | Integrated viewer |
| Install module | CLI + config edits | GUI wizard |
| Health check | `npx rapidkit doctor` | Right-click menu |
| Port conflicts | Manual debugging | Auto-resolves |

**Time saved per project: ~5-10 minutes**

### 🐛 Troubleshooting

**Extension not showing workspaces?**
- Reload window: `Cmd/Ctrl+Shift+P` → **Reload Window**
- Check output panel: **View → Output → RapidKit**

**Project won't start?**
- Right-click → **Run Health Check**
- Install missing dependencies: Right-click → **Install Dependencies**

**Module installation fails?**
- Check logs in Output panel
- Ensure virtual environment is activated
- Try: Right-click project → **Rebuild Environment**

### 📚 Learn More

- **Extension Docs:** https://docs.getrapidkit.com/vscode
- **Video Tutorial:** https://www.youtube.com/@rapidkit
- **Report Issues:** https://github.com/rapidkit/vscode-extension/issues

---

## ⚡ Quick Start (Manual Setup)

### Quickstart Workspace (Beginner - 5 minutes)

**Production-ready FastAPI with auth, database, caching:**

```bash
git clone https://github.com/rapidkitlabs/rapidkit-examples.git
cd rapidkit-examples/quickstart-workspace/product-api

# Start infrastructure
docker-compose up -d postgres redis

# Install & run
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev
```

**Endpoints:**
- 📚 API Docs: http://localhost:8000/docs
- ❤️ Health: http://localhost:8000/health
- 🔐 Auth: http://localhost:8000/api/health/module/auth-core
- 💾 Database: http://localhost:8000/api/health/module/postgres
- 🗄️ Redis: http://localhost:8000/api/health/module/redis
- 📊 Metrics: http://localhost:8000/metrics

---

### AI Agent Workspace (Intermediate)

**FastAPI:**

```bash
git clone https://github.com/rapidkitlabs/rapidkit-examples.git
cd rapidkit-examples/my-ai-workspace/ai-agent
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev
```

**NestJS:**

```bash
cd rapidkit-examples/my-ai-workspace/ai-agent-nest
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev -p 8013
```

**Endpoints:**
- 📚 Swagger UI: http://127.0.0.1:8000/docs (or auto-fallback port)
- 🤖 AI Providers: `GET /ai/assistant/providers`
- 💬 Completions: `POST /ai/assistant/completions`
- 📡 Streaming: `POST /ai/assistant/stream`
- 🎫 Support Ticket: `POST /support/ticket`

---

### SaaS Starter Workspace (Advanced)

```bash
git clone https://github.com/rapidkitlabs/rapidkit-examples.git
cd rapidkit-examples/saas-starter-workspace
npx rapidkit doctor workspace
```

**Run each service:**

```bash
# Main SaaS API
cd saas-api
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev

# Admin API
cd ../saas-admin
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev -p 8001

# NestJS API
cd ../saas-nest
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev -p 8002

# Webhooks service
cd ../saas-webhooks
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev -p 8003
```

**Key endpoints:**
- `saas-api`: `/auth/register`, `/subscriptions/plans`, `/teams`
- `saas-admin`: `/admin/users`, `/admin/subscriptions`, `/admin/health`
- `saas-nest`: `/docs`, `/api/health/module/{module}`
- `saas-webhooks`: `POST /api/webhooks/stripe`, `GET /api/webhooks/logs`, `POST /api/webhooks/replay/{event_id}`

## 🔍 Workspace Health Check

**Quickstart Workspace:**

```bash
cd quickstart-workspace
npx rapidkit doctor workspace
```

**AI Agent Workspace:**

```bash
cd my-ai-workspace
npx rapidkit doctor workspace
```

**SaaS Starter Workspace:**

```bash
cd saas-starter-workspace
npx rapidkit doctor workspace
```

**Checks:**
- ✅ Python version (3.10+)
- ✅ Poetry installation
- ✅ RapidKit Core version
- ✅ Virtual environment status
- ✅ Project dependencies
- ✅ Module configurations

## 📁 Repository Layout

```text
rapidkit-examples/
├── README.md                    # This file
├── examples.json                # Workspace metadata
│
├── quickstart-workspace/        # ⚡ Beginner (5 minutes)
│   ├── README.md               # Workspace guide
│   ├── pyproject.toml          # Workspace dependencies
│   └── product-api/            # Production-ready API
│       ├── README.md           # Project guide
│       ├── src/
│       │   ├── main.py         # FastAPI app
│       │   ├── modules/        # RapidKit modules
│       │   ├── routing/        # API routes
│       │   └── health/         # Health probes
│       ├── tests/              # Test suite
│       ├── config/             # Module configs
│       ├── docker-compose.yml  # Postgres + Redis
│       └── Dockerfile          # Production image
│
├── my-ai-workspace/            # 🤖 Intermediate (10 minutes)
    ├── README.md               # Workspace guide
    ├── ai-agent/               # FastAPI AI assistant
    │   ├── README.md
    │   └── EXAMPLE_README.md   # Tutorial walkthrough
    └── ai-agent-nest/          # NestJS implementation
        └── README.md
│
└── saas-starter-workspace/     # 🏢 Advanced (15-20 minutes)
    ├── README.md               # Workspace guide
    ├── saas-api/               # Main SaaS API (FastAPI)
    ├── saas-admin/             # Admin API (FastAPI)
    ├── saas-nest/              # Framework comparison (NestJS)
    └── saas-webhooks/          # Stripe webhook processor (FastAPI)
```

## 📚 Documentation Structure

**Quickstart Workspace:**
- [quickstart-workspace/README.md](quickstart-workspace/README.md) - Workspace setup & overview
- [quickstart-workspace/product-api/README.md](quickstart-workspace/product-api/README.md) - Project guide & usage

**AI Agent Workspace:**
- [my-ai-workspace/README.md](my-ai-workspace/README.md) - Workspace-level setup
- [my-ai-workspace/ai-agent/README.md](my-ai-workspace/ai-agent/README.md) - FastAPI run/test commands
- [my-ai-workspace/ai-agent/EXAMPLE_README.md](my-ai-workspace/ai-agent/EXAMPLE_README.md) - Tutorial walkthrough
- [my-ai-workspace/ai-agent-nest/README.md](my-ai-workspace/ai-agent-nest/README.md) - NestJS parity guide

**SaaS Starter Workspace:**
- [saas-starter-workspace/README.md](saas-starter-workspace/README.md) - Workspace setup & commands
- [saas-starter-workspace/saas-api/README.md](saas-starter-workspace/saas-api/README.md) - Main SaaS API
- [saas-starter-workspace/saas-admin/README.md](saas-starter-workspace/saas-admin/README.md) - Admin service
- [saas-starter-workspace/saas-nest/README.md](saas-starter-workspace/saas-nest/README.md) - NestJS parity service
- [saas-starter-workspace/saas-webhooks/README.md](saas-starter-workspace/saas-webhooks/README.md) - Webhooks processor

---

## 🎓 Learn More

**RapidKit Resources:**
- 📦 **npm CLI:** https://www.npmjs.com/package/rapidkit
- 🐍 **Python Core:** https://pypi.org/project/rapidkit-core/
- 🧩 **VS Code Extension:** https://marketplace.visualstudio.com/items?itemName=rapidkit.rapidkit-vscode
- 🌐 **Website:** https://www.getrapidkit.com
- 📖 **Documentation:** https://docs.getrapidkit.com

**Tutorial Articles:**
- Medium: https://rapidkit.medium.com
- Dev.to: https://dev.to/rapidkit

---

## 🚀 Coming Soon

- **product-workspace** - Step-by-step tutorial (Article 6)
- **ecommerce-workspace** - Multi-service architecture (Article 10)
- **ddd-workspace** - DDD + CQRS patterns (Article 11)
- **AI workspaces** - Advanced AI patterns (Articles 7-8)

---

**Built with RapidKit** 🚀
