# ai-agent

Production-ready FastAPI AI Assistant example generated with RapidKit.

- Medium: https://rapidkit.medium.com/build-your-first-ai-agent-with-rapidkit-in-10-minutes-f38a6a12088d
- Dev.to: https://dev.to/rapidkit/build-your-first-ai-agent-with-rapidkit-in-10-minutes-3dj6
- Detailed example guide: [EXAMPLE_README.md](EXAMPLE_README.md)

## Quick Checks

From workspace root (`../`):

```bash
npx rapidkit doctor workspace
npx rapidkit --help
```

## Run

```bash
source .rapidkit/activate
rapidkit init
rapidkit dev
```

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

Current baseline on this workspace:

- `65 passed, 2 skipped`

## Notes on OpenAI

- OpenAI provider is implemented in `src/modules/free/ai/ai_assistant/providers/openai_provider.py`.
- Set `OPENAI_API_KEY` to enable real OpenAI calls.
- Without API key, the app still works via local providers (`echo` / `support`).
