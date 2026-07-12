# ai-agent

FastAPI AI assistant example generated with RapidKit Core and managed through
the current Workspai workspace.

**Part of [my-ai-workspace](../README.md).**

- Medium: https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d
- Dev.to: https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6
- Detailed example guide: [EXAMPLE_README.md](EXAMPLE_README.md)
- Workspace clone, intelligence, and agent-grounding workflow:
  [Workspace onboarding](../../WORKSPACE_ONBOARDING.md)

## Quick Checks

From workspace root (`../`):

```bash
npx workspai doctor workspace
npx workspai --help
```

## Run

```bash
npx workspai init
npx workspai dev
```

API and OpenAPI docs: http://127.0.0.1:8000/docs

Alternative:

```bash
poetry run uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

## Core Endpoints

- `GET /docs`
- `GET /ai/assistant/providers`
- `POST /ai/assistant/completions`
- `POST /ai/assistant/stream`
- `GET /ai/assistant/health`
- `POST /support/ticket`

## Tests

```bash
poetry run pytest tests/ -q
```

Test counts can change with the example. Treat the current command result as
the evidence for the checked-out revision.

## Deployment

This example includes the RapidKit deployment module assets so it can move from
local development to a container or production host without changing the
Workspace Intelligence flow.

Before deploying, copy `.env.example` to `.env`, set runtime secrets such as
`OPENAI_API_KEY`, and run the workspace checks that produce release evidence:

```bash
npx workspai workspace model --json
npx workspai pipeline --json --strict
```

Use the generated `Dockerfile`, `docker-compose.yml`, and project health
endpoints as the deployment baseline for local containers, CI, or a managed
hosting target.

## Notes on OpenAI

- OpenAI provider is implemented in `src/modules/free/ai/ai_assistant/providers/openai_provider.py`.
- Set `OPENAI_API_KEY` to enable real OpenAI calls.
- Without API key, the app still works via local providers (`echo` / `support`).
