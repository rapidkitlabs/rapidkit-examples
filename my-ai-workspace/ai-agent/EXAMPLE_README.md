# AI Agent Example Walkthrough

Companion document for the published tutorial:

- Medium: https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d
- Dev.to: https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6
- Source: https://github.com/rapidkitlabs/rapidkit-examples/tree/main/my-ai-workspace

## What this example covers

- Multi-provider assistant (`echo`, `support`, optional `openai`)
- Chat completions + streaming
- Health and cache endpoints
- Support ticket endpoint (`/support/ticket`)

## Build Flow (as in the article)

```bash
npx workspai my-ai-workspace
cd my-ai-workspace
npx workspai create project fastapi.standard ai-agent
cd ai-agent
npx workspai init
npx workspai add module ai_assistant
```

Then configure and run:

```bash
npx workspai dev
```

## API Smoke Checks

```bash
curl http://127.0.0.1:8000/ai/assistant/providers

curl -X POST http://127.0.0.1:8000/ai/assistant/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is RapidKit?","provider":"echo"}'

curl -X POST "http://127.0.0.1:8000/support/ticket?message=My%20payment%20failed"
```

## OpenAI Mode (optional)

```bash
export OPENAI_API_KEY="sk-..."
npx workspai dev
```

When `OPENAI_API_KEY` is not set, the app falls back to local providers so tutorial flows still work.

## Validation

```bash
poetry run pytest tests/ -q
npx workspai modules status
```

Latest local result in this workspace:

- `65 passed, 2 skipped`

## Important Paths

- App entry: `src/main.py`
- AI module routes: `src/modules/free/ai/ai_assistant/routers/ai/ai_assistant.py`
- OpenAI provider: `src/modules/free/ai/ai_assistant/providers/openai_provider.py`
- Support agent: `src/agents/support_agent.py`
- Provider config: `config/ai_assistant.yaml`
