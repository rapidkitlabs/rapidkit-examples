# Java-only Workspace

An empty Workspai `java-only` profile fixture for Java and Spring-oriented
projects.

## Start after clone or download

```bash
cd java-only-workspace
npx workspai workspace sync
npx workspai workspace contract verify --strict --json
npx workspai workspace model --json --write
```

The first sync registers this cloned workspace on the current machine. An empty
model with zero projects is expected until you add one.

## Add a project

```bash
npx workspai create project springboot.standard my-service --yes
# Or use an existing Java project:
npx workspai import ../existing-service --workspace . --json
npx workspai adopt ../existing-service --workspace . --dry-run --json
npx workspai adopt ../existing-service --workspace . --json
npx workspai workspace sync
```

## Continue with Workspace Intelligence

```bash
npx workspai workspace model --json --write
npx workspai workspace snapshot --json
```

Complete clone, registry, import, adopt, intelligence, and CI workflow:
[Workspace onboarding](../WORKSPACE_ONBOARDING.md).
