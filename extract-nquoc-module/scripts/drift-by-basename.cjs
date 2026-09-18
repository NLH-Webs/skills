#!/usr/bin/env node
/**
 * Drift check for an extracted module when the migration's filemap.json is
 * missing: match every file under <target>/src/modules and <target>/src/shared
 * to the legacy file with the same basename on nquoc-user origin/dev, strip
 * import/export-from lines and CRLF, and report which differ.
 *
 *   node drift-by-basename.cjs --user nquoc-user --target nquoc-design \
 *     [--ref origin/dev] [--map modules/design/design-workspace.tsx=src/pages/DesignTeam/Index.tsx ...]
 *
 * Run from the workspace root after `git -C nquoc-user fetch origin`.
 * Each DIFF must be a change you can name; a DIFF against an unrelated file of
 * the same name (index.ts, utils.ts) is a false match.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : fallback;
};
const USER = path.resolve(opt('user', 'nquoc-user'));
const TARGET = path.resolve(opt('target', ''), 'src');
const REF = opt('ref', 'origin/dev');
const special = Object.fromEntries(
  args.flatMap((a, i) => (args[i - 1] === '--map' ? [a.split('=')] : [])),
);

if (!fs.existsSync(TARGET)) {
  console.error('Usage: drift-by-basename.cjs --user <nquoc-user> --target <module repo> [--ref origin/dev] [--map new=old]');
  process.exit(2);
}

const git = (cmd) => execSync(`git -C "${USER}" ${cmd}`, { encoding: 'utf8', maxBuffer: 5e7 });
const legacyFiles = git(`ls-tree -r --name-only ${REF} -- src`).split('\n').filter(Boolean);
const byBase = {};
for (const f of legacyFiles) (byBase[path.basename(f).toLowerCase()] ??= []).push(f);

const normalise = (t) =>
  t
    .replace(/\r/g, '')
    .replace(/^\s*import\s[\s\S]*?from\s+['"][^'"]+['"];?/gm, '')
    .replace(/^\s*import\s+['"][^'"]+['"];?/gm, '')
    .replace(/^\s*export\s+(\*|\{[\s\S]*?\})\s+from\s+['"][^'"]+['"];?/gm, '')
    .split('\n')
    .map((l) => l.trimEnd())
    .filter((l) => l.trim())
    .join('\n');

const walk = (d) =>
  fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)],
  );

const same = [];
const diff = [];
const noSource = [];

for (const abs of walk(TARGET)) {
  const rel = path.relative(TARGET, abs).split(path.sep).join('/');
  if (!/^(modules|shared)\//.test(rel)) continue;
  const candidates = special[rel] ? [special[rel]] : byBase[path.basename(rel).toLowerCase()] || [];
  if (!candidates.length) {
    noSource.push(rel);
    continue;
  }
  const mine = normalise(fs.readFileSync(abs, 'utf8'));
  let best = null;
  for (const c of candidates) {
    const theirs = normalise(git(`show "${REF}:${c}"`));
    if (theirs === mine) {
      best = { src: c, d: 0 };
      break;
    }
    const a = new Set(theirs.split('\n'));
    const b = mine.split('\n');
    const removed = [...a].filter((x) => !b.includes(x)).length;
    const added = b.filter((x) => !a.has(x)).length;
    if (!best || removed + added < best.d) best = { src: c, d: removed + added, added, removed };
  }
  (best.d === 0 ? same : diff).push({ rel, ...best });
}

console.log(`identical: ${same.length}`);
console.log(`DIFF:      ${diff.length}`);
for (const x of diff) console.log(`  ${x.rel} <- ${x.src}  (+${x.added}/-${x.removed} lines)`);
console.log(`no legacy source (new files): ${noSource.length}`);
for (const f of noSource) console.log(`  ${f}`);
