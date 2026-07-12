# Python-only Workspace

An empty Workspai `python-only` profile fixture. Workspace Intelligence is
available; Python engine installation was intentionally deferred in this raw
fixture.

## Start after clone or download

```bash
cd python-only-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
```

The first sync registers this cloned workspace on the current machine. An empty
model with zero projects is expected until you add one.

## Add a project

```bash
npx workspai create project fastapi.standard api --yes
# Or use an existing Python project:
npx workspai import ../existing-api --workspace . --json
npx workspai adopt ../existing-api --workspace . --dry-run --json
npx workspai adopt ../existing-api --workspace . --json
npx workspai workspace sync
```

Initialize all discovered projects when needed:

```bash
npx workspai workspace run init
```

## Continue with Workspace Intelligence

```bash
npx workspai workspace model --json --write
npx workspai workspace snapshot --json
```

Complete clone, registry, import, adopt, intelligence, and CI workflow:
[Workspace onboarding](../WORKSPACE_ONBOARDING.md).
