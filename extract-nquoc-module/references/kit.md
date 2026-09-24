# The N-Quốc module kit

Everything a module repo shares with every other module repo. Source of truth:
[`nquoc-module-template`](https://github.com/NLH-NQUOC-LABS/nquoc-module-template)
(GitHub template repo; local checkout at `nquoc-module-template/` in this
workspace). Full standard: `plans/frontend-kit-standard.md`.

Applied to `nquoc-design`, `nquoc-it`, `nquoc-fit` and `nquoc-edit` (2026-09-15/16).

## What the kit gives a module

| Area | What you get |
| --- | --- |
| Dev without a backend | `.env.example` points at staging (`https://api-dev.nquoc.vn/api`); `pnpm dev` shows a **dev login** form (staging account) when the web runs standalone |
| Identity | `nquoc-module.json` (`key`, `name`, `devPort`) — the only file that differs per module; every kit file reads it |
| Embedding | embed bridge + `parent-app.ts` table (development / preview / staging / production), `frame-ancestors` written into `dist/_headers` at build time |
| Contract | `pnpm contract:refresh` (staging OpenAPI → `generated/` + `src/infrastructure/api/contract-types.ts`), `contract:check`, `approved-contract-gaps.json` |
| Mocks | MSW under `src/mocks/`, **only** in `pnpm dev` with `VITE_ENABLE_MOCKING=true`; a build with mocks on fails |
| Guardrails | ESLint (no `fetch`/XHR outside the api layers, no `import.meta.env` outside config, no `@supabase/*` anywhere, no deep imports between modules), husky (`dev`/`main` + secret files, `pre-push` runs `verify`) |
| CI | `.github/workflows/`: `verify`, `contract-drift`, `guard-direct-push`, `kit-drift` |
| Deploy | `wrangler.toml` with `-prod` (root), `[env.dev]`, `[env.preview]`; `pnpm deploy:preview` (one preview URL per branch) |
| Docs | `CLAUDE.md` (two git lanes, locked stack, core files), `agents/api-vibe-coding.md` (API checklist, `BLOCKED_BY_TECH`), README |

`kit-files.json` lists the files that must stay identical everywhere.

## Creating a module repo

```bash
# 1. GitHub → nquoc-module-template → "Use this template" → NLH-NQUOC-LABS/nquoc-<key>
git clone https://github.com/NLH-NQUOC-LABS/nquoc-<key>
cd nquoc-<key>
node scripts/init-module.mjs <key> "<Name>" <devPort>   # e.g. fit "N-Fit" 8083
pnpm install && cp .env.example .env && pnpm dev
```

`init-module.mjs` writes `nquoc-module.json` and renames `example` everywhere
(package name, wrangler workers + domains, README, CLAUDE.md, the starter
module folder), producing **`<key>.nquoc.vn`** / `preview.<key>.nquoc.vn`
(the module domain; users only ever see `nquoc.vn/n-<key>`). Ports in use:
`nquoc-user` 8080, it 8081, design 8082, fit 8083, edit 8084 — take the next
free one and use the same value in nquoc-user's `embedded-modules.ts`.

Do **not** scaffold by copying another module repo any more; that is how the
repos drifted before the kit existed.

**If `nquoc-<key>` already exists** (an old non-tech mockup — N-Edit's was a lone
`Readme` on `dev` plus `ui/*` branches), "Use this template" cannot be applied to
it and force-pushing would destroy the `ui/*` work. Instead: clone the template
elsewhere, `init-module.mjs` it, then bring that content into the existing repo on
a branch and PR it into `dev`:

```bash
git clone …/nquoc-module-template tmpl && cd tmpl
node scripts/init-module.mjs <key> "<Name>" <devPort> && rm -rf .git
git clone …/nquoc-<key> && cd nquoc-<key>
git checkout -b feat/init-module-kit origin/dev
cp -r ../tmpl/. .           # then remove the old Readme, commit, PR into dev
```

The result is identical to a template-generated repo (same `kit-files.json`, so
`kit:diff` works), with `ui/*` branches preserved. After `init-module.mjs`, grep
for `example` and fix the one comment it misses in `src/modules/<key>/index.ts`.

## Keeping repos in sync

```bash
pnpm kit:diff                            # compare with the template on GitHub (needs gh auth)
pnpm kit:diff --from ../nquoc-module-template
pnpm kit:sync                            # copy the template's kit files over this repo's
```

Rule: **change a kit file in the template first**, merge it there, then
`pnpm kit:sync` in each module repo as a Tech PR. `kit-exceptions.json` records
a reviewed, temporary difference (none exist today).
A kit change for **every** module repo at once: `node scripts/fleet-kit-sync.mjs --dry-run`
in the template, then with `--branch`/`--title`/`--notes` — one PR per repo into `dev`,
`pnpm verify` run first, re-runnable (repos that already have the PR are skipped).
The `kit-drift` workflow opens an issue weekly; it needs a repository secret
`KIT_READ_TOKEN` (fine-grained, read Contents on the template).

## Dev login (development / preview only)

- Standalone + `VITE_APP_ENV` `development` or `preview` → `DevLoginScreen`
  posts to `/auth/login` at auth-central (`VITE_AUTH_URL`, staging:
  `https://auth-dev.nhi.sg`) and refreshes through its `/auth/refresh`; the
  session lives in `localStorage` per module + API URL. Without
  `VITE_AUTH_URL` the web shows the config-error screen.
- Inside nquoc-user's iframe the embed bridge supplies the token; the dev login
  never appears.
- `staging` / `production` builds contain neither the form nor MSW — verified by
  `pnpm smoke <url>` ("no dev login and no mocks"). Keep it that way.
- A 401 whose refresh fails ends in "chưa có phiên đăng nhập" (the dev login),
  not "không kết nối được máy chủ".

## Standalone hosting (own domain, own login — e.g. N-Team)

A kit repo that is **not** embedded in nquoc-user (`team.nquoc.vn`: own login,
own sidebar, staging and production) sets `"hosting": "standalone"` in
`nquoc-module.json` (default `"embedded"`; new repo:
`init-module.mjs <key> "<Name>" <port> --standalone`). Added in
`nquoc-module-template` (`feat/kit-standalone-hosting`).

- Build-time: `vite.config.ts` `define`s `__NQUOC_STANDALONE__` from the JSON;
  `STANDALONE` in `config/env.ts`. Embedded bundles contain no `LoginScreen`,
  `AuthCallbackPage` or Google/recovery session code (`standaloneAuth` in
  `dev-session.ts`); standalone bundles contain no dev login and no embed
  bridge messages.
- Runtime: no redirect to nquoc-user, `frame-ancestors 'none'`, bridge inert,
  `LoginScreen` (`data-login`) in every env, signing in at **auth-central**.
  `App.tsx` (not routes.tsx) mounts auth-central's two return pages:
  `/auth-callback` (Google comes back with `#access_token…`; kept only after
  the backend's `GET /auth/me` confirms an N-Quốc profile — invite-only) and
  `/auth/reset-password?token=…` (the recovery email; `POST /auth/password/reset`
  at auth-central). Tokens only in `localStorage` `nquoc:session:<key>:<api>`;
  `main.tsx` strips them from the address bar first.
- Cloudflare build variables: an embedded module's, **plus `VITE_AUTH_URL`**
  (`https://auth.nhi.sg` on -prod, `https://auth-dev.nhi.sg` on -dev).
- **Human step**: auth-central `ALLOWED_RETURN_ORIGINS` (both environments)
  adds `https://<key>.nquoc.vn`, `https://preview.<key>.nquoc.vn`,
  `http://localhost:<devPort>`. Without it Google answers 400 and
  "Quên mật khẩu?" is refused.
- `pnpm smoke` switches to standalone checks (`'none'`, `data-login` present,
  no `data-dev-login`/MSW, `/auth-callback` and `/auth/reset-password` serve
  the SPA) and prints a standalone manual checklist.
- Chrome (sidebar, logout via `useAuth().signOut`) lives in the module-owned
  `src/app/layout/AppLayout.tsx`.

## Embedding in a standalone host (N-Team)

A standalone kit app (`team.nquoc.vn`) can show module pages (N-Feedback
`/admin`, N-Learning `/manage`, N-Doc) in its content area the way nquoc.vn
does, with its own session. Added in `nquoc-module-template`
(`feat/kit-extra-embedders`, stacked on `feat/kit-standalone-hosting`).
Protocol (`embed-protocol.ts`) unchanged; nquoc-user needs no change.

- **Module side, opt-in**: `nquoc-module.json` `"embedders": ["team"]` (default
  `[]`; distinct lower-case keys; not allowed with `"hosting": "standalone"`).
  Known keys: `EMBEDDER_ORIGIN_BY_ENV` in `config/parent-app.ts` — `team`: dev
  `http://localhost:8097`, preview/staging `https://preview.team.nquoc.vn`,
  production `https://team.nquoc.vn`. Unknown key → build fails.
  `resolveEmbedderOrigins(appEnv)` feeds both `env.parentOrigins` (bridge
  trust list) and `frame-ancestors` (e.g. staging
  `https://preview.nquoc.vn https://preview.team.nquoc.vn`). Direct visits still
  redirect to nquoc-user. Without `embedders` nothing changes.
- **Bridge handshake**: never `*`. `location.ancestorOrigins[0]` (Chromium/WebKit)
  locks the parent before `ready` when it is trusted; otherwise `ready` is posted
  once per trusted origin (the browser only delivers the matching one) and the
  origin locks on the first valid message from `window.parent`.
- **Host side**: route inside `ProtectedRoute`:
  `<Route path="/feedback/*" element={<EmbeddedModuleFrame module="feedback" basePath="/feedback" defaultPath="/admin" theme={effectiveTheme} teamId={…} />} />`.
  Files: `src/app/EmbeddedModuleFrame.tsx` (lazy behind `STANDALONE`, embedded
  bundles never contain it), `EmbeddedModuleFrameView.tsx` (port of nquoc-user's
  `EmbeddedModule.tsx`), `infrastructure/embed/host-bridge.ts` (port of
  `parent-bridge.ts` + `module-paths.ts` + `resolveOpenTarget`),
  `infrastructure/config/host-modules.ts` (feedback 8093, learning 8091, doc 8092;
  `<key>.nquoc.vn` / `preview.<key>.nquoc.vn`). Token = host `authTokens`;
  refresh = session refresh; failed refresh / `logout` / `auth-failed` → host
  `signOut`; `navigated` → `basePath + path` (replace); `open` → in `hostPaths`
  (default `[basePath]`) navigates, other paths → new tab on nquoc-user, https
  `*.nquoc.vn` URL → new tab, anything else ignored.
- **Rollout order**: module PR adding `"embedders": ["team"]` deployed first
  (`curl -sI https://preview.<key>.nquoc.vn | grep -i frame-ancestors` shows both
  origins), then the N-Team route. `pnpm smoke` compares frame-ancestors with
  nquoc-user + `embedders`. A `*.workers.dev` preview of N-Team cannot frame
  modules; test on `preview.team.nquoc.vn`.
- Caveat: a module's `auth-failed` (403 / role not allowed in that module) signs
  the user out of the host too — same as nquoc-user. A team page should only
  link to module pages the member can use.

## Contract workflow

1. `pnpm contract:refresh` — fetches `VITE_OPENAPI_URL`, re-applies the `/api`
   prefix, writes `generated/openapi.snapshot.json` + metadata, regenerates
   `contract-types.ts`. Malformed schemas in the backend's JSDoc are quarantined
   and listed in the metadata's `contractDefects` (report them to backend).
2. Module api layer calls `apiClient.<verb>('/path')` with a literal or template
   path, typed with `ContractResponse<'/path', 'get'>`.
3. `pnpm contract:check` — every call must exist in the snapshot or be an
   approved gap (`scripts/approved-contract-gaps.json`, each with a
   `backend_ref`). It scans `src/modules/*/api` **and** `src/shared/api`, and
   ignores query strings.
4. Endpoint missing → stop, report `BLOCKED_BY_TECH`, open a contract-request
   for nquoc-backend (a draft OpenAPI fragment under
   `docs/contract-request/` is fine — see nquoc-fit), add the gap, and let the
   UI show an empty state. Mock it only for `pnpm dev`.

## Cloudflare (per module, done once by a human)

Two Workers Builds projects wired to the repo:

| Worker | Production branch | Build command | Deploy command | Non-production branches |
| --- | --- | --- | --- | --- |
| `nquoc-<key>-dev` | `dev` | `pnpm run build` | `npx wrangler deploy --env dev` | `npx wrangler versions upload --env dev` |
| `nquoc-<key>-prod` | `main` | `pnpm run build` | `npx wrangler deploy` | `npx wrangler versions upload` |

Build **variables** (not runtime variables):

| Worker | Variables |
| --- | --- |
| `-dev` | `VITE_APP_ENV=staging`, `VITE_API_URL=https://api-dev.nquoc.vn/api` |
| `-prod` | `VITE_APP_ENV=production`, `VITE_API_URL=https://api.nquoc.vn/api` |

Nothing else. Leftover variables from an older setup break the build on
purpose: `VITE_ENABLE_MOCKING=true` is rejected (it would ship fake data), and
a missing `VITE_APP_ENV` is rejected (it decides who may embed the web).
Domains (`<key>.nquoc.vn`, `preview.<key>.nquoc.vn`) are created by wrangler on
the first deploy (`custom_domain = true`).

`nquoc-<key>-preview` (the non-tech lane, `pnpm deploy:preview`) needs one
manual `pnpm exec wrangler deploy --env preview` to exist.

## Two git lanes (from Nedu)

- **Non-tech:** branch `ui/<mô-tả>` from `origin/dev` → commit → push (pre-push
  runs `verify`) → `pnpm deploy:preview` → send the link. **No PR**; Tech pulls
  the work in.
- **Tech:** `feat/*` → PR into `dev` → merged by someone else. `dev → main` is
  the Tech Lead's.
- `-dev` / `-prod` Workers build from `dev` / `main` only; nobody deploys them
  by hand.

## Kit failures seen in production (do not repeat)

| Symptom | Cause | Fix |
| --- | --- | --- |
| Cloudflare build stuck 15+ min in "Installing" | `.nvmrc` held a partial version (`22.18`) | full version (`22.18.0`) |
| Deploy step hangs after a successful build | `wrangler` not in `devDependencies`, `npx` downloads it | `pnpm add -D wrangler` (the kit has it) |
| Build fails: `VITE_ENABLE_MOCKING=true is not allowed in a build` | leftover Cloudflare build variable | delete the variable |
| Build fails: `VITE_APP_ENV must be …` | Worker never had build variables | add them (table above) |
| `pnpm contract:types` crashes | malformed `@swagger` JSDoc in nquoc-backend | fix the backend YAML; `contract:refresh` quarantines it meanwhile |
| Push rejected with 403 | the agent's GitHub account lacks Write on the new repo | add it in the repo's Settings → Collaborators |
| A follow-up commit never reaches `dev` | the PR was merged while the commit was still being pushed | check `git merge-base --is-ancestor <sha> origin/dev`, open a small follow-up PR |
| Embedded module iframe is blank on staging, no error | `nquoc-<key>-dev` built with `VITE_APP_ENV=production` (or the prod API URL), so `preview.<key>.nquoc.vn` sends `frame-ancestors: nquoc.vn` and the browser refuses `preview.nquoc.vn` as embedder | fix the **`-dev`** project's build variables to `staging` + `api-dev.nquoc.vn`; `curl -sI https://preview.<key>.nquoc.vn \| grep -i frame-ancestors` must be `preview.nquoc.vn` (prod domain must be `nquoc.vn`) |
| Fixed a Cloudflare build variable but the deploy still ships the old value | changing a build variable does **not** trigger a rebuild | Deployments → **Retry deployment** (or push a commit); confirm the bundle hash changed **and** the header/API flipped before believing it — a human "I fixed the var / retried" has shipped the old value more than once |
| A module page hangs/shows a wrong-state screen forever (no team, wrong theme) despite the parent clearly having the right value (check its localStorage/store directly) and auth/data all succeeding | `embed-bridge.ts`'s `onThemeChange`/`onTeamChange` had no replay for a subscriber that mounts after the one-shot message already arrived — fixed in `nquoc-module-template#13` (2026-09-16); confirm the module has synced past it | `pnpm kit:sync`, or diagnose live by adding a temporary `console.log` inside `embed-bridge.ts`'s message `listener` switch statement to see whether the *raw* message arrives (it usually does) vs. whether the *hook* subscribed to it ever fires (the actual break point) |

## Pending kit fixes not yet on every shipped module

Fixes merged into `nquoc-module-template` after a module was extracted only
reach that module once someone runs `pnpm kit:sync` there and merges the
result. Track anything security- or UX-relevant here until every already-
shipped module (currently N-IT, N-Design, N-Fit, N-Edit, N-Admin, N-Meeting,
N-HR, N-Report) has synced past it — delete the row once all of them have.

| Merged | What | Why it matters | Modules still needing `kit:sync` |
| --- | --- | --- | --- |
| 2026-09-16, `nquoc-module-template#12` | `AuthContext.tsx` now calls `embedBridge.authFailed()` on a definitive backend denial (403 / 401-after-refresh / disallowed role), not just a local screen | Before this, a module that got a permanent auth rejection never told `nquoc-user` — the user stayed fully signed in to every other module and the sidebar while only the one module showed "access denied". Security/UX gap, not cosmetic. | N-IT, N-Design, N-Fit, N-Edit, N-Admin, N-Meeting, N-HR, N-Report (all 8 — this is kit-wide, confirmed in `plans/task-step14-parity-audit.md` §9) |
| 2026-09-16, `nquoc-module-template#13` | `embed-bridge.ts` now caches the last `nquoc:theme`/`nquoc:team` message and replays it immediately to a subscriber that calls `onThemeChange`/`onTeamChange` *after* the message already arrived — same pattern `token` already had via `getAccessToken()`. Before this, a component mounting late (which is normal — it's often several router layers deep) could silently never learn the theme or active team for the entire session. | Reproduced live for N-Task: a user with a real, correctly-selected team saw the module's own "no team selected" screen forever, with zero console/network errors, because the one-shot `nquoc:team` message was dispatched to zero listeners before `useActiveTeam`'s subscription existed. Theme has the identical bug (lower visibility, same mechanism) — check any module for a page that occasionally opens in the wrong light/dark theme. | N-IT, N-Design, N-Fit, N-Edit, N-Admin, N-Meeting, N-HR, N-Report (all 8; N-Task got the fix directly, not via kit:sync, since it's where the bug was found — `nquoc-task#5`) |
