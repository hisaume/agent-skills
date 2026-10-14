import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, symlinkSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const script = new URL('../scripts/scaffold.mjs', import.meta.url);
const versions = {'@eslint/js': '10.0.1', '@types/node': `${process.versions.node.split('.')[0]}.0.0`, eslint: '10.12.0', 'eslint-config-prettier': '10.1.8', globals: '17.13.0', prettier: '3.9.10', tsx: '4.23.15', typescript: '6.0.3', 'typescript-eslint': '8.71.2', vitest: '5.0.4'};
function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), 'scaffold-test-'));
  t.after(() => rmSync(root, {recursive: true, force: true}));
  const target = join(root, 'My_App'); mkdirSync(target);
  const inputs = join(root, 'inputs.json');
  const data = {node: process.versions.node, pnpm: '11.21.0', dependencies: {...versions}};
  writeFileSync(inputs, JSON.stringify(data));
  return {target, inputs, data, run: mode => spawnSync(process.execPath, [script.pathname, mode, target, inputs], {encoding: 'utf8'})};
}
test('canonical generation and verification; detects configuration drift', t => {
  const f = fixture(t); assert.equal(f.run('create').status, 0); assert.equal(f.run('verify').status, 0);
  assert.equal(JSON.parse(readFileSync(join(f.target, 'package.json'))).name, 'my-app');
  const path = join(f.target, 'tsconfig.json');const config = JSON.parse(readFileSync(path));config.compilerOptions.strict = false;writeFileSync(path, JSON.stringify(config));
  assert.equal(f.run('verify').status, 1);
});
test('existing destination prevents all writes and preserves content', t => {
  const f = fixture(t);mkdirSync(join(f.target, 'src'));writeFileSync(join(f.target, 'src/index.ts'), 'preserve');
  assert.equal(f.run('create').status, 1);assert.deepEqual(readdirSync(f.target), ['src']);assert.equal(readFileSync(join(f.target, 'src/index.ts'), 'utf8'), 'preserve');
});
test('symlink destination prevents generation', t => {
  const f = fixture(t);symlinkSync(tmpdir(), join(f.target, 'src'), 'dir');assert.equal(f.run('create').status, 1);assert.deepEqual(readdirSync(f.target), ['src']);
});
test('Node types mismatch prevents generation', t => {
  const f = fixture(t);f.data.dependencies['@types/node'] = '99.0.0';writeFileSync(f.inputs, JSON.stringify(f.data));assert.equal(f.run('create').status, 1);assert.deepEqual(readdirSync(f.target), []);
});
test('legacy pnpm 10 uses its supported approval setting', t => {
  const f = fixture(t);f.data.pnpm = '10.25.0';writeFileSync(f.inputs, JSON.stringify(f.data));assert.equal(f.run('create').status, 0);assert.equal(readFileSync(join(f.target, 'pnpm-workspace.yaml'), 'utf8'), 'onlyBuiltDependencies:\n  - esbuild\n');
});
