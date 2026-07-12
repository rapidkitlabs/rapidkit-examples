import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const failures = [];
const trackedFiles = process.argv.includes('--tracked-stdin')
  ? new Set(fs.readFileSync(0, 'utf8').split('\0').filter(Boolean))
  : null;

if (trackedFiles) {
  for (const relativePath of trackedFiles) {
    if (/\/.rapidkit\/(?:vendor|snapshots|audit|reports|tmp)\//.test(relativePath)) {
      failures.push(`Generated RapidKit state must not be published: ${relativePath}`);
    }
  }
}

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));
}

function requireFile(relativePath) {
  if (!fs.existsSync(path.join(root, relativePath))) {
    failures.push(`Missing required file: ${relativePath}`);
  }
}

const index = readJson('examples.json');
requireFile('PUBLICATION_CONTRACT.md');
requireFile('WORKSPACE_ONBOARDING.md');
if (index.schemaVersion !== 'workspai.examples-index.v1') {
  failures.push(`Unexpected examples schema: ${index.schemaVersion}`);
}

const rootReadme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
const positioningRequirements = [
  'Workspai is not another AI coding assistant',
  'One workspace. One truth. Humans and AI aligned.',
  'evidence-backed intelligence layer',
  '`AGENTS.md`, skills, structured reports',
  'instead of competing with them',
  '### Choose a learning path',
];
for (const requirement of positioningRequirements) {
  if (!rootReadme.includes(requirement)) {
    failures.push(`Root README lacks Workspace Intelligence positioning: ${requirement}`);
  }
}

const published = index.workspaces.filter((workspace) => workspace.lifecycleStatus === 'published');
const portableFiles = [];
const rapidkitCoreVersion = '0.5.5';
const pythonProjectBaseline = {
  fastapi: '^0.139.0',
  uvicorn: '^0.50.2',
  pydantic: '^2.12.5',
  pytest: '^9.0.3',
  black: '^26.3.1',
};

function lockedPackageVersion(lockContent, packageName) {
  const escaped = packageName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = lockContent.match(
    new RegExp(
      `\\[\\[package\\]\\][\\s\\S]*?name = "${escaped}"[\\s\\S]*?version = "([^"]+)"(?=[\\s\\S]*?(?:\\n\\[\\[package\\]\\]|$))`
    )
  );
  return match?.[1] ?? null;
}

function compareVersions(left, right) {
  const leftParts = left.split('.').map(Number);
  const rightParts = right.split('.').map(Number);
  for (let index = 0; index < Math.max(leftParts.length, rightParts.length); index += 1) {
    const difference = (leftParts[index] ?? 0) - (rightParts[index] ?? 0);
    if (difference !== 0) return Math.sign(difference);
  }
  return 0;
}

function satisfiesLockedBaseline(actual, minimum, nextExclusive) {
  return (
    actual !== null &&
    compareVersions(actual, minimum) >= 0 &&
    compareVersions(actual, nextExclusive) < 0
  );
}

function collectFiles(directory, predicate) {
  if (!fs.existsSync(directory)) return [];
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...collectFiles(absolutePath, predicate));
    else if (predicate(absolutePath)) files.push(absolutePath);
  }
  return files;
}

function vendorModuleName(slug) {
  const aliases = {
    'free/auth/core': 'auth_core',
    'free/observability/core': 'observability_core',
  };
  return aliases[slug] ?? slug.split('/').at(-1);
}
const supportedProfiles = [
  'minimal',
  'java-only',
  'python-only',
  'node-only',
  'go-only',
  'dotnet-only',
  'polyglot',
  'enterprise',
];

const workspaceOnboardingRequirements = [
  ['npx workspai workspace sync', 'workspace reconciliation'],
  [
    'npx workspai workspace contract verify --strict --json',
    'strict workspace contract verification',
  ],
  ['npx workspai workspace model --json --write', 'canonical workspace model'],
  ['WORKSPACE_ONBOARDING.md', 'complete workspace onboarding guide'],
];

function validateWorkspaceReadme(workspaceRoot) {
  const readmePath = `${workspaceRoot}/README.md`;
  requireFile(readmePath);
  const absolutePath = path.join(root, readmePath);
  if (!fs.existsSync(absolutePath)) return;

  const content = fs.readFileSync(absolutePath, 'utf8');
  for (const [needle, label] of workspaceOnboardingRequirements) {
    if (!content.includes(needle)) {
      failures.push(`Workspace README lacks ${label}: ${readmePath}`);
    }
  }
}

for (const workspace of published) {
  const workspaceRoot = workspace.path;
  validateWorkspaceReadme(workspaceRoot);
  const rootPyprojectPath = `${workspaceRoot}/pyproject.toml`;
  const rootLockPath = `${workspaceRoot}/poetry.lock`;
  requireFile(rootPyprojectPath);
  requireFile(rootLockPath);
  if (fs.existsSync(path.join(root, rootPyprojectPath))) {
    const pyproject = fs.readFileSync(path.join(root, rootPyprojectPath), 'utf8');
    if (!pyproject.includes(`rapidkit-core (==${rapidkitCoreVersion})`)) {
      failures.push(
        `Workspace must pin rapidkit-core==${rapidkitCoreVersion}: ${workspaceRoot}`
      );
    }
  }
  if (fs.existsSync(path.join(root, rootLockPath))) {
    const lock = fs.readFileSync(path.join(root, rootLockPath), 'utf8');
    const coreBlock = lock.match(
      /name = "rapidkit-core"[\s\S]*?version = "([^"]+)"[\s\S]*?(?=\n\[\[package\]\]|$)/
    );
    if (coreBlock?.[1] !== rapidkitCoreVersion) {
      failures.push(
        `Workspace lock must contain rapidkit-core ${rapidkitCoreVersion}: ${workspaceRoot}`
      );
    }
  }
  const required = [
    `${workspaceRoot}/.workspai-workspace`,
    `${workspaceRoot}/.workspai/workspace.json`,
    `${workspaceRoot}/.workspai/workspace.contract.json`,
    `${workspaceRoot}/.workspai/policies.yml`,
    `${workspaceRoot}/.workspai/toolchain.lock`,
    `${workspaceRoot}/.workspai/cache-config.yml`,
  ];
  required.forEach(requireFile);
  portableFiles.push(...required);

  const contractPath = `${workspaceRoot}/.workspai/workspace.contract.json`;
  if (!fs.existsSync(path.join(root, contractPath))) continue;

  const contract = readJson(contractPath);
  if (contract.kind !== 'rapidkit.workspace.contract' || contract.schemaVersion !== 1) {
    failures.push(`Invalid workspace contract identity: ${contractPath}`);
  }

  const indexedProjects = workspace.projects
    .map((project) => ({
      slug: project.name,
      relativePath: path.relative(workspaceRoot, project.path).replaceAll(path.sep, '/'),
    }))
    .sort((a, b) => a.slug.localeCompare(b.slug));
  const contractProjects = contract.projects
    .map((project) => ({ slug: project.slug, relativePath: project.relativePath }))
    .sort((a, b) => a.slug.localeCompare(b.slug));

  if (JSON.stringify(indexedProjects) !== JSON.stringify(contractProjects)) {
    failures.push(`Catalog/contract project drift: ${workspaceRoot}`);
  }

  const indexedPorts = new Map(
    workspace.projects.map((project) => [project.name, project.defaultPort])
  );
  for (const project of contract.projects) {
    const contractPort = project.ports?.find((port) => port.name === 'http')?.port;
    if (contractPort !== indexedPorts.get(project.slug)) {
      failures.push(
        `Catalog/contract HTTP port drift: ${workspaceRoot}/${project.slug} ` +
          `(catalog ${indexedPorts.get(project.slug)}, contract ${contractPort})`
      );
    }
  }

  for (const project of workspace.projects) {
    requireFile(`${project.path}/.rapidkit/project.json`);

    const projectReadmePath = path.join(root, project.path, 'README.md');
    requireFile(`${project.path}/README.md`);
    if (fs.existsSync(projectReadmePath)) {
      const projectReadme = fs.readFileSync(projectReadmePath, 'utf8');
      if (!projectReadme.includes('(../README.md)')) {
        failures.push(`Project README lacks parent workspace navigation: ${project.path}`);
      }
      if (!projectReadme.includes(`:${project.defaultPort}`)) {
        failures.push(
          `Project README does not expose catalog port ${project.defaultPort}: ${project.path}`
        );
      }
    }

    const projectPyprojectPath = path.join(root, project.path, 'pyproject.toml');
    const projectLockPath = path.join(root, project.path, 'poetry.lock');
    const projectPackagePath = path.join(root, project.path, 'package.json');
    const projectPackageLockPath = path.join(root, project.path, 'package-lock.json');
    if (fs.existsSync(projectPyprojectPath)) {
      const pyproject = fs.readFileSync(projectPyprojectPath, 'utf8');
      for (const [name, version] of Object.entries(pythonProjectBaseline)) {
        if (!pyproject.includes(`${name}`) || !pyproject.includes(version)) {
          failures.push(
            `Python project baseline drift (${name} ${version}): ${project.path}`
          );
        }
      }
      if (!fs.existsSync(projectLockPath)) {
        failures.push(`Python project lock missing: ${project.path}`);
      }
    }
    if (fs.existsSync(projectLockPath)) {
      const lock = fs.readFileSync(projectLockPath, 'utf8');
      const expectedLocks = {
        fastapi: ['0.139.0', '0.140.0'],
        uvicorn: ['0.50.2', '0.51.0'],
        pydantic: ['2.12.5', '3.0.0'],
        pytest: ['9.0.3', '10.0.0'],
        black: ['26.3.1', '27.0.0'],
      };
      for (const [name, [minimum, nextExclusive]] of Object.entries(expectedLocks)) {
        const actual = lockedPackageVersion(lock, name);
        if (!satisfiesLockedBaseline(actual, minimum, nextExclusive)) {
          failures.push(
            `Python lock baseline drift (${name}: expected >=${minimum}, <${nextExclusive}; got ${actual}): ${project.path}`
          );
        }
      }
    }
    if (fs.existsSync(projectPackagePath) && !fs.existsSync(projectPackageLockPath)) {
      failures.push(`Node project lock missing: ${project.path}`);
    }
    if (!fs.existsSync(projectPyprojectPath) && !fs.existsSync(projectPackagePath)) {
      failures.push(`Project has no supported runtime manifest: ${project.path}`);
    }

    const registryPath = path.join(root, project.path, 'registry.json');
    requireFile(`${project.path}/registry.json`);
    if (fs.existsSync(registryPath)) {
      const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
      const installedByVendorName = new Map(
        (registry.installed_modules ?? []).map((module) => [
          vendorModuleName(module.slug),
          module,
        ])
      );
      for (const sourcePath of collectFiles(path.join(root, project.path, 'src'), (file) =>
        file.endsWith('.py')
      )) {
        const source = fs.readFileSync(sourcePath, 'utf8');
        const moduleMatch = source.match(/_VENDOR_MODULE = "([^"]+)"/);
        const versionMatch = source.match(/_VENDOR_VERSION = "([^"]+)"/);
        if (!moduleMatch || !versionMatch) continue;

        const installed = installedByVendorName.get(moduleMatch[1]);
        const relativeSource = path.relative(root, sourcePath);
        if (!installed) {
          failures.push(`Vendor wrapper has no installed module: ${relativeSource}`);
          continue;
        }
        if (versionMatch[1] !== installed.version) {
          failures.push(
            `Vendor wrapper version drift (${moduleMatch[1]}: registry ${installed.version}, wrapper ${versionMatch[1]}): ${relativeSource}`
          );
        }
      }

      const settingsModule = (registry.installed_modules ?? []).find(
        (module) => module.slug === 'free/essentials/settings'
      );
      if (settingsModule) {
        for (const sourcePath of collectFiles(
          path.join(root, project.path, 'src'),
          (file) => file.endsWith('.ts')
        )) {
          const source = fs.readFileSync(sourcePath, 'utf8');
          if (!source.includes('vendor/settings')) continue;
          const versionMatches = [
            ...source.matchAll(/(?:DEFAULT_)?VENDOR_VERSION\s*=\s*['"]([^'"]+)['"]/g),
          ];
          for (const versionMatch of versionMatches) {
            if (versionMatch[1] !== settingsModule.version) {
              failures.push(
                `TypeScript settings vendor drift (registry ${settingsModule.version}, wrapper ${versionMatch[1]}): ${path.relative(root, sourcePath)}`
              );
            }
          }
        }
      }
    }

    const snippetRegistryPath = path.join(root, project.path, '.rapidkit/snippet_registry.json');
    requireFile(`${project.path}/.rapidkit/snippet_registry.json`);
    if (fs.existsSync(snippetRegistryPath)) {
      const snippetRegistry = JSON.parse(fs.readFileSync(snippetRegistryPath, 'utf8'));
      for (const [key, snippet] of Object.entries(snippetRegistry.snippets ?? {})) {
        if (snippet.status === 'failed' || snippet.status === 'pending') {
          failures.push(
            `Unresolved snippet state (${snippet.status}): ${project.path}/${key}`
          );
        }
      }
    }

    const envExamplePath = path.join(root, project.path, '.env.example');
    if (fs.existsSync(envExamplePath)) {
      const envExample = fs.readFileSync(envExamplePath, 'utf8');
      const portMatch = envExample.match(/^(?:APP_PORT|PORT)=["']?(\d+)["']?$/m);
      if (portMatch && Number(portMatch[1]) !== project.defaultPort) {
        failures.push(
          `Catalog/.env.example port drift: ${project.path} ` +
            `(catalog ${project.defaultPort}, env ${portMatch[1]})`
        );
      }
    }

    for (const runtimeFile of ['Makefile', 'docker-compose.yml']) {
      const runtimePath = path.join(root, project.path, runtimeFile);
      if (!fs.existsSync(runtimePath)) continue;
      const runtimeContent = fs.readFileSync(runtimePath, 'utf8');
      const uvicornPorts = [
        ...runtimeContent.matchAll(/uvicorn[^\n]*--port\s+(\d+)/g),
      ].map((match) => Number(match[1]));
      for (const runtimePort of uvicornPorts) {
        if (runtimePort !== project.defaultPort) {
          failures.push(
            `Catalog/${runtimeFile} port drift: ${project.path} ` +
              `(catalog ${project.defaultPort}, runtime ${runtimePort})`
          );
        }
      }
    }
  }
}

const profileFixtures = index.profileWorkspaces ?? [];
const indexedProfiles = profileFixtures.map((fixture) => fixture.profile).sort();
if (JSON.stringify(indexedProfiles) !== JSON.stringify([...supportedProfiles].sort())) {
  failures.push('Profile fixture index must contain each supported profile exactly once.');
}

for (const fixture of profileFixtures) {
  const workspaceRoot = fixture.path;
  validateWorkspaceReadme(workspaceRoot);
  const required = [
    `${workspaceRoot}/.workspai-workspace`,
    `${workspaceRoot}/.workspai/workspace.json`,
    `${workspaceRoot}/.workspai/workspace.contract.json`,
    `${workspaceRoot}/.workspai/policies.yml`,
    `${workspaceRoot}/.workspai/toolchain.lock`,
    `${workspaceRoot}/.workspai/cache-config.yml`,
    `${workspaceRoot}/.gitignore`,
    `${workspaceRoot}/README.md`,
  ];
  required.forEach(requireFile);
  portableFiles.push(...required);

  const manifestPath = `${workspaceRoot}/.workspai/workspace.json`;
  const contractPath = `${workspaceRoot}/.workspai/workspace.contract.json`;
  if (fs.existsSync(path.join(root, manifestPath))) {
    const manifest = readJson(manifestPath);
    if (manifest.profile !== fixture.profile || manifest.workspace_name !== fixture.name) {
      failures.push(`Profile manifest drift: ${workspaceRoot}`);
    }
  }
  if (fs.existsSync(path.join(root, contractPath))) {
    const contract = readJson(contractPath);
    if (
      contract.workspace?.profile !== fixture.profile ||
      contract.workspace?.name !== fixture.name ||
      contract.projects?.length !== 0
    ) {
      failures.push(`Raw profile contract drift: ${workspaceRoot}`);
    }
  }

  const fixtureGitignore = path.join(root, workspaceRoot, '.gitignore');
  if (
    fs.existsSync(fixtureGitignore) &&
    fs
      .readFileSync(fixtureGitignore, 'utf8')
      .split(/\r?\n/)
      .includes('.workspai-workspace')
  ) {
    failures.push(`Canonical marker must remain trackable: ${workspaceRoot}`);
  }
}

const onboardingPath = path.join(root, 'WORKSPACE_ONBOARDING.md');
if (fs.existsSync(onboardingPath)) {
  const onboarding = fs.readFileSync(onboardingPath, 'utf8');
  if (!onboarding.includes('## Choose your path')) {
    failures.push('Workspace onboarding guide lacks audience-based navigation.');
  }
  const requiredOnboardingCommands = [
    'npx workspai workspace foundation ensure',
    'npx workspai import ../existing-project --workspace . --json',
    'npx workspai adopt ../existing-project --workspace . --dry-run --json',
    'npx workspai workspace model --json --write',
    'npx workspai workspace snapshot --json',
    'npx workspai workspace diff',
    'npx workspai workspace impact',
    'npx workspai doctor workspace --json',
    'npx workspai analyze --json --strict',
    'npx workspai workspace contract verify --strict --json',
    'npx workspai readiness --json',
    'npx workspai workspace verify',
    'npx workspai workspace context --for-agent --json --write --no-agent-sync',
    'npx workspai workspace agent-sync --write --json --preset enterprise',
    'npx workspai workspace explain release-blocked --json --write',
    'npx workspai pipeline --json --strict',
  ];
  for (const command of requiredOnboardingCommands) {
    if (!onboarding.includes(command)) {
      failures.push(`Workspace onboarding guide lacks command: ${command}`);
    }
  }

  const requiredAgentOutputs = [
    '.workspai/reports/workspace-context-agent.json',
    '.workspai/reports/INDEX.json',
    '.workspai/reports/agent-customization-pack.json',
    '.workspai/reports/workspace-skills-index.json',
    '.workspai/skills/*.md',
    'AGENTS.md',
    '.workspai/AGENT-GROUNDING.md',
  ];
  for (const output of requiredAgentOutputs) {
    if (!onboarding.includes(output)) {
      failures.push(`Workspace onboarding guide lacks agent output: ${output}`);
    }
  }
}

for (const relativePath of portableFiles) {
  const absolutePath = path.join(root, relativePath);
  if (!fs.existsSync(absolutePath) || fs.statSync(absolutePath).isDirectory()) continue;
  const content = fs.readFileSync(absolutePath, 'utf8');
  if (/\/(?:home|Users)\/|[A-Za-z]:\\/.test(content)) {
    failures.push(`Machine-local absolute path in portable file: ${relativePath}`);
  }
}

for (const showcase of index.proShowcases) {
  requireFile(`${showcase.path}/README.md`);
  for (const marker of ['.workspai-workspace', '.rapidkit-workspace']) {
    if (fs.existsSync(path.join(root, showcase.path, marker))) {
      failures.push(`Showcase-only directory must not claim workspace identity: ${showcase.path}`);
    }
  }
}

const requiredIgnoreRules = [
  '**/.workspai/reports/',
  '**/.workspai/workspace-registry.v1.json',
  '**/.workspai/imported-projects.json',
  '**/.workspai/adopt.json',
  '**/.workspai/adopt-readiness.json',
];
const gitignore = fs.readFileSync(path.join(root, '.gitignore'), 'utf8');
for (const rule of requiredIgnoreRules) {
  if (!gitignore.split(/\r?\n/).includes(rule)) {
    failures.push(`Missing machine-local artifact ignore rule: ${rule}`);
  }
}

function collectMarkdown(directory, relativeDirectory = '') {
  const docs = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    const relativePath = path.join(relativeDirectory, entry.name);
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) docs.push(...collectMarkdown(absolutePath, relativePath));
    else if (entry.name.endsWith('.md')) docs.push(relativePath);
  }
  return docs;
}

const docs = collectMarkdown(root);
const stalePatterns = [
  { pattern: /\bnpx rapidkit\b/, label: 'legacy npm command' },
  { pattern: /npmjs\.com\/package\/rapidkit(?:\b|\/)/, label: 'legacy npm package link' },
  { pattern: /github\.com\/rapidkitlabs\/rapidkit-npm(?:\b|\/)/, label: 'legacy CLI repository link' },
  { pattern: /docs\.getrapidkit\.com/, label: 'retired documentation host' },
  { pattern: /RapidKit CLI/, label: 'legacy CLI naming' },
  { pattern: /Health:\s*100%/, label: 'non-evidence health claim' },
  { pattern: /\(TODO\)/, label: 'unscoped TODO presented in public documentation' },
  {
    pattern: /Production-ready API in 5 minutes/,
    label: 'unqualified production-readiness claim',
  },
];
for (const relativePath of docs) {
  const content = fs.readFileSync(path.join(root, relativePath), 'utf8');
  for (const { pattern, label } of stalePatterns) {
    if (pattern.test(content)) failures.push(`${label} in ${relativePath}`);
  }

  for (const match of content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const rawTarget = match[1].trim().replace(/^<|>$/g, '');
    if (!rawTarget || /^(?:https?:|mailto:|#)/.test(rawTarget)) continue;
    const targetWithoutFragment = rawTarget.split('#', 1)[0];
    if (!targetWithoutFragment) continue;
    const resolved = path.resolve(
      root,
      path.dirname(relativePath),
      decodeURIComponent(targetWithoutFragment)
    );
    if (!fs.existsSync(resolved)) {
      failures.push(`Broken local link in ${relativePath}: ${rawTarget}`);
    }
  }
}

function collectPublicSourceFiles(directory, relativeDirectory = '') {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (
      entry.name === '.git' ||
      entry.name === 'node_modules' ||
      entry.name === '.venv' ||
      entry.name === '.rapidkit'
    ) {
      continue;
    }
    const relativePath = path.join(relativeDirectory, entry.name);
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...collectPublicSourceFiles(absolutePath, relativePath));
    else files.push(relativePath);
  }
  return files;
}

for (const relativePath of collectPublicSourceFiles(root)) {
  const baseName = path.basename(relativePath);
  if (baseName === '.env.local' || baseName === '.env.backup') {
    failures.push(`Machine-local environment artifact must not be published: ${relativePath}`);
    continue;
  }
  if (baseName === '.env' || /\.(?:pem|key|p12|pfx)$/.test(baseName)) {
    failures.push(`Secret-bearing file type must not be published: ${relativePath}`);
    continue;
  }
  if (!/\.(?:ts|js|mjs|cjs)$/.test(relativePath)) continue;
  const content = fs.readFileSync(path.join(root, relativePath), 'utf8');
  if (/SECRET_KEY:\s*process\.env\.SECRET_KEY\s*\?\?\s*['"][A-Za-z0-9]{24,}['"]/.test(content)) {
    failures.push(`Secret-looking hardcoded fallback in ${relativePath}`);
  }
}

if (failures.length > 0) {
  console.error('[examples] Validation failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  `[examples] ${published.length} project workspaces, ${profileFixtures.length} raw profile workspaces, ${published.reduce((sum, workspace) => sum + workspace.projects.length, 0)} projects, contracts and publication boundaries verified.`
);
