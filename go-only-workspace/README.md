# Go-only Workspace

An empty Workspai `go-only` profile fixture for Go services.

## Start after clone or download

```bash
cd go-only-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
```

The first sync registers this cloned workspace on the current machine. An empty
model with zero projects is expected until you add one.

## Add a project

```bash
npx workspai create project gofiber.standard my-api --yes
# Or choose the Gin kit:
npx workspai create project gogin.standard my-api --yes
# Or use an existing Go project:
npx workspai import ../existing-api --workspace . --json
npx workspai adopt ../existing-api --workspace . --dry-run --json
npx workspai adopt ../existing-api --workspace . --json
npx workspai workspace sync
```

## Continue with Workspace Intelligence

```bash
npx workspai workspace model --json --write
npx workspai workspace snapshot --json
```

Complete clone, registry, import, adopt, intelligence, and CI workflow:
[Workspace onboarding](../WORKSPACE_ONBOARDING.md).
