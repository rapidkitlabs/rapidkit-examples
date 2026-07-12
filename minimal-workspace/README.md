# Minimal Workspace

An empty Workspai `minimal` profile fixture. Use it as a lightweight governed
boundary for mixed, existing, or not-yet-classified projects.

## Start after clone or download

```bash
cd minimal-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
```

The first sync registers this cloned workspace on the current machine. An empty
model with zero projects is expected until you add one.

## Add a project

```bash
# Create a supported project inside this workspace
npx workspai create project

# Or copy/clone an existing project into it
npx workspai import ../existing-project --workspace . --json

# Or register a project while leaving it at its current path
npx workspai adopt ../existing-project --workspace . --dry-run --json
npx workspai adopt ../existing-project --workspace . --json

npx workspai workspace sync
```

## Continue with Workspace Intelligence

Create the first baseline, then use the canonical model, diff, impact,
verification, context, agent-sync, and explain workflow:

```bash
npx workspai workspace model --json --write
npx workspai workspace snapshot --json
```

Complete workflow: [Workspace onboarding](../WORKSPACE_ONBOARDING.md).
