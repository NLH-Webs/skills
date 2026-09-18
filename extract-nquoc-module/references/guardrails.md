# Guardrails

> **Kit update (2026-09-16):** do not copy `nquoc-it/eslint.config.js` any more — a
> repo created from `nquoc-module-template` already has the whole config, and it
> derives the module list from `src/modules/*` instead of a hardcoded array. It
> also bans raw `fetch`/`XMLHttpRequest` outside the api layers and confines
> `@supabase/*` to `src/infrastructure/supabase`. Change rules in the template
> first, then `pnpm kit:sync`. See `kit.md`. The rest of this file explains why
> each rule exists and how to prove it fires — still worth reading.

Copy `nquoc-it/eslint.config.js` and change the module names. This file
explains what each rule is for and — more importantly — how each one failed
before it worked.

**Every rule here was wrong at least once.** Two silently matched nothing.
Run the probes.

## The rules

### 1. Layering — `import/no-restricted-paths`

Not `no-restricted-imports`. The difference matters: `no-restricted-imports`
pattern-matches the **text** of the specifier, so it misses
`../other-module/internals` entirely and cannot tell a module importing its
own files from one reaching into a sibling. `import/no-restricted-paths`
resolves imports to real files.

Zones:

| target | must not import | why |
| --- | --- | --- |
| `src/modules`, `src/app`, `src/shared` | `src/infrastructure/supabase` | business code never learns the provider |
| `src/app` | `src/modules` except each module's `index.ts` | modules are entered through their public API |
| `src/modules/<a>` | `src/modules` except its own files and other modules' `index.ts` | no deep cross-module imports |
| `src/shared` | `src/modules`, `src/app` | lower layers never depend upwards |
| `src/infrastructure` | `src/modules`, `src/app` | same |

Keep a `MODULE_PUBLIC_APIS` array listing each module's `index.ts`. Adding a
module means adding a line — deliberately, so the registry is written down.

### 2. API layer — `no-restricted-imports` + `no-restricted-syntax`

Only `modules/*/api/**`, `shared/api/**` and `infrastructure/**` may import the
API client. Components, hooks and pages go through a module api layer, so every
backend call has one reviewable home and the contract has one binding point.

**The exemption needs a second rule.** An exempt api file can re-export the
client, and a component can import *that* — `no-restricted-imports` only ever
inspects the direct specifier, so the chain is invisible. A reviewer found this
on N-IT after the rule shipped:

```js
// in an exempt api/ file — a one-line hole through the boundary
export { default as apiClient } from '@/infrastructure/api/api-client';
```

So api directories also get:

```js
'no-restricted-syntax': ['error',
  { selector: 'ExportNamedDeclaration[source.value=/api-client/]',
    message: 'Do not re-export the API client.' },
  { selector: 'ExportAllDeclaration[source.value=/api-client/]',
    message: 'Do not re-export the API client.' },
],
```

### 3. Config boundary — `no-restricted-syntax`, not `no-restricted-properties`

`import.meta` parses as a `MetaProperty`, **not** a `MemberExpression` on an
identifier named `import`. `no-restricted-properties` with
`{ object: 'import', property: 'meta' }` therefore matches nothing, ever. It
looked right and protected nothing for three commits.

```js
'no-restricted-syntax': ['error', {
  selector: 'MetaProperty[meta.name="import"][property.name="meta"]',
  message: 'Read configuration from @/infrastructure/config/env.',
}],
```

Exempt `infrastructure/config/*`, `infrastructure/supabase/*`, `vite-env.d.ts`.

## Flat config replaces, it does not merge

A later block that names the same rule **replaces** the earlier value. On N-IT
an `src/app/**` override redefined `no-restricted-imports` with only the
Supabase pattern, silently disabling the module-boundary check in the one layer
whose whole job is composing modules.

If a block overrides a rule, it must restate everything that rule was doing.

## Probes — run these, do not assume

Write each file, run `pnpm exec eslint` on it, confirm the expected result, delete it.

**The import target must actually resolve.** `import/no-restricted-paths`
resolves specifiers to real files, so a probe pointing at a path that does not
exist reports nothing and looks like a passing rule — indistinguishable from a
rule that works. Create the target file too, or point the probe at something
real.

| probe | where | expected |
| --- | --- | --- |
| `import { getSupabaseClient } from '@/infrastructure/supabase/client'` | `src/modules/<m>/` | FAIL |
| `import { X } from '../other/internals'` | `src/modules/<m>/` | FAIL — relative must be caught |
| `import { X } from '@/modules/<m>/routes'` | `src/modules/<m>/` | **PASS** — own module |
| `import X from '@/modules/<m>/pages/Y'` | `src/app/` | FAIL |
| `import { X } from '@/modules/<m>'` | `src/shared/` | FAIL — no upward deps |
| `import apiClient from '@/infrastructure/api/api-client'` | `src/modules/<m>/` | FAIL |
| same | `src/modules/<m>/api/` | **PASS** |
| `import apiClient from '../../../infrastructure/api/api-client'` | `src/modules/<m>/` | FAIL |
| `export { default as apiClient } from '@/infrastructure/api/api-client'` | `src/shared/api/` | FAIL |
| `import.meta.env.MODE` | `src/modules/<m>/` | FAIL |
| same | `src/infrastructure/config/env.ts` | **PASS** |

A rule that has not been probed is a comment.

## What lint will not catch

Do not assume a green build means a clean migration:

- **hardcoded absolute routes** — they are strings; grep for them
- **a store nobody writes to** — N-IT's release editor read an owner id from a
  store whose only writer stayed in the monolith, so every image upload
  silently no-opped behind `if (!profileId) return`
- **request body shapes** — a path can match the backend while the body does
  not; the contract checker validates paths and methods only
- **anything lost with the chrome** — no file changed, so nothing reports it
- **links that leave the module** — they need `embedBridge.open`, lint cannot tell
- **`embed-protocol.ts` drift** — diff it against nquoc-user's; a changed message
  shape breaks silently at runtime

And holes the N-Design senior review proved with probes, still open in the
copied config — check by hand until the shared lint preset closes them:

- raw `fetch(...)`, `window.fetch`, `new XMLHttpRequest` in a module
- `import { createClient } from '@supabase/supabase-js'` directly in a repo that
  still keeps Supabase for Storage (nquoc-it; nquoc-design bans `@supabase/*`
  outright)
- a new folder such as `src/lib/` that re-exports the Supabase client or api client
- api files that re-export the client without `from`
- `import.meta.env` inside `infrastructure/**`, `shared/api/**` and module
  `api/**`, where an override *replaces* the rule
- the contract checker misses a renamed client import (`http.get`) and does not
  scan `shared/api` or the shell's own endpoints
- the smoke test only catches a localhost API / localhost parent; a build with
  the wrong environment's values still passes — check the bundle

## Git-flow hooks

Copy `.husky/pre-commit` and `.husky/pre-push` from nquoc-it (byte-identical to
nquoc-user and nquoc-backend). pre-commit refuses a commit while HEAD is `dev`
or `main`; pre-push refuses any push whose remote ref is `dev` or `main`,
including `git push origin HEAD:dev`.

**Install them, do not just copy them.** nquoc-user ships the files with no
husky dependency and no `prepare` script, so they never run on a fresh clone:

```json
"scripts":         { "prepare": "husky || true" },
"devDependencies": { "husky": "^9.1.7" }
```

After `pnpm install`, `git config --get core.hooksPath` must print `.husky/_`.

### Proving the hooks fire

Test in a throwaway repo with a bare remote. **Do not test by checking out
`dev` in the real repo**: `dev` does not contain `.husky/` until the guard PR
merges, so the hooks vanish on checkout and a commit slips through — which
looks exactly like a broken hook. (`git stash -u` has the same effect, since it
stashes the untracked `.husky/` directory.) That mistake was made on N-IT and
left a probe commit on local `dev` that had to be removed.

```bash
git init -q --bare /tmp/remote.git && git init -q /tmp/hooktest && cd /tmp/hooktest
cp -r <REPO>/.husky . && git config core.hooksPath .husky/_
git remote add origin /tmp/remote.git
git checkout -b feat/x && git commit --allow-empty -m ok        # must PASS
git checkout -b dev    && git commit --allow-empty -m no        # must be BLOCKED
git checkout feat/x    && git push origin feat/x:dev            # must be BLOCKED
git push origin feat/x                                          # must PASS
```

Hooks catch honest mistakes. The real guard is GitHub branch protection on
`dev` and `main` — ask a repo admin to enable it.

## Checks to wire

```json
"typecheck":       "tsc -p tsconfig.app.json --noEmit",
"lint":            "eslint .",
"contract:check":  "node scripts/openapi-contract-check.mjs --check",
"test":            "node --test scripts/tests/*.test.mjs",
"verify":          "pnpm run typecheck && pnpm run lint && pnpm run test && pnpm run contract:check && pnpm run build"
```

`nquoc-user` has no typecheck script and `vite build` does not type-check —
which is how a `ReferenceError` in N-IT's archive and delete buttons survived
in production until the extraction ran `tsc` over the same code. Wire
`verify` into CI from the first commit.
