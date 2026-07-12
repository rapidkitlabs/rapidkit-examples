# Enterprise Workspace

An empty Workspai `enterprise` profile fixture for polyglot systems that need a
governance-oriented workspace boundary. Python engine installation was
intentionally deferred in this raw fixture.

## Start after clone or download

```bash
cd enterprise-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
npx workspai doctor workspace --json
```

The first sync registers this cloned workspace on the current machine. An empty
model with zero projects is expected until you add one.

## Add projects

```bash
npx workspai create project
npx workspai import ../existing-service --workspace . --json
npx workspai adopt ../external-service --workspace . --dry-run --json
npx workspai adopt ../external-service --workspace . --json
npx workspai workspace sync
```

## Continue with Workspace Intelligence

```bash
npx workspai workspace model --json --write
npx workspai workspace snapshot --json
npx workspai pipeline --json --strict
```

Complete clone, registry, import, adopt, intelligence, agent grounding, and CI
workflow: [Workspace onboarding](../WORKSPACE_ONBOARDING.md).
