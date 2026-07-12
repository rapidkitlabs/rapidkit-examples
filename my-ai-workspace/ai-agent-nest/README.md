# ai-agent-nest

NestJS parity example for RapidKit `ai_assistant`.

**Part of [my-ai-workspace](../README.md).**

This project includes:

- `ai_assistant` module routes under `/ai/assistant/*`
- support workflow endpoint `POST /support/ticket`
- optional OpenAI provider registration via `OPENAI_API_KEY`
- Swagger docs at `/docs`

## Prerequisites

- Node.js 20+
- npm 10+
- Python 3.10+ (for RapidKit workspace tooling)

## Run

```bash
npx workspai init
npx workspai dev -p 8013
```

Alternative:

```bash
PORT=8013 npm run start:dev
```

## Optional OpenAI provider

```bash
OPENAI_API_KEY=your_key npx workspai dev -p 8013
```

When `OPENAI_API_KEY` is set, `openai` is added to provider list.

## Smoke test

```bash
curl http://127.0.0.1:8013/health
curl http://127.0.0.1:8013/ai/assistant/providers
curl http://127.0.0.1:8013/ai/assistant/health
```

Completion:

```bash
curl -X POST http://127.0.0.1:8013/ai/assistant/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is RapidKit?","provider":"echo"}'
```

Stream:

```bash
curl -X POST http://127.0.0.1:8013/ai/assistant/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Give me a deployment checklist","provider":"echo"}'
```

Clear cache:

```bash
curl -X DELETE http://127.0.0.1:8013/ai/assistant/cache
```

Support ticket parity endpoint:

```bash
curl -X POST http://127.0.0.1:8013/support/ticket \
  -H "Content-Type: application/json" \
  -d '{"message":"Customer cannot complete payment"}'
```

## Main files

- `src/modules/free/ai/ai_assistant/ai_assistant.service.ts`
- `src/modules/free/ai/ai_assistant/ai_assistant.controller.ts`
- `src/agents/support-agent.service.ts`
- `src/app.controller.ts`
- `src/modules/index.ts`

## Notes

- In latest module versions, `AiAssistantModule` is auto-injected into `src/modules/index.ts`.
- If you generated an older project and AI routes are missing, ensure this line exists in `optionalModules`:

```ts
registerOptionalModule(() => require('./free/ai/ai_assistant').AiAssistantModule as ModuleRef),
```
