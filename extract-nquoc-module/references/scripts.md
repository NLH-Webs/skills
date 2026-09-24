# Scripts

> **Kit update (2026-09-16):** scaffolding scripts are no longer needed — create
> the repo from `nquoc-module-template` (`kit.md`). The closure/migration/drift
> scripts below are still the right tool for moving a module's code out of
> nquoc-user, and the reachability idea is what Phase 7 uses to find legacy files
> that are safe to delete (normalise Windows backslashes when comparing paths).

**These scripts are deleted after each migration** (Phase 4 step 7 removes them),
so there is no committed copy to reuse — earlier revisions of this file pointed at
`nquoc-design/scripts/migration/` and `nquoc-it/scripts/migration/`, which no
longer exist. Rewrite `closure.cjs`, `migrate.cjs`, `build-public-api.cjs`,
`drift.cjs`, `reachability.cjs` from the sketches below (they are complete enough
to run once the constants at the top point at your module); the sketches also
explain where each one goes wrong.

They hardcode the workspace root and the target repo in constants at the top —
the N-Design copies still say `C:/Projects/Nquoc` and name a variable `IT`.
Point every constant at the new module before running, and check the machine's
real workspace path (it is not the same on every machine).

**Auditing an extraction without its `filemap.json`:** use
`scripts/drift-by-basename.cjs` bundled with this skill. It matches each file in
the target repo's `src/modules` and `src/shared` to the legacy file with the
same name on `nquoc-user origin/dev`, strips imports, and lists what differs:

```bash
node .claude/skills/extract-nquoc-module/scripts/drift-by-basename.cjs --user nquoc-user --target nquoc-design --map modules/design/design-workspace.tsx=src/pages/DesignTeam/Index.tsx
```

Renamed files need a `--map`. A `DIFF` whose source is an unrelated file of the
same name (`index.ts`, `utils.ts`) is a false match — read it, don't count it.

**On Windows Git Bash, `export MSYS_NO_PATHCONV=1` before any `git show
<branch>:<path>`.** Otherwise Git Bash rewrites `origin/dev:.husky/pre-commit`
into a Windows path and git reports an "ambiguous argument".

Run from the workspace root (`C:/Projects/Nquoc`). Replace `<MODULE>` with the
module's folder in `nquoc-user/src/pages/`, and `<REPO>` with the target repo.

## 1. Transitive closure — run this before promising a scope

Follows every `@/` and relative import from the module's folder, so you learn
the real cost rather than the folder's size.

```js
// closure.cjs
const fs = require('fs'), path = require('path');
const SRC = 'C:/Projects/Nquoc/nquoc-user/src';
const ENTRY = 'pages/<MODULE>';          // e.g. pages/DesignTeam
const OUT = process.env.SCRATCH || '.';

const resolve = (spec) => {
  if (!spec.startsWith('@/')) return null;
  const base = path.join(SRC, spec.slice(2));
  for (const c of ['.tsx', '.ts', '/index.tsx', '/index.ts', '.css', ''])
    if (fs.existsSync(base + c) && fs.statSync(base + c).isFile()) return base + c;
  return null;
};

const importsOf = (file) => {
  let src; try { src = fs.readFileSync(file, 'utf8'); } catch { return []; }
  const out = [];
  const re = /from\s+['"]([^'"]+)['"]|import\s+['"]([^'"]+)['"]/g;
  let m;
  while ((m = re.exec(src))) {
    const spec = m[1] || m[2];
    if (spec.startsWith('@/')) out.push(spec);
    else if (spec.startsWith('.')) {
      const abs = path.resolve(path.dirname(file), spec);
      out.push('@/' + path.relative(SRC, abs).split(path.sep).join('/'));
    }
  }
  return out;
};

const seed = fs.readdirSync(path.join(SRC, ENTRY)).map((f) => path.join(SRC, ENTRY, f));
const seen = new Set(seed.map((f) => path.relative(SRC, f).split(path.sep).join('/')));
const queue = [...seed];
while (queue.length) {
  for (const spec of importsOf(queue.shift())) {
    const r = resolve(spec);
    if (!r) continue;
    const rel = path.relative(SRC, r).split(path.sep).join('/');
    if (!seen.has(rel)) { seen.add(rel); queue.push(r); }
  }
}

const all = [...seen].sort();
const owned = all.filter((f) => f.startsWith(ENTRY + '/'));
let loc = 0;
for (const f of all) { try { loc += fs.readFileSync(path.join(SRC, f), 'utf8').split('\n').length; } catch {} }

console.log('owned:', owned.length, ' pulled in:', all.length - owned.length, ' total lines:', loc);
const byArea = {};
all.filter((f) => !f.startsWith(ENTRY + '/'))
   .forEach((f) => (byArea[f.split('/').slice(0, 2).join('/')] ||= []).push(f));
Object.entries(byArea).sort((a, b) => b[1].length - a[1].length)
  .forEach(([k, v]) => console.log(String(v.length).padStart(4), k));
fs.writeFileSync(path.join(OUT, 'closure-files.txt'), all.join('\n'));
```

Then check how shared each pulled-in area is — this decides COPY vs KEEP:

```bash
for d in order-composer order-detail order-rounds order-report deadline-calendar; do
  echo -n "$d -> "
  grep -rl "@/components/$d/" --include=*.tsx --include=*.ts nquoc-user/src/ \
    | grep -v "^nquoc-user/src/components/$d/" \
    | sed 's|.*/pages/\([^/]*\)/.*|\1|' | sort -u | tr '\n' ' '
  echo
done
```

## 2. Migration

Maps every file and rewrites every import in one pass. **Adjust `RULES` for
the module**, and confirm you are reading the right branch first.

```js
// migrate.cjs — working version: nquoc-it/scripts/migration/migrate.cjs
const RULES = [
  [/^pages\/<MODULE>\/(.+)$/,                 (m) => `modules/<name>/${m[1]}`],
  [/^components\/(order-[a-z]+)\/(.+)$/,      (m) => `modules/order/components/${m[1]}/${m[2]}`],
  [/^api\/(orders|teamDocuments)\.ts$/,       (m) => `modules/order/api/${m[1]}.ts`],
  [/^components\/ui\/(.+)$/,                  (m) => `shared/components/ui/${m[1]}`],
  [/^components\/(.+)$/,                      (m) => `shared/components/${m[1]}`],
  [/^hooks\/(.+)$/,                           (m) => `shared/hooks/${m[1]}`],
  [/^utils\/(.+)$/,                           (m) => `shared/utils/${m[1]}`],
  [/^lib\/(.+)$/,                             (m) => `shared/lib/${m[1]}`],
  [/^api\/(.+)$/,                             (m) => `shared/api/${m[1]}`],
];

// Never copy these — the new repo has its own:
const SKIP = new Set([
  'contexts/AuthContext.tsx', 'hooks/useProfileQueries.ts',
  'lib/api-client.ts',
  'lib/logoutUtils.ts', 'lib/utils.ts', 'stores/teamContextStore.ts',
  'api/userTeams.ts', 'index.css',
]);

const REDIRECTS = new Map([
  ['@/contexts/AuthContext',           '@/infrastructure/auth'],
  ['@/lib/api-client',                 '@/infrastructure/api/api-client'],
  ['@/lib/utils',                      '@/shared/lib/utils'],
]);
```

Normalise relative imports to `@/` **first**, then rewrite through one map —
otherwise relative imports silently keep pointing at the old layout.

Report every specifier it could not resolve. On N-IT that list was empty; a
non-empty list means the mapping is incomplete, not that the file is fine.

## 3. Drift check — run this before you call the migration done

Catches the "migrated from the wrong branch" failure. On N-IT this found 16
files, including an API signature change that would have been silently
reverted.

```js
// drift.cjs
const { execSync } = require('child_process');
const strip = (t) => t.split(/\r?\n/)
  .filter((l) => !/from\s+['"]/.test(l) && !/^\s*import\s+['"]/.test(l))
  .map((l) => l.replace(/\s+$/, '')).join('\n').trim();

for (const [srcRel, dstRel] of Object.entries(filemap)) {
  const target = `<REPO>/src/${dstRel}`;
  if (!fs.existsSync(target)) continue;            // deliberately deleted
  const dev = execSync(`git -C nquoc-user show dev:src/${srcRel}`, { encoding: 'utf8' });
  if (strip(dev) !== strip(fs.readFileSync(target, 'utf8'))) console.log('DRIFT', srcRel);
}
```

Every reported file is either a change you made deliberately — and can name —
or work from `dev` you are about to lose.

Also check the reverse: recompute the closure on `dev` and diff the file lists.
New files there are dependencies the module gained since your branch.

## 4. Reachability — run before opening the PR

```js
// reach.cjs — walk imports from src/main.tsx, then list everything unvisited
```

Anything unreachable is dead. On N-IT this found 14 files: a store whose only
writer was left behind, a util pulled in by a file that was never migrated,
three components already dead in the monolith, and nine speculatively-copied
shadcn primitives. Delete them; `components.json` means shadcn can re-add any
primitive in one command.

## 5. Hardcoded routes

```bash
grep -rn "navigate('/\|navigate(\`/\|window.location.href\s*=\|href=\"/" <REPO>/src/modules
```

The module is served at its own domain root, so paths inside it are root-relative:
`navigate('/')`, not `navigate('/n-task')`. A link to another N-Quốc page
(`/dashboard`, `/n-doc/…`) must be `embedBridge.open(href)`, or it opens inside the
iframe. Nothing in the toolchain catches this — they are strings.

## 6. Migration gotchas learned on N-Edit

- **Bun/pnpm may not be installed.** `npx -y pnpm@10.10.0 …`; backend `npx -y bun@<pinned> …`.
- **`Index.tsx` collides with `index.ts`** in the same module folder on
  Windows/macOS (`error TS1149 … differs only in casing`). Rename the page file
  (`edit-team-page.tsx`) and update its route import.
- **Copied order/shared drag npm deps** the template lacks — `@tiptap/*`,
  `recharts`, `date-fns`, `@radix-ui/react-{avatar,dropdown-menu,hover-card,popover,select}`.
  `pnpm typecheck` lists them; add from the donor repo's `package.json` versions.
- **`apiClient` path shape decides `contract:check`.** The checker resolves a
  file-local `const X = 'edit'` to the literal (so `/orders/${X}/…` becomes
  `/orders/edit/…` and fails to match `/orders/{teamKey}/…`), but does **not**
  resolve `const X = 'edit' as const` — use `as const` for a module-fixed team
  key. And it cannot see inside a helper: a `const base = (k)=>\`/x/${k}\`` call
  collapses to one opaque `${base(k)}` segment that never validates and whose
  approved-gap never self-detects as stale — **write the path literally**
  (`/team-documents/${teamKey}`), `${param}` matching `{param}`.
- **Approved gaps are stale once the endpoint deploys.** Re-run
  `contract:refresh` + `contract:check` after the backend reaches staging;
  remove gaps for endpoints now in the snapshot. Match the checker's key format
  exactly (it prints the normalized path it looked for).
- **Reachability only works after trimming the barrel.** `modules/order/index.ts`
  re-exports everything, so an import-graph walk from `main.tsx` reaches all of
  it. Trim `index.ts` to the exact names the module imports first, then the walk
  reveals the genuinely dead files. A tiny walker: BFS `from '…'` / `import '…'`
  / `import('…')` specifiers from `src/main.tsx`, list files under
  `src/modules/<domain>` + `src/shared` not visited (normalise Windows `\`).
  Note the barrel itself can show as a false-positive; the components it
  re-exports being reached proves it is reached.
