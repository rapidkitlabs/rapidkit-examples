# AI Agent Workspace

A Workspai-managed RapidKit Core workspace with FastAPI and NestJS agent
implementations.

- Medium: https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d
- Dev.to: https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6
- Source repository: https://github.com/rapidkitlabs/rapidkit-examples/tree/main/my-ai-workspace
- FastAPI project: [ai-agent](ai-agent/README.md)
- NestJS project: [ai-agent-nest](ai-agent-nest/README.md)

## Start after clone or download

First restore the FastAPI project's generated Core module payloads from the
repository root, then enter `my-ai-workspace`:

```bash
npm run hydrate:core -- \
  --workspace my-ai-workspace \
  --project ai-agent
cd my-ai-workspace
npx workspai workspace sync
npx workspai workspace contract inspect
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
npx workspai doctor workspace --json
```

The first sync registers this workspace on the current machine and discovers
the FastAPI and NestJS projects. Do not import or adopt the workspace itself;
its portable markers already identify it.

To add another project, use import to copy it into the workspace or adopt to
leave it at its existing path:

```bash
npx workspai import ../existing-agent --workspace . --json
npx workspai adopt ../external-agent --workspace . --dry-run --json
npx workspai adopt ../external-agent --workspace . --json
npx workspai workspace sync
```

Complete baseline, diff, impact, verify, agent context, agent-sync, explain, and
CI workflow: [Workspace onboarding](../WORKSPACE_ONBOARDING.md).

## Quick Start (FastAPI)

```bash
cd ai-agent
cp .env.example .env
npx workspai init
npx workspai dev
```

Notes:

- `npx workspai dev` now auto-switches to a free port if your requested/default port is busy.
- API docs: http://127.0.0.1:8000/docs (or the fallback port printed in terminal).

## Quick Start (NestJS parity example)

```bash
cd ai-agent-nest
cp .env.example .env
npx workspai init
npx workspai dev -p 8013
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
npx workspai doctor workspace
```

The exact tool versions and timestamps depend on the machine. A healthy run
should report both projects and no blocking workspace errors:

```text
Workspace: my-ai-workspace
Projects: 2
  - ai-agent (FastAPI)
  - ai-agent-nest (NestJS)
Contract: passed
```

## Command Reference

When in doubt, print the command catalog:

```bash
npx workspai --help
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
