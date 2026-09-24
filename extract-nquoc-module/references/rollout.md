# Rollout: merged code → staging → production

> **Kit update (2026-09-16):** the edge proxy is gone — only N-IT and N-Design
> ever sat behind it, and both were cut over on 2026-09-15. For any new module
> skip §1 and the proxy steps. Add to §0: the Cloudflare Workers Builds settings
> in `kit.md` (build variables, deploy commands) must be right before the first
> merge, and `pnpm smoke` now also asserts the deployed build has no dev login
> and no mocks. Production order for a new module: module `dev → main` → smoke
> the module domain → nquoc-user `enabled.production: true` → nquoc-user
> `dev → main`.

How a module web goes live embedded in nquoc-user. Do **one step at a time**.
Verify it yourself, then hand over the next one.

`<m>` is the module key (`it`, `design`), `/n-<m>` its path in nquoc-user,
Commands marked
**(Cloudflare machine)** run where `npx wrangler@4 whoami` shows the NhiLe
Holding account.

| Env | nquoc-user | Module Worker | Module domain |
| --- | --- | --- | --- |
| staging | `preview.nquoc.vn` (`nquoc-user-dev`) | `nquoc-<m>-dev` | `preview.<m>.nquoc.vn` |
| production | `nquoc.vn` (`nquoc-user-prod`) | `nquoc-<m>-prod` | `<m>.nquoc.vn` |

## 0. Before starting

- The module PRs and the nquoc-user PR that adds the module to
  `src/app/config/embedded-modules.ts` are merged into `dev`. Check each one
  with `gh pr view <n> -R <repo> --json state`. "Merged" reports were wrong once.
- The module entry exists in nquoc-user with `enabled` all false, deployed to
  `nquoc-user-dev`. Nothing changes for users yet.
- **Do not merge the module's embedded build into `dev` while the edge proxy
  still routes `/n-<m>` to its Worker** — Workers Builds deploys it at once and
  `preview.nquoc.vn/n-<m>` goes blank. This happened to N-Design on 2026-09-15;
  do §2 first.
- `embed-protocol.ts` is identical in both repos:

  ```bash
  diff nquoc-user/src/infrastructure/embed/embed-protocol.ts nquoc-<m>/src/infrastructure/embed/embed-protocol.ts
  ```

## 1. Is the module behind the old edge proxy?

Only N-IT and N-Design ever were. Check the live state:

```bash
curl -s -D - -o /dev/null https://preview.nquoc.vn/n-<m>/
```

- `x-nquoc-route: n-<m>` → the proxy still sends `/n-<m>` to the module
  Worker. Do §2 before deploying anything to that Worker.
- `x-nquoc-route: nquoc-user`, or no header at all → go to §3.

## 2. Send `/n-<m>` back to nquoc-user (proxy modules only)

**Preferred: take the proxy out of the path.** Cloudflare → `nquoc-proxy-dev` →
Settings → Domains & Routes → remove `preview.nquoc.vn`; then immediately
`nquoc-user-dev` → Domains & Routes → Add → Custom domain `preview.nquoc.vn`.
(Adding it first fails: "Hostname already in use by other custom domain".)
Check that responses no longer carry `x-nquoc-route`. Leave the proxy Worker
for a few days as a way back, then delete it. Done for staging on 2026-09-15.

**Alternative, while the domain must stay on the proxy:**

The proxy forwards `/n-<m>/*` unchanged; the new root-based build cannot
answer there (blank page, assets 404). So first make nquoc-user answer.

1. **Human, Cloudflare:** `nquoc-proxy-dev` → Settings → Variables → set
   `ROLLBACK_MODULES=<m>` (comma-separate when both). Immediate, no deploy.
2. **You:** check `curl -s -D - -o /dev/null https://preview.nquoc.vn/n-<m>/`
   now says `x-nquoc-route: nquoc-user:rollback`. Users see the legacy page.
3. **You:** make it durable — the next proxy deploy resets variables. In
   nquoc-user set `serve.dev` → `"legacy"` for the module in
   `platform/modules.json` (hand-edit one line), run
   `node platform/edge-proxy/scripts/generate.mjs` and `--check`, PR into `dev`.
   After merge, deploy the proxy by hand (there is no workflow for it; Cloudflare
   machine, from `platform/edge-proxy`): `npx wrangler@4 deploy --env="" --dry-run`, read the
   bindings, then without `--dry-run`.

## 3. The module web on staging

1. **Human, Cloudflare dashboard:** the Worker `nquoc-<m>-dev` exists and is
   connected to the repo (branch `dev`, deploy command
   `pnpm dlx wrangler deploy --env dev`). Build Variables from the Deploy section of the
   module's `README.md`: `VITE_APP_ENV=staging` (not `development` — it decides
   which nquoc-user may embed the web), `VITE_API_URL` (+ `VITE_AUTH_URL` for a
   standalone module). Delete the old `VITE_BASE_PATH`, `VITE_AUTH_STORAGE_KEY`,
   `NODE_AUTH_TOKEN`, and any `VITE_SUPABASE_*` / `VITE_AUTH_DRIVER` /
   `VITE_REALTIME_DRIVER` left from before 2026-09.
2. Deploy (merge to `dev` triggers Workers Builds). `routes` with
   `custom_domain = true` attaches `preview.<m>.nquoc.vn`; if the domain is
   already attached to that Worker in the dashboard, nothing changes.
   Watch the build with `gh api repos/<org>/<repo>/commits/dev/check-runs`.
3. **You:** `pnpm run smoke https://preview.<m>.nquoc.vn` in the module repo.
   Every check must pass.

## 4. Switch it on in staging

1. **You:** open TWO PRs into nquoc-user `dev` at the same time — one setting
   `enabled.staging: true`, one setting `enabled.production: true` (title it
   `DO NOT MERGE until staging embed-checklist passes`). Preparing both now
   means the human's second merge in §6 is immediate instead of waiting on you
   to draft it later. **The production PR must not be merged until this
   section is fully done** — there is no way around merging the staging PR
   first: Cloudflare only builds `nquoc-user-dev` from commits actually on
   `dev`, so nothing is testable before that merge regardless of PR count.
2. A human merges the staging PR; Workers Builds deploys `nquoc-user-dev`.
3. **You:** confirm the new nquoc-user bundle is live (its `index-*.js` name
   changed) and `pnpm run smoke https://preview.<m>.nquoc.vn` passes. Also
   `curl -sI https://preview.<m>.nquoc.vn/ | grep -i frame-ancestors` and
   `nslookup preview.<m>.nquoc.vn 1.1.1.1` — a green Workers Build does not
   prove the custom domain attached (seen on the N-HR/N-Report wave: both
   `-dev` builds succeeded while their domains were NXDOMAIN until a human
   added them by hand in the Cloudflare dashboard).
4. **Human:** run `embed-checklist.md` on `https://preview.nquoc.vn/n-<m>` with
   real accounts (requester, team member, leader, an account without access).
5. **Rollback:** `nquoc-user-dev` → Deployments → Rollback (seconds), then a PR
   with `enabled.staging: false`.

## 5. Production prerequisites

1. **Tech Lead:** merge `dev → main` in the module repo **and** in nquoc-user,
   and check that `main` has no commits missing from `dev`. You do not open
   these PRs.
2. **Human:** Worker `nquoc-<m>-prod` (branch `main`, deploy command
   `pnpm dlx wrangler deploy --env=""`, non-production builds off), with the
   production Build Variables from the module README's Deploy section.
3. **You:** check that backend `main` contains the endpoints the module calls:

   ```bash
   git -C nquoc-backend rev-list --count origin/main..origin/dev
   ```

   Then `git diff --stat origin/dev origin/main -- src/modules/<domain>`.
4. **You:** module bundle config matches production: API `api.nquoc.vn`; for a
   standalone module `VITE_AUTH_URL=https://auth.nhi.sg` (staging is `auth-dev.nhi.sg`).

## 6. Cut over in production

Quiet hour. Explain the rollback to the human before starting.

1. **Before:** the `enabled.production: true` PR opened back in §4 step 1 is
   still open and green — merge it into nquoc-user `dev` now. The module
   repos' `dev` is ready — but `dev → main` NOT merged yet anywhere.
2. **Proxy modules only:** move `nquoc.vn` off `nquoc-proxy-prod` onto
   `nquoc-user-prod` as in §2 (remove, then add). Until the next step the
   legacy pages answer `/n-<m>` — acceptable for minutes, so do 2–4 back to back.
3. **Tech Lead:** merge `dev → main` in the module repos (Workers Builds deploys
   `nquoc-<m>-prod`); `pnpm run smoke https://<m>.nquoc.vn`.
4. **Tech Lead:** merge `dev → main` in nquoc-user (deploys `nquoc-user-prod`
   with the module enabled).
5. **Human:** `embed-checklist.md` on `https://nquoc.vn/n-<m>`. Watch for 30 minutes.
6. **Rollback:** `nquoc-user-prod` → Deployments → Rollback (legacy pages back
   in seconds). A bad module release alone: `npx wrangler@4 rollback --env=""`
   in the module repo.

## 7. After cutover

- Add `https://<m>.nquoc.vn` and `https://preview.<m>.nquoc.vn` to
  nquoc-backend's `CORS_ORIGIN` (Railway), so the module keeps working when the
  allow-all entry in `server.ts` is removed.
- **Legacy code:** after 1–2 weeks stable, delete the legacy page from
  nquoc-user in its own PR. Move anything other pages still import first
  (for IT/Design: `ITOrderEventCard`, `AssignMemberSheet`, the `UIOrder` type).
- **Retiring the edge proxy** (once no module is served `standalone` in any
  env): move the custom domains `preview.nquoc.vn` → `nquoc-user-dev` and
  `nquoc.vn` → `nquoc-user-prod` (Cloudflare → Worker → Domains & Routes → Add
  Custom Domain, confirm the move), check the site, then delete
  `nquoc-proxy-dev/prod`. In nquoc-user delete `platform/` and the `edge:*` scripts
  (`packages/shell/` and both workflows are already gone); deprecate
  `@nlh-nquoc-labs/shell` on GitHub Packages.
