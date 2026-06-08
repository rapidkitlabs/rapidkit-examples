# AI Agent Workspace

RapidKit workspace for AI agent examples (FastAPI + NestJS).

- Medium: https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d
- Dev.to: https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6
- Source repository: https://github.com/rapidkitlabs/rapidkit-examples/tree/main/my-ai-workspace
- FastAPI project: [ai-agent](ai-agent/README.md)
- NestJS project: [ai-agent-nest](ai-agent-nest/README.md)

## Quick Start (FastAPI)

```bash
cd ai-agent
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev
```

Notes:

- `rapidkit dev` now auto-switches to a free port if your requested/default port is busy.
- API docs: http://127.0.0.1:8000/docs (or the fallback port printed in terminal).

## Quick Start (NestJS parity example)

```bash
cd ai-agent-nest
cp .env.example .env
source .rapidkit/activate
rapidkit init
rapidkit dev -p 8013
```

Key endpoints:

- `GET /ai/assistant/providers`
- `POST /ai/assistant/completions`
- `POST /ai/assistant/stream`
- `DELETE /ai/assistant/cache`
- `POST /support/ticket`
- `GET /docs`

## Health Check

Before running the project, you can validate the whole workspace:

```bash
npx rapidkit doctor workspace
```

Sample output for this workspace:

```text
🩺 RapidKit Health Check

Workspace: my-ai-workspace
Path: /path/to/my-ai-workspace

📊 Health Score:
    100% ████████████████████
    ✅ 6 passed | ⚠️ 0 warnings | ❌ 0 errors


System Tools:

✅ Python: Python 3.10.19
    Using python3
✅ Poetry: Poetry 2.3.2
    Available for dependency management
✅ pipx: pipx 1.8.0
    Available for global tool installation
✅ RapidKit Core: RapidKit Core 0.3.0
    • Global (pipx): ~/.local/bin/rapidkit -> 0.3.0
    • Global (pyenv): ~/.pyenv/shims/rapidkit -> 0.3.0
    • Workspace (.venv): /path/to/my-ai-workspace/.venv/bin/rapidkit -> 0.3.0

📦 Projects (2):

✅ Project: ai-agent
    🐍 Framework: FastAPI
    Path: /path/to/my-ai-workspace/ai-agent
    ✅ Dependencies: Installed
    ✅ Environment: .env configured
    ✅ Modules: Healthy
    📊 Stats: 5 modules
    🕒 Last Modified: today
    ✅ Tests • ✅ Docker • ✅ Ruff

✅ Project: ai-agent-nest
    🦅 Framework: NestJS
    Path: /path/to/my-ai-workspace/ai-agent-nest
    ✅ Dependencies: Installed
    ✅ Environment: .env configured
    ✅ Modules: Healthy
    📊 Stats: 5 modules
    🕒 Last Modified: today
    ✅ Tests • ✅ Docker • ✅ ESLint

✅ All checks passed! Workspace is healthy.
```

## Command Reference

When in doubt, print the command catalog:

```bash
npx rapidkit --help
```

Use this to quickly see global commands (create, doctor, modules, etc.) and project commands (init/dev/test/lint).

## Workspace Layout

```text
my-ai-workspace/
├── README.md
├── ai-agent/
│   ├── README.md
│   └── EXAMPLE_README.md
└── ai-agent-nest/
    └── README.md
```

Use:

- `ai-agent/README.md` for day-to-day development commands
- `ai-agent/EXAMPLE_README.md` for tutorial walkthrough and API usage examples
- `ai-agent-nest/README.md` for NestJS parity implementation and endpoint checks
