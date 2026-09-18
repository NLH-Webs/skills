---
name: extract-nquoc-module
description: Extract an N-Quốc module (N-Task, N-Doc, Edit, Admin, HR, N-Lead, N-Chat, …) out of the nquoc-user monolith into its own frontend repo created from nquoc-module-template, that nquoc-user embeds in an iframe (nquoc.vn/n-<m>/*), isolate its backend module (repository, policy, OpenAPI) in the same wave, and roll it out to staging and production. Use when asked to extract, migrate, split out, or stand up a module as its own app — even when the user only says a module name ("tách N-Task", "/extract-nquoc-module task") — or to repeat what was done for N-IT / N-Design / N-Fit. Also use when auditing an extraction someone else did, when checking whether a module is ready, when deploying or cutting a module over on preview.nquoc.vn / nquoc.vn, when applying or syncing the module kit (kit:diff, kit:sync, nquoc-module-template), when touching nquoc-user's embedded-modules config, EmbeddedModule, the embed protocol or module-urls, or when the user asks "what do I do next to make <module> run".
---

# Extracting an N-Quốc module

The playbook from N-IT, N-Design (2026-09-15) and N-Fit (2026-09-16). Written
from what actually went wrong.

**The shape:** a module is a **content-only web on its own domain**, created
from `nquoc-module-template`, shown by nquoc-user inside its content area
through an iframe. nquoc-user keeps the sidebar, login, notifications and theme;
the module renders only its pages and borrows the API token over `postMessage`.
No reverse proxy, no shared sidebar package.

**Since the kit (2026-09-16)** every module repo also runs **against the staging
backend with no local backend**: `pnpm dev` → dev login → real data. The shared
half of a module repo is the kit — read `references/kit.md` first; it is the
part you must not reinvent.

**Read before planning:** `plans/frontend-kit-standard.md` (the standard),
`context.md` (strategy, incl. "Cô lập backend theo module"),
`plans/module-embed-architecture.md` (why iframes). Human-facing short version:
`MODULE-EXTRACTION-CHECKLIST.md` at the workspace root — keep it in sync with
this file.

## Starting from just a module name

The user may say no more than `/extract-nquoc-module task` or "tách N-Task ra".
Derive the rest yourself, then confirm it in one short message:

| Field | How to derive |
| --- | --- |
| `key` | lower-case, no `n-` prefix: N-Task → `task` (domain `task.nquoc.vn`, path `/n-task`) |
| `name` | display name as used in nquoc-user's sidebar (`src/constants/config.ts`, i18n `menu.*`) |
| `devPort` | next free port after the entries in `nquoc-user/src/app/config/embedded-modules.ts` (8080 user, 8081 it, 8082 design, 8083 fit, 8084 edit → 8085…) |
| scope | routes in `nquoc-user/src/App.tsx` under `/n-<key>` + the pages they render |

Then run Phase 1 (audit) and **stop for approval before writing code**. Say in
that message which steps a human must do (they are listed under "Human steps"),
so the person can start the GitHub/Cloudflare work in parallel.

## Where to start

| Situation | Go to |
| --- | --- |
| New module, from the name | "Starting from just a module name", then Phase 1 → 7 |
| What the shared half of a repo contains, how to create/sync it | `references/kit.md` |
| Backend mixed into shared code, direct Supabase, permissions in RLS | `references/backend-isolation.md` |
| Someone else extracted a module and you must check it | `references/audit-existing-extraction.md` |
| Code merged, module must run on staging then production | `references/rollout.md` |
| Before switching a module on in nquoc-user (any environment) | `references/embed-checklist.md` |
| Push/PR/install/deploy fails: 403, not found, not logged in | `references/access-checklist.md` |

## Working with the person driving this

These rollouts touch real users, several repos and two clouds, and much of it
needs a human with the right account (GitHub merge, Cloudflare dashboard).

**Default to autonomous, end-to-end execution.** The one hard gate is Phase 1:
produce the audit + plan and **stop for approval**. Everything the plan covers
was decided there — once it is approved, do the *entire* implementation in one
continuous run without pausing to ask or narrating one step at a time: create
the repo, isolate the backend (all its PRs), migrate the module, run the
reviews, wire nquoc-user, smoke each deploy, and open **both** the
`enabled.staging` and `enabled.production` nquoc-user PRs together (Phase 6) —
prepared and reviewed at the same time so the human's two merges are
back-to-back once staging checks out, not one merge then a wait for you to
draft the second. The production PR still must not be merged (by you or the
human) before the staging one is merged, deployed, and passed
`references/embed-checklist.md`. Push feature branches and open PRs (always
into `dev`) as you go — do not wait for permission per PR; the plan approval
covers them.
Batch what a human must do into one checklist and keep coding rather than
blocking on it.

- **Only these stop you** (you cannot do them — you have no such access): a
  human with GitHub merge rights merging PRs (merger ≠ author; `dev → main` is
  the Tech Lead's), the Cloudflare dashboard (Workers Builds projects + build
  variables), Railway `CORS_ORIGIN`, and the signed-in embed-checklist with real
  accounts. Do everything else and hand these over as a batched list.
- **Verify every deploy yourself** rather than trusting a "done": `gh pr view`
  for merge state, the check-runs API for Cloudflare builds, `pnpm smoke <url>`
  and `curl -sI` the deployed bundle for what actually shipped (env, CSP). A
  human "I merged / I fixed the var / I retried" has been wrong or incomplete
  more than once — re-check the live artifact before continuing.
- **Explain rollback before every production change**, not after.
- Only genuinely blocking uncertainty (something the plan did not settle and
  that would make the work wrong if guessed) is worth a question mid-run — and
  even then, do everything that does not depend on the answer first.

## Git flow — before the first commit, every time

- branch from the latest `origin/dev` (`git checkout -b feat/<x> origin/dev`)
- PR **into `dev`**; never commit/push to `dev`/`main`, never `--no-verify`
- **never open a PR from `dev` into `main`** — Tech Lead only
- PR body: Summary + Test plan
- a repo made from the template already has the husky hooks and the CI
  workflows; nothing else needs a "guardrails first" PR any more

## The things that will bite you

1. **The scope estimate will be wrong, usually by 3–5×.** A module's folder is
   not its cost; its transitive closure is. N-IT was audited at "23 files,
   ~3.5k LOC" and was **103 files, 15.3k lines**. Compute the closure with a
   real import-graph walk (`references/scripts.md`) before promising anything.
2. **You are probably on the wrong branch.** Run
   `git -C nquoc-user branch --show-current` first; the team works on `dev`.
3. **"No direct Supabase usage" is usually only true of the module folder.**
   Grep the whole closure. Browser-side Storage/Realtime matter most: an
   embedded web has no Supabase session, so they use the parent's token
   (nquoc-it's `accessToken: () => authTokens.getAccessToken()`) or a backend
   endpoint.
4. **Links that leave the module are strings.** Inside the module routes are
   root-relative; a link to another N-Quốc page must go through
   `embedBridge.open(href)`. Lint will not see them — grep `navigate(`, `href=`,
   `window.location`.
5. **Chrome stays in nquoc-user.** Sidebar, bell, user menu, logout, theme. Do
   not rebuild them. Something new the module needs from the parent = a new
   message type in **both** copies of `embed-protocol.ts`.
6. **Do not copy another module repo.** Create from the template
   (`references/kit.md`); sync later with `pnpm kit:sync`. Before the kit,
   six `src/infrastructure` files had already drifted a day after a copy.
7. **Search-and-replace copies claim things that never happened.** After
   `init-module.mjs`, grep the repo for `example` and for the old module's name,
   and read every sentence that says something was verified.
8. **A UI moved out of nquoc-user keeps its data shape, not its data.** N-Fit's
   pilot ran on MSW; on staging its endpoints do not exist. Design every panel
   to show an empty state on 404 instead of a blank page, and record the gaps
   (`references/kit.md` → Contract workflow).
9. **Cloudflare settings are part of the migration.** A Worker that predates the
   kit carries the old build variables and the old deploy command; see the
   failure table in `references/kit.md`.
10. **The module repo may already exist** (an old non-tech mockup — N-Edit's
    `dev` was a lone Readme with `ui/*` branches). "Use this template" only makes
    a *new* repo, so you cannot apply it. Do not force-push over the existing
    repo either: run `init-module.mjs` on a fresh template clone, then commit
    that content on a `feat/init-module-kit` branch and PR it into the existing
    `dev`. Same result, `ui/*` branches preserved. (`references/kit.md`.)
11. **A wrong `-dev` build variable is invisible until the iframe is blank.** If
    `nquoc-<key>-dev` builds with `VITE_APP_ENV=production` (or the prod API URL),
    `preview.<key>.nquoc.vn` ships `frame-ancestors: nquoc.vn` — so the *staging*
    shell `preview.nquoc.vn` is refused as an embedder and the iframe is blank,
    with no error. Always `curl -sI https://preview.<key>.nquoc.vn | grep -i
    frame-ancestors` after a deploy: staging must be `preview.nquoc.vn`, prod
    `nquoc.vn`. And **changing a Cloudflare build variable does not rebuild** —
    the human must Retry the deployment (or push); confirm the bundle hash
    changed *and* the header flipped before believing it.
12. **The contract checker inlines a `const` but not `as const`, and cannot see
    inside a helper.** `apiClient` paths must be literal templates whose only
    `${…}` are path params: write `` `/orders/${teamKey}/x` `` (param → matches
    `/orders/{teamKey}/x`). A module-fixed key needs `` const TEAM = 'edit' as
    const `` — a plain `const TEAM = 'edit'` is inlined to a literal `edit`
    segment and fails to match `{teamKey}`. Never route calls through a
    `const base = (k) => \`/x/${k}\`` helper: the checker collapses
    `${base(k)}` to one opaque segment that can never validate *and* whose
    approved-gap can never self-detect as stale. Inline the path.
13. **Bun / pnpm may not be on the machine.** The backend runs on Bun; if it is
    absent, use `npx -y bun@<pinned> …`. A broken global pnpm → `npx -y
    pnpm@10.10.0 …`. (`references/access-checklist.md`.)
14. **`openapi.json` and `Index.tsx` fight the filesystem.** Regenerating
    `openapi.json` reorders the whole file (swagger-jsdoc glob order differs per
    OS) — a 6k-line diff the audit tolerates but review cannot; merge your
    additions onto the committed key order instead (`references/backend-isolation.md`).
    And a module page named `Index.tsx` collides with the module's `index.ts` on
    Windows/macOS — rename the page (`edit-team-page.tsx`) (`references/scripts.md`).
15. **Copying the order domain drags npm deps and dead files.** The donor's
    `modules/order`/`shared` may need packages the template lacks (tiptap,
    recharts, date-fns, radix-*) — add them from the donor's `package.json`.
    Cross-module deep imports are a lint error, so `modules/edit` reaches the
    order domain only through `@/modules/order`: trim its `index.ts` to the exact
    surface the module imports, then delete what an import-graph walk from
    `main.tsx` now finds unreachable (the barrel hid it before). (`references/scripts.md`.)
    A module that uses **more** of `api/orders.ts` than the donor did (Admin uses
    the post-draft/brand-page/fan-out functions N-Edit pruned) is cleanest fixed
    by taking nquoc-user's **full** `api/orders.ts` and converting its
    `` const b=(k)=>`/orders/${k}` `` helper to literal `` `/orders/${teamKey}/…` ``
    paths (gotcha 12), then `export *`-ing it from the order barrel and pruning by
    reachability — rather than porting functions one by one.
16. **The backend is a different GitHub org.** `NLH-NQUOC-CORE/nquoc-backend`,
    not `NLH-NQUOC-LABS` (all the frontend repos). `gh` needs
    `--repo NLH-NQUOC-CORE/nquoc-backend`. And the toolchain often isn't global:
    `npx -y bun@<pinned>` for the backend (`bun test`/`openapi:audit`),
    `npx -y pnpm@10.10.0` for module repos **with `CI=true`** (without it, `pnpm
    add`/`install` silently keep the frozen lockfile and never install the new
    dep), and `node_modules/.bin/tsc` (the `npx typescript tsc` form is flaky).
    The backend has ~160 pre-existing `tsc` errors and does **not** gate on tsc —
    its gates are `bun test` + `eslint .` + `openapi:audit`.
17. **`openapi:audit` is order-insensitive** (it compares with a recursively
    key-sorted `stableJson`), so the merge-deltas approach in
    `references/backend-isolation.md` B2 works — parse `git show HEAD:openapi.json`,
    append only the new paths/`Duty*` components, **and sort the top-level `tags`
    array by name** (it is the one array whose order the audit compares; the
    generator sorts it). A full `openapi:generate` reshuffles paths/components per
    OS and produces an unreadable diff.
18. **A module can own a bare product domain** instead of `n-<key>`: set
    `webHost` on its `embedded-modules.ts` entry (N-Admin → `admin.nquoc.vn`).
    `moduleWebUrl(key, env, devPort, host?)` defaults `host` to `n-<key>`;
    `frame-ancestors` is keyed on `VITE_APP_ENV` (the nquoc-user origin), not the
    module's own domain, so nothing else changes. If the bare domain is held by
    another app (a Vercel deploy), the Cloudflare Worker can't attach it until
    that app releases it — a human prerequisite for the prod cutover. **The
    template's own default is now the bare domain** (commit "domain-bare"): a
    freshly-scaffolded `wrangler.toml` already reads `<key>.nquoc.vn` /
    `preview.<key>.nquoc.vn` with no edits needed — verify this against the
    actual file after `init-module.mjs` runs rather than assuming you must set
    `webHost` by hand (N-Task, 2026-09-16).
19. **A large module's backend isolation (Phase B2/D-style PR stack) parallelizes
    safely across background agents *within* one PR, but not *across* PRs that
    touch the same generated file.** Splitting statusCode/repository work by
    sub-area (e.g. `nwork` vs `ntask`/`nworkspace`) into disjoint-file PRs
    branched from the same parent and run as concurrent agents is safe and fast
    (N-Task's T1a/T1b ran in parallel, zero conflicts, because they touched
    different service/controller files). **OpenAPI-docs PRs (T2a/b/c/d) must
    NOT run in parallel** — they all hand-merge onto the same `openapi.json`
    and the same `MODULE_OWNERS` array in
    `openapi-operation-metadata.ts`, so run them sequentially, each stacked on
    the previous one's branch. When a later PR (e.g. the repository-layer T3)
    needs the combined result of two *parallel* disjoint-file PRs that aren't
    merged to `dev` yet, build a local integration branch first — `git worktree
    add <dir> -b <name> <second-PR-branch>` then `git merge <first-PR-branch>
    --no-edit` — verify it's green (test/lint/audit) before branching the next
    PR off it, and say in that PR's body which upstream PR numbers it stacks on
    (GitHub will show all their commits until they merge; that's expected).
20. **Give each parallel worktree its own `node_modules` via an OS junction, not
    a fresh install.** `git worktree add` does not copy `node_modules`, and a
    real `pnpm install`/`bun install` per worktree is slow and, with a frozen
    lockfile, sometimes a no-op that leaves the worktree without deps at all.
    When the branch doesn't change `package.json`, junction it from the main
    checkout instead: `cmd //c "mklink /J <worktree>\node_modules
    <main-checkout>\node_modules"` (Windows; needs no admin rights, unlike a
    symlink). Also copy `.env` from the main checkout — bun's test suite reads
    real env vars and fails with a Zod validation error, not a helpful "no
    .env", if it's missing.
21. **This backend repo's source files are CRLF.** A Node one-off script doing
    `content.includes(someMultilineString)` or `.replace(...)` will silently
    find nothing and no-op (or throw once you add an assertion) unless the
    search string also uses `\r\n` — `file <path>` or a quick `node -e
    "console.log(JSON.stringify(fs.readFileSync(p).slice(...).toString()))"`
    on a snippet confirms it before you spend a retry loop on it. Simplest fix:
    prefer a real file-edit tool over scripted regex replacement whenever the
    repo might be CRLF; reserve Node scripts for large mechanical renames where
    you control both sides of the search precisely.
22. **A `checkProjectPermission`-style middleware that resolves an id chain
    (`workId` ← `taskId` ← `commentId` ← …) trusts snake_case body fields
    (`work_id`, `task_id`) — a controller that reads camelCase (`workId`,
    `taskId`) from its own body won't be found by the shared middleware**, so a
    route can look gated (the middleware runs) while silently never resolving
    an id and falling through to whatever the caller supplied instead. This is
    the same failure shape as the message-string-sniffing bug (gotcha for
    duty D1): the guard exists in the code but doesn't actually fire for the
    real request shape. Check both naming conventions are covered when reusing
    a permission middleware in a route file that wasn't written against it
    originally (N-Task's `/gdrive/*` routes, T-SEC PR).
23. **A caller-supplied `work_id`/parent-id in the request body is not proof of
    ownership of the *other* id in the URL.** A route gated by
    `checkProjectPermission(['task:edit'])` where the middleware falls back to
    trusting `req.body.work_id` when it has no lookup branch for the URL's own
    id (e.g. `:labelId`, `:snapshotId`) lets a legitimate editor on Work A act
    on a label/snapshot that actually belongs to Work B, by simply sending
    Work A's id in the body. The fix is a DB-resolved lookup keyed on the URL
    id that **overrides** any client-supplied value for that id type, not one
    that only fills a gap when the client omits it.
24. **Don't rename a module's backend folder while its isolation PRs are still
    open.** N-Meeting's `nmeeting` → `meeting` rename happened *after* the
    initial migration PR was already merged, as its own follow-up PR — not
    interleaved with in-flight work. If a mid-flight rename request arrives
    while several PRs are stacked on the old path (N-Task had 6+ open PRs
    under `src/modules/ntasks` when this came up), queue it as one dedicated
    PR at the end of that chain instead: renaming the shared directory earlier
    would conflict every open PR built against the old path. HTTP mount
    prefixes and the frontend's own module key/domain are a separate naming
    decision from the backend folder name — don't assume a rename request
    covers both without checking which one the user actually named.

## Embedding in nquoc-user

```
nquoc.vn/n-<m>/123          nquoc-user: sidebar, login, bell, theme
└── <iframe src="https://<m>.nquoc.vn/123">   the module web: pages only
        ▲ postMessage (embed-protocol.ts v1)
        │  parent → module: token, navigate, theme
        │  module → parent: ready, token-refresh, navigated, open, logout, auth-failed
        ▼
    api.nquoc.vn (nquoc-backend, unchanged)
```

nquoc-user side (already built, reuse it):

- `src/app/config/embedded-modules.ts` — one entry per module
  `{ key, name, basePath, devPort, enabled: { staging, production } }`, plus an
  optional `webHost` when the module owns a bare product domain instead of
  `n-<key>` (N-Admin → `webHost: 'admin'` → `admin.nquoc.vn`; gotcha 18). The
  `enabled` flags are the only switch (a reviewed PR, no Cloudflare variable).
  URL derived from the host by `src/infrastructure/embed/module-urls.ts`
  (`moduleWebUrl(key, env, devPort, host = \`n-${key}\`)`);
  `localhost` → `http://localhost:<devPort>` for keys in `VITE_DEV_EMBED_MODULES`.
- `src/app/layouts/EmbeddedModule.tsx` — iframe, loading/error UI, URL + theme
  sync. `src/app/layouts/ModuleNotEnabled.tsx` — shown when a module is not
  enabled for that environment (there are no legacy pages left for the
  extracted modules).
- `src/infrastructure/embed/` — protocol, parent bridge, paths; tested by
  `pnpm run test:embed`.

Module side: the kit provides all of it (`references/kit.md`).

Adding a module to nquoc-user = one entry in `MODULES` (`enabled` false at
first) + the `/n-<key>/*` route next to design/it/fit in `App.tsx`.

## Phase 1 — Audit (no code)

Produce `plans/<module>-boundary-audit.md`:

- routes and entry points
- the **full transitive closure**, with file and line counts
- which pulled-in files are shared with other modules, and with how many
- every direct Supabase usage in the closure
- every absolute route in the closure, and which leave the module
- what the module gets from nquoc-user's chrome
- cross-module deep links pointing *into* the module (notifications)
- **backend** (`references/backend-isolation.md` B1): endpoints the closure
  calls, which are in OpenAPI, direct Supabase on that path, module tables,
  where permissions are decided, side effects

Classify each dependency MOVE / COPY / KEEP / REFACTOR-FIRST / BACKEND-OWNED /
DO-NOT-MOVE. **Stop for approval.**

Order-domain modules (Edit, Admin, …) share ~26 `components/order-*` and
`api/orders.ts`: copy them into `modules/order/` with a public API, as N-IT and
N-Design did, unless told otherwise. Realtime modules (N-Task, N-Chat,
N-Meeting): decide in the audit whether realtime uses the parent token or moves
behind the backend.

## Phase 2 — Create the repo from the template

`references/kit.md` → "Creating a module repo". After `init-module.mjs`:

- `pnpm install && cp .env.example .env && pnpm dev` → the dev login must appear
- `pnpm kit:diff` clean, `pnpm verify` green **before** any module code
- the starter `modules/<key>` page proves the whole chain (staging API + types);
  replace it, do not delete the folder

Human steps in parallel: repo created from the template, Write access for the
account doing the work, two Workers Builds projects with their build variables
(`references/kit.md` → Cloudflare).

## Phase 3 — Backend isolation (nquoc-backend, in parallel)

`references/backend-isolation.md` B2, small PRs into `dev`: module folder +
public `index.ts` → OpenAPI for every endpoint the web calls → repository
interface + Supabase adapter → integrations behind adapters → explicit policy
functions → replace browser-side Supabase with endpoints → boundary test.
Model: the Order module (nquoc-backend#383, #385).

Backend ships **before** the frontend that depends on it: staging deploy, then
`pnpm contract:refresh` + `pnpm contract:check` in the module repo.

## Phase 4 — Migrate the module's code

Use the migration script in `references/scripts.md` (maps files, rewrites
imports, reports what it could not resolve). Then, in order:

1. `pnpm typecheck` — expect only Supabase touchpoints, missing npm deps
   (add tiptap/recharts/date-fns/radix-* from the donor's `package.json`), and a
   `Index.tsx` vs `index.ts` casing clash (rename the page)
2. route Supabase touchpoints through `infrastructure/storage` or a module api layer
3. `pnpm lint` — every boundary crossing it reports is a real finding; a module
   may import another module (the order domain) **only** through `@/modules/order`
4. **build the order/module public `index.ts` from exactly what the app imports**
   (cross-module deep imports are a lint error), then rewrite the module's deep
   imports to the barrel
5. grep for routes; make internal paths root-relative, cross-module links go
   through `embedBridge.open`; `apiClient` paths literal (gotcha 12)
6. **diff every migrated file against `dev`**, ignoring imports; commit the
   `filemap.json` the migration script writes
7. **reachability-prune:** trim `index.ts` to the used surface, then delete what
   an import-graph walk from `main.tsx` now finds unreachable (the barrel hid it);
   delete the migration scripts
8. `pnpm contract:refresh` + `contract:check`; record gaps with a `backend_ref`,
   and re-check after the backend deploys — a gap for an endpoint now on staging
   is stale (gotcha 12: a `base()` helper hides this)
9. **Local dev-login smoke before pushing — the human drives it.** After `pnpm
   verify` is green, start `pnpm dev` and open `http://localhost:<devPort>` in
   the Browser frame, then **stop and hand it to the person**: they type a real
   staging account into the "Đăng nhập (chế độ dev)" form and click through the
   module (open an item, create/edit, upload, feedback…) *before* anything is
   committed or pushed. **Never enter the password for them** — you only open
   localhost; they log in. Commit + PR only after they confirm the local test
   passes. This catches runtime breakage (a mis-mapped import, a wrong root-
   relative route, a missing dep) that `verify` — types/lint/build only — does
   not, and it costs nothing because the module already runs against staging
   data with no backend of its own. (`git push` waits for their OK.)

## Phase 5 — Review

Three reviews, separately, after each meaningful step:

- **As a user of the tool** (not a developer): inside nquoc-user, does it feel
  like one system? Is the Vietnamese natural? What did they lose?
- **As a senior engineer**: verify claims rather than reading the diff — do the
  guardrails fire, does the embed protocol check origins on both sides, does the
  commit message overclaim?
- **Functional parity**, legacy vs embedded, before any deploy. On N-Design this
  found 0 business regressions but 11 gaps.

Run them as parallel background agents on detached git worktrees. Reproduce
every finding before fixing it. `references/review-prompts.md` has the prompts.

## Phase 6 — Deploy and switch on

1. Merge the module PR into `dev` → Workers Builds deploys
   `preview.<key>.nquoc.vn`. Watch the check-run, not the clock. **Then verify
   the deployed artifact yourself** — `curl -sI https://preview.<key>.nquoc.vn/
   | grep -i frame-ancestors` and `nslookup preview.<key>.nquoc.vn 1.1.1.1`. A
   green Workers Build does not prove the custom domain actually attached: on
   the N-HR/N-Report wave both `-dev` builds reported success while their
   `preview.<key>.nquoc.vn` domains were NXDOMAIN (the route never attached on
   first deploy) — only a human with Cloudflare dashboard access could add it
   by hand. Catch this before it wastes a review cycle.
2. `pnpm smoke https://preview.<key>.nquoc.vn` — root build, SPA fallback,
   `frame-ancestors` = that environment's nquoc-user, embedded build, no
   localhost API, **no dev login and no mocks**.
3. **Open two nquoc-user PRs at once, not one at a time:** `enabled.staging:
   true` and, stacked on it or as a second branch off the same `dev`,
   `enabled.production: true`. Title the production one clearly, e.g. `feat:
   enable <key> on production (DO NOT MERGE until staging embed-checklist
   passes)`, and say so again in its body. Having both ready and reviewed
   means the human's second merge is immediate once staging checks out —
   no round-trip waiting for you to draft it. **Do not merge the production
   PR yourself, and do not ask the human to merge it, until `staging` has
   actually been merged, deployed, and passed `references/embed-checklist.md`
   with real accounts** — merging the staging PR is the only thing that
   deploys and makes it testable at all (Cloudflare only builds `nquoc-user-dev`
   from commits on `dev`; there is no PR-preview for nquoc-user itself), so
   there is no way to verify staging before that merge, one PR or two.
4. Merge the staging PR → run `references/embed-checklist.md` with real
   accounts on `preview.nquoc.vn/n-<key>`.
5. Production, in this order: module `dev → main` (deploys `<key>.nquoc.vn`,
   creates the domain) → smoke it → merge the already-open nquoc-user
   `enabled.production: true` PR → nquoc-user `dev → main`. The reverse order
   embeds a domain that does not exist yet.
5. **Rollback:** Cloudflare → `nquoc-user-dev`/`-prod` → Deployments → Rollback
   (seconds), then `enabled: false` in a PR; or `wrangler rollback` the module
   Worker for a bad module release.

Notifications and deep links need nothing from the module: nquoc-user still owns
`/n-<key>/*`.

## Phase 7 — Remove the legacy implementation

Only after the embedded module has been stable in production for 1–2 weeks, in
its own PR (N-Fit's static page could go immediately; Design/IT waited).

- find what to delete with an **import-graph diff** from `src/main.tsx`: the set
  reachable before minus the set reachable after removing the legacy routes —
  never by folder name. A legacy folder usually still holds files other pages
  import (three `pages/ITTeam` files were shared with Admin/Edit and had to move
  to `components/order-*` instead of being deleted)
- when comparing paths, normalise Windows backslashes, or the check silently
  reports "nothing is still used" and you delete live files
- update `scripts/direct-ui-exceptions.json` (stale entries fail the
  architecture check), route `/n-<key>/*` to `EmbeddedModule` unconditionally
  with `ModuleNotEnabled` as the fallback
- verify with `tsc --noEmit` (no `TS2307`), `pnpm run build`,
  `check:architecture`, `test:embed`
- **before merging**, tag the last commit that still has the legacy code:
  `git tag archive/legacy-<key> origin/main && git push origin archive/legacy-<key>`
- after this, "flip `enabled` to false" is no longer a rollback; say so in the PR

Reference PR: NLH-NQUOC-LABS/nquoc-user#729 (design + it + fit, −12.1k lines).

## Human steps (the person, not the agent)

1. Create `NLH-NQUOC-LABS/nquoc-<key>` from the template; create `dev` and make
   it the default branch.
2. Give the account doing the work **Write** access.
3. Cloudflare: two Workers Builds projects + build variables + branch control
   (`references/kit.md`); once `pnpm exec wrangler deploy --env preview` for the
   preview Worker.
4. Merge PRs (merger ≠ author) and open `dev → main` when going to production.
5. Test on `preview.nquoc.vn/n-<key>` and `nquoc.vn/n-<key>` with real accounts.
6. Optional: repository secret `KIT_READ_TOKEN` so `kit-drift` can run.

## Definition of done

- [ ] repo created from `nquoc-module-template`; `pnpm kit:diff` clean
- [ ] `pnpm dev` works with **no local backend**: dev login → staging data
- [ ] `pnpm verify` green; CI `verify` green on the PR
- [ ] every change reached `dev` through a feature-branch PR; no `dev → main` PR by the agent
- [ ] no login pages, no sidebar/shell, no base path, no migration scripts left
- [ ] `embed-protocol.ts` byte-identical to nquoc-user's
- [ ] opened directly it redirects into nquoc-user; `frame-ancestors` lists only that environment's nquoc-user
- [ ] staging/production bundles contain no dev login and no MSW (`pnpm smoke`)
- [ ] no business file imports Supabase, and lint proves it
- [ ] all data access goes through a module api layer; `contract:check` clean or gaps recorded with a `backend_ref`
- [ ] every migrated file matches `dev` except changes you can name; nothing unreachable from `main.tsx`
- [ ] the three reviews are clean
- [ ] nquoc-user has the module in `embedded-modules.ts`; `embed-checklist.md` passed with real accounts
- [ ] Cloudflare: both Workers build and deploy; domains answer; rollback path stated
- [ ] backend: `references/backend-isolation.md`'s definition of done met, or gaps written down with owners
- [ ] no sentence in the new repo claims something that was not done in it

## Module order

| Wave | Modules | Why |
| --- | --- | --- |
| done | IT, Design | pilot + second Order-domain module; embedded since 2026-09-15 |
| done | N-Fit | first module rebuilt straight on the kit (2026-09-16); backend API still missing, UI shows empty states |
| done | **N-Edit** | 2026-09-16; first with full backend isolation (order policy layer, storage adapter, boundary test) done in the same wave, and first `contract:check`-clean order module; `nquoc-edit` (repo already existed as a mockup) |
| done | **Admin** | 2026-09-16; `modules/order` **copy #4** from `nquoc-edit` + re-added `order-detail`/`order-rounds`/`order-content-studio`; first full **duty** backend isolation (repository + policy + boundary test, `src/modules/duty`); first module on a **bare product domain** (`admin.nquoc.vn`, not `n-admin`) via the `webHost` override; `nquoc-admin` (repo pre-existed as a mockup) |
| done | **N-Meeting** | 2026-09-16; first Wave-4 (realtime/collab) module — but needed *no* frontend realtime (Google Calendar degraded to an empty state, contract gap recorded); backend `nmeeting` module already existed, needed OpenAPI only; renamed `nmeeting`→`meeting` (backend folder + `/nmeeting`→`/meeting` with the old path kept as a deprecated alias) **after** the initial migration PR, per user request — see gotcha 24; bare domain `meeting.nquoc.vn` |
| done | **N-HR** | 2026-09-16; staging only so far (`enabled.production: false`) pending the embed-checklist |
| in progress | **N-Report** | 2026-09-16; migrated from the legacy NReport page; staging enabled, needs new backend time-off read endpoints before production |
| in progress | **N-Task** | started 2026-09-16 (`plans/task-boundary-audit.md`); first module needing **zero Supabase client** in the module web (realtime + Yjs collab are both parent-owned/dead code, not in the live closure); first backend module isolated **from a completely unisolated state** (0 endpoints in OpenAPI, ~276 direct Supabase calls, 41-branch message-sniffing controller, 33 flat-500 catches, real authorization holes on `/gdrive/*` — see gotchas 19, 22, 23) — the T0–T7 + T-SEC PR-stack pattern here is the reference for any future module in this state, more so than duty/order which already had partial isolation; needed a **new embed-protocol message** (`nquoc:team`, gotcha in `module-embed-architecture.md`) because its board is scoped to the sidebar's active team, unlike every prior module which either owns no team-scoped data or resolves its own primary team from `/users/me/teams` (N-Report's `useActiveTeam` pattern) |
| in progress | **N-Learning** | started 2026-09-17 (`plans/learning-boundary-audit.md` in nquoc-user); backend PR stack merged into one wave (rename `/nlearning`→`/learning` with a deprecated alias, OpenAPI docs file, repository boundary, policy-gated writes, server-side MCQ grading, upload limits, new `POST /learning/activity-events`, boundary test — nquoc-backend#442-447); repo `nquoc-learning` pre-existed as a lone README (gotcha 10) — kit init + full frontend migration in nquoc-learning#1; nquoc-user registered disabled with legacy Training/TrainingDetail pages kept as fallback (nquoc-user#773, same phased pattern as N-HR/N-Report); still needs the nquoc-backend PRs merged + deployed to staging, Cloudflare Workers Builds for nquoc-learning, and the staging embed-checklist before `enabled.staging` can flip |
| in progress | **N-Team** | started 2026-09-17 (`plans/team-boundary-audit.md`, contract `plans/team-api-contract.md`); first **standalone** kit repo — `team.nquoc.vn` keeps its own login + sidebar and is NOT in nquoc-user `embedded-modules.ts` (kit gains `hosting: "standalone"`: real login via nquoc-backend `/auth/*`, `/auth-callback` for Google + recovery, `frame-ancestors 'none'`); legacy repo was a full antd + Supabase app rebuilt in place (archive tag `archive/legacy-team`); leader-side N-Doc/N-Learning authoring/Feedback admin move to their module repos; backend TM0 security (public/unguarded `/teams` writes) → TM-AUTH redirect_origin → TM1 OpenAPI → TM2 endpoints → TM3 repo+policy → TM4 boundary |
| 1 | N-Doc, Academy | self-contained, low coupling |
| 3 | N-Data, Social Content, Potential, Application, Enrollment, Experience, Completion | mostly CRUD over their own domain |
| 4 | N-Chat | realtime/collab — hardest, do last |
| never | Dashboard, Calendar, Rules/Policy, Teams, Profile, Notifications | CORE; they stay in nquoc-user ("Teams" = the sidebar team switcher/org facts; the leader admin portal is N-Team, standalone) |
