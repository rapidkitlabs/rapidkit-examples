import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const root = process.cwd();
const args = process.argv.slice(2);
let workspaceArg;
const projectArgs = [];

for (let index = 0; index < args.length; index += 1) {
  if (args[index] === '--workspace') workspaceArg = args[++index];
  else if (args[index] === '--project') projectArgs.push(args[++index]);
  else throw new Error(`Unknown argument: ${args[index]}`);
}

if (!workspaceArg || projectArgs.length === 0) {
  throw new Error(
    'Usage: node scripts/hydrate-core-modules.mjs --workspace <path> --project <path> [--project <path>]'
  );
}

const workspace = path.resolve(root, workspaceArg);

function run(command, commandArgs, options = {}) {
  const result = spawnSync(command, commandArgs, {
    cwd: options.cwd ?? root,
    encoding: 'utf8',
    stdio: options.capture ? 'pipe' : 'inherit',
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    if (options.capture) {
      process.stderr.write(result.stdout ?? '');
      process.stderr.write(result.stderr ?? '');
    }
    throw new Error(`${command} exited with status ${result.status}`);
  }
  return (result.stdout ?? '').trim();
}

run('poetry', ['--directory', workspace, 'install', '--no-interaction']);
const environment = path.join(workspace, '.venv');
const rapidkit = path.join(
  environment,
  process.platform === 'win32' ? 'Scripts' : 'bin',
  process.platform === 'win32' ? 'rapidkit.exe' : 'rapidkit'
);

if (!fs.existsSync(rapidkit)) {
  throw new Error(`RapidKit executable not found after workspace install: ${rapidkit}`);
}

const aliases = new Map([
  ['free/auth/core', 'auth_core'],
  ['free/observability/core', 'observability_core'],
]);

for (const projectArg of projectArgs) {
  const project = path.resolve(workspace, projectArg);
  const registryPath = path.join(project, 'registry.json');
  if (!fs.existsSync(registryPath)) throw new Error(`Module registry not found: ${registryPath}`);

  const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
  const modules = registry.installed_modules ?? [];
  if (modules.length === 0) throw new Error(`No installed modules recorded in ${registryPath}`);

  const temporaryRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'rapidkit-hydrate-'));
  const temporaryProject = path.join(temporaryRoot, path.basename(project));
  try {
    fs.cpSync(project, temporaryProject, {
      recursive: true,
      filter: (source) => {
        const relative = path.relative(project, source);
        return !['.venv', 'node_modules', '.rapidkit/vendor'].some(
          (ignored) => relative === ignored || relative.startsWith(`${ignored}${path.sep}`)
        );
      },
    });

    console.log(`[hydrate] ${path.relative(root, project)}: ${modules.length} module(s)`);
    for (const module of modules) {
      if (!module.slug || !module.version) {
        throw new Error(`Invalid module registry entry in ${registryPath}`);
      }
      run(
        rapidkit,
        ['add', 'module', module.slug, '--update', '--with-deps', '--no-reconcile'],
        { cwd: temporaryProject }
      );

      const vendorName = aliases.get(module.slug) ?? module.slug.split('/').at(-1);
      const payload = path.join(
        temporaryProject,
        '.rapidkit',
        'vendor',
        vendorName,
        module.version
      );
      if (!fs.existsSync(payload)) {
        throw new Error(`Hydration did not produce ${module.slug}@${module.version}: ${payload}`);
      }
    }

    const restoredRegistry = path.join(temporaryProject, 'registry.json');
    const restored = JSON.parse(fs.readFileSync(restoredRegistry, 'utf8')).installed_modules ?? [];
    const expectedVersions = new Map(modules.map((module) => [module.slug, module.version]));
    for (const module of restored) {
      if (expectedVersions.get(module.slug) !== module.version) {
        throw new Error(
          `Hydration changed ${module.slug} from ${expectedVersions.get(module.slug)} to ${module.version}`
        );
      }
    }

    const generatedVendor = path.join(temporaryProject, '.rapidkit', 'vendor');
    const projectVendor = path.join(project, '.rapidkit', 'vendor');
    fs.rmSync(projectVendor, { recursive: true, force: true });
    fs.cpSync(generatedVendor, projectVendor, { recursive: true });
  } finally {
    fs.rmSync(temporaryRoot, { recursive: true, force: true });
  }
}

console.log('[hydrate] RapidKit Core module payloads restored from project registries.');
