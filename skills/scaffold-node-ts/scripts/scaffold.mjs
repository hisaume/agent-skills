import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, lstatSync } from 'node:fs';
import { resolve, dirname, basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const required = ['@eslint/js', '@types/node', 'eslint', 'eslint-config-prettier', 'globals', 'prettier', 'tsx', 'typescript', 'typescript-eslint', 'vitest'];
const versionPattern = /^\d+\.\d+\.\d+$/;
const assets = resolve(dirname(fileURLToPath(import.meta.url)), '../assets');
function fail(message) { throw new Error(message); }
function files(directory, prefix = '') {
  return readdirSync(directory).sort().flatMap(name => {
    const relative = join(prefix, name);
    return lstatSync(join(directory, name)).isDirectory() ? files(join(directory, name), relative) : [relative];
  });
}
try {
  const [mode, targetArg, inputsArg] = process.argv.slice(2);
  if (!['create', 'verify'].includes(mode) || !targetArg || !inputsArg || process.argv.length !== 5)
    fail('Usage: node scaffold.mjs <create|verify> <existing-directory> <inputs.json>');
  const target = resolve(targetArg);
  if (!lstatSync(target).isDirectory()) fail('Target must be an existing directory');
  const inputs = JSON.parse(readFileSync(resolve(inputsArg), 'utf8'));
  if (Object.keys(inputs).sort().join(',') !== 'dependencies,node,pnpm') fail('Inputs must contain only node, pnpm, and dependencies');
  const node = String(inputs.node).replace(/^v/, '');
  if (!versionPattern.test(node) || !versionPattern.test(inputs.pnpm)) fail('Node and pnpm must be exact stable versions');
  if (!process.release.lts) fail('Run the script on an installed Node LTS');
  if (process.versions.node !== node) fail('Run the script using the selected Node version through nvm');
  const major = Number(node.split('.')[0]);
  const targets = {20: 'ES2023', 22: 'ES2023', 24: 'ES2024'};
  if (!targets[major]) fail(`Node ${major} needs an explicit compiler baseline before scaffolding`);
  const [pnpmMajor, pnpmMinor] = inputs.pnpm.split('.').map(Number);
  if (pnpmMajor < 10) fail('This baseline requires pnpm 10 or newer; do not upgrade automatically');
  if (Object.keys(inputs.dependencies).sort().join(',') !== required.join(',')) fail('Provide exactly the required development dependencies');
  for (const [name, version] of Object.entries(inputs.dependencies))
    if (!versionPattern.test(version)) fail(`Use an exact stable version for ${name}`);
  if (Number(inputs.dependencies['@types/node'].split('.')[0]) !== major) fail('@types/node major must match Node');
  const name = basename(target).toLowerCase().replace(/[ _]+/g, '-').replace(/[^a-z0-9-]/g, '').replace(/-+/g, '-').replace(/^-+|-+$/g, '') || 'node-ts-app';
  const output = new Map(files(assets).map(file => [file, readFileSync(join(assets, file), 'utf8')]));
  const pkg = JSON.parse(output.get('package.json'));
  output.set('package.json', JSON.stringify({name, ...pkg, packageManager: `pnpm@${inputs.pnpm}`, engines: {node: `${major}.x`}, devDependencies: Object.fromEntries(required.map(key => [key, inputs.dependencies[key]]))}, null, 2) + '\n');
  const ts = JSON.parse(output.get('tsconfig.json')); ts.compilerOptions.target = targets[major];
  output.set('tsconfig.json', JSON.stringify(ts, null, 2) + '\n');
  output.set('.nvmrc', `v${node}\n`);
  output.set('pnpm-workspace.yaml', pnpmMajor > 10 || pnpmMinor >= 26 ? 'allowBuilds:\n  esbuild: true\n' : 'onlyBuiltDependencies:\n  - esbuild\n');
  if (mode === 'create') {
    for (const file of output.keys()) {
      const parts = file.split('/');
      for (let i = 1; i <= parts.length; i++) {
        const path = join(target, ...parts.slice(0, i));
        try {
          const stat = lstatSync(path);
          if (stat.isSymbolicLink() || i === parts.length || !stat.isDirectory()) fail(`Refusing existing file or unsafe path: ${path}`);
        } catch (error) { if (error.code !== 'ENOENT') throw error; }
      }
    }
    for (const [file, content] of output) {
      const path = join(target, file); mkdirSync(dirname(path), {recursive: true}); writeFileSync(path, content, {flag: 'wx'});
    }
  } else {
    for (const [file, content] of output) {
      const path = join(target, file);
      if (!existsSync(path)) fail(`Missing baseline file: ${file}`);
      const actual = readFileSync(path, 'utf8');
      if (file.endsWith('.json')) {
        const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
        if (JSON.stringify(canonical(JSON.parse(actual))) !== JSON.stringify(canonical(JSON.parse(content)))) fail(`Baseline changed: ${file}`);
      } else if (actual !== content) fail(`Baseline changed: ${file}`);
    }
  }
  console.log(`${mode}: baseline ${mode === 'create' ? 'created' : 'verified'} for ${name}`);
} catch (error) { console.error(error.message); process.exitCode = 1; }
