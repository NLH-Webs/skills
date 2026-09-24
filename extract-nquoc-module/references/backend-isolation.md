# Backend isolation for a module

Extracting a module's frontend is half the job. If its backend code is still
mixed into shared services, runs queries from everywhere and hides
permissions in the database, the team that owns the module still needs Tech
for every change. `context.md` (backend Phase 9–13) describes the target for the whole
backend; this file applies it **to one module at a time**, in the same wave as
its frontend extraction.

Data already lives in PostgreSQL (Railway), files in Cloudflare R2 and
realtime on the backend's SSE stream — the Supabase Exit (2026) is done, and
the repository boundary built here is what made it possible without touching
the frontend. The case studies below predate it and name the old
`supabase-<m>.repository.ts` files; today's equivalent is
`postgres-<m>.repository.ts`.

## Reference and current state (check before relying on it)

- **Pattern to copy:** `nquoc-backend/src/modules/order/` — `routes → controllers
  → services → repositories/{order.repository.ts (interface),
  postgres-order.repository.ts + postgres/*.queries.ts}`, OpenAPI in `openapi/*.docs.ts`, public API in
  `index.ts` (nquoc-backend#383 boundary + repository, #385 OpenAPI).
- **Layer rules:** `nquoc-backend/docs/architecture-boundaries.md`
  (`app → modules → core → integrations → shared`, cross-module only through
  `@/modules/<name>`).
- **State as of 2026-09-16 (N-Admin wave) — the 2026-09-15 gaps are now closed
  for the Order module; re-verify before relying on them for yours:**
  - the boundary test **exists and is green** at
    `tests/app/architecture-boundaries.test.ts` (not `src/app/…` — a
    `test-location` convention test forbids `*.test.ts` under `src/`). It scans
    text, freezes a `@supabase/supabase-js` debt allowlist that may only shrink,
    and asserts `modules/order` is clean;
  - the **policy layer exists and is wired**:
    `src/modules/order/policies/order.policy.ts` (pure `PolicyDecision`
    functions) called from the order controllers;
  - `order-upload.service.ts` is **behind a storage port**
    (`repositories/order-file-storage.ts` over `@/core/storage`, R2), with a
    server-built object key. Re-verify the extension-fallback constraint if you
    copy it.
  - **Still open for a new module:** every non-order module (duty included) has
    none of the above. Add them as part of the isolation, not as a someday task.

## Phase B1 — Audit (with the frontend audit, before code)

Add to `plans/<module>-boundary-audit.md`:

| Question | How to find it |
| --- | --- |
| Which endpoints does the frontend closure call? | `pnpm run contract:inventory -- --json` in the module repo / nquoc-user |
| Which backend files serve them? | route file → controller → service → where data is read |
| Are they in OpenAPI? | `bun run openapi:audit`; count `@swagger` / `*.docs.ts` per route |
| SQL outside a repository on that path? | `git grep -n "getSql" src/modules/<m>` outside `repositories/` (+ helpers it imports) |
| Which tables / storage buckets / realtime topics belong to the module? | queries on the path; shared tables marked SHARED |
| Where are permissions decided? | middleware, service `if`s, database policies in migrations |
| Other modules importing its internals, or it importing theirs? | `git grep -n "modules/<m>/" src` and the reverse |
| Side effects: notifications, cron, telegram, email, uploads | services on the path; `notification/config/topic.config.ts` |
| Anything in the frontend closure that bypasses the backend (uploads, realtime, third-party SDKs) | frontend closure grep — each one needs a backend endpoint |

Classify each item: **MOVE into module**, **STAYS SHARED** (core/integrations),
**ADAPTER NEEDED**, **CONTRACT GAP**. Stop and get it approved together with the
frontend boundary.

## Phase B2 — Isolate (backend PRs into `dev`, before the frontend cutover)

Do it in small PRs, each green on its own. Order:

1. **Module folder + public API.** Move the module's routes/controllers/services
   under `src/modules/<m>/`. Export only what `app` and other modules need from
   `index.ts`. Other modules switch to `@/modules/<m>`.
2. **OpenAPI first.** Every endpoint the frontend calls gets a doc in
   `src/modules/<m>/openapi/*.docs.ts` and an owner in
   `src/core/openapi/openapi-operation-metadata.ts` — the generator (via
   `MODULE_OWNERS`) assigns `operationId`/`tags`/`x-nquoc-module`, so a new mount
   needs a row there or `openapi:audit` fails "missing source-owned metadata".
   `x-nquoc-stability: stable` is a JSDoc line (mark the ops the module depends
   on). `bun run openapi:audit` clean. Contract changes are additive; breaking
   changes need a new endpoint or a coordinated frontend PR.

   **Keep `openapi.json`'s diff small.** `bun run openapi:generate` rewrites the
   whole file in the local filesystem's glob order (Windows vs Linux differ), so
   a plain regen is a multi-thousand-line reordering the audit tolerates
   (order-insensitive) but review cannot read. Merge only the new
   paths/components/tags/stability onto the committed key order instead:
   `git show HEAD:openapi.json` as the base, add just the deltas, keep the base's
   ordering (and its trailing-newline style), then `openapi:audit` to confirm.
3. **Repository boundary.** `repositories/<m>.repository.ts` (interface named by
   business operations, not tables) + `postgres-<m>.repository.ts` (SQL via
   `@/core/db`). Services depend on the interface. No query left in services.
4. **Integrations behind adapters.** Files through `@/core/storage` (R2), Telegram/Google/Gemini through `integrations/*`.
   No SDK imports in the module's services.
5. **Policy visible in code.** `policies/<m>.policy.ts` with functions like
   `canView(user, item)`, `canEdit(user, item)`, called from services. A
   database policy may stay as defense-in-depth but must not be the only check.
6. **Nothing in the module web bypasses the backend.** Uploads go to backend
   endpoints (e.g. `POST /orders/{teamKey}/uploads`), live updates come from
   the SSE stream (`GET /api/realtime/stream`).
7. **Guardrails.** A boundary test (the one `architecture-boundaries.md`
   describes) covering at least this module: no SQL outside `repositories/`,
   no deep imports into `src/modules/<m>/`. Unit tests for policies and the
   service against a fake repository.

Keep behaviour identical: same response shapes, same permissions, same side
effects. Refactor, don't redesign, in these PRs.

**Proven on N-Edit (Order module) — reuse these, one commit per step:**

- **Bun/pnpm may be absent** on the machine: `npx -y bun@<pinned> …`,
  `npx -y pnpm@10.10.0 …`.
- **Policy layer:** make `policies/<m>.policy.ts` pure functions returning the
  exact message + status each controller `if` sent, land it unwired first
  (reviewable in isolation with unit tests), then wire it in a second PR.
- **Kill string-sniffing carefully.** The mapper that did
  `detail.includes('forbidden') → 403` hid the real status in the message. Give
  every 4xx throw an explicit status in the file's own idiom
  (`Object.assign(new Error(msg), { statusCode })`) *before* switching the mapper
  to statusCode-only, or those throws become 500. **Do not** migrate to
  `next(error)` in the same wave: `normalizeError` ignores a bare `statusCode`,
  so it would 500 every un-converted throw. Add a grep test that fails on a new
  bare `throw new Error('…Forbidden…')`.
- **Storage adapter:** a `repositories/<m>-file-storage.ts` port over
  `@/core/storage`; the service builds the object key server-side from the auth
  id and never from client input. Constrain the extension fallback
  (`/^[a-z0-9]{1,8}$/i`) so a crafted filename can't reach the key; test it.
- **Boundary test lives at `tests/app/…`, not `src/app/…`** (a `test-location`
  convention test forbids `*.test.ts` under `src/`). Promote `local/no-module-internal-import` to `error`
  with a scoped `off` only for the OpenAPI aggregator.

**Proven on N-Admin (Duty module) — a module with no repository at all, six
small PRs, one commit each, stacked (D3 on D1, D4 on D3, …) so they merge in
order:**

- **D1 statusCode before anything.** The duty controller sniffed the HTTP status
  from the error *message* (`e.message.includes('quyền') ? 403 : 500`). Give every
  authz throw an explicit `statusCode: 403` (`Object.assign` idiom) and switch each
  controller `catch` to `e.statusCode ?? <existing fallback>` — keep the exact
  per-endpoint fallback (some 500, some 400) so non-authz throws are unchanged. A
  denial the sniff missed (a message without the sniffed word) was silently 500 —
  fixing it to 403 is the point, not a regression. Add a grep test that fails on a
  new bare authz `throw new Error('…quyền…')`.
- **D2 OpenAPI** for every endpoint (there were zero) — merge only the new paths +
  `Duty*` components onto `git show HEAD:openapi.json`, **sort the `tags` array**,
  audit is order-insensitive (SKILL.md gotcha 17). New `MODULE_OWNERS` row required.
- **D3 repository** — one interface method per business operation (not per table);
  move every `supabase.from(...)` **verbatim** into `supabase-duty.repository.ts`
  (keep the `onConflict` keys, the PostgREST embed constraints, the
  `referencedTable` ordering); the `throw new Error(error.message)` on a DB error
  moves into the repo; the `duty-auth.helper` facts (`isAdminTeamLeader` etc.)
  become repo methods too, since the policy builds on them.
- **D4 policy pure + unwired**, one function per gated operation returning the
  exact 403 message, taking a boolean fact; a table-driven unit test pins
  allow/deny/message/status. **D5 wires it** (`enforce(canX(await <fact>))`, a
  one-line `enforce` helper co-located with the decisions) and switches
  `app/routes.ts` to `import { dutyRouter } from '@/modules/duty'`.
- **D6 boundary test** — mirror the order assertions for duty: no database
  client outside `repositories/`, and `modules/duty/index.ts` frozen.

**Proven on N-Task (ntasks module) — a module starting from *zero* isolation
(0 endpoints in OpenAPI, ~276 direct database calls across 22 files including
controllers/middleware, message-string-sniffing across 41+33 catch blocks, and
real authorization holes), split into a wider PR stack than duty's six:**

- **Run T0 (dead code + entry wiring) first, always** — it's small, fast to
  verify, and every later PR benefits from a clean `index.ts`/`routes.ts`. Fold
  in any free-standing bugs you find while reading the entry points (N-Task's
  cron was registered twice — once at import time, once from the explicit
  `start...()` call `server.ts` already made; a missing notification-template
  entry for a topic that *was* registered in the DB but never got template
  copy).
- **Split the statusCode PR (duty's D1) by sub-area when the module has more
  than one, and run those splits as parallel background agents** — they touch
  disjoint controller/service files, so there's no merge conflict, and it cuts
  wall-clock time roughly in half. Give each agent the *actual* fallback status
  each catch block uses today (some 500, some 400) rather than assuming
  they're uniform — a single module can have both a "message-sniffed but
  already correct" area (duty's D1 pattern) and a "flat 500 hiding a real 403"
  area (N-Task's `task.controller.ts`, 33 catches with no message check at
  all — the worse and more urgent bug of the two) in different files.
- **Split OpenAPI docs (duty's D2) by mount when there's more than one, but run
  those SEQUENTIALLY, each stacked on the previous** — they all hand-merge onto
  the same `openapi.json` and the same `MODULE_OWNERS` array, so parallel
  agents would each produce a diverging merge base. Do the mount the frontend
  actually calls first (N-Task did `/nworkspace` before `/ntask`/`/nwork`/`/gdrive`)
  so the module repo's `contract:check` gap list shrinks as early as possible.
  Mark `x-nquoc-stability: stable` only on endpoints a frontend closure audit
  confirmed are actually called — cross-reference the boundary-audit doc's
  endpoint table rather than marking everything in a mount stable by default.
- **Split the repository PR (duty's D3) by sub-area, but sequentially, not in
  parallel** — unlike statusCode splits, a repository introduces a *new*
  interface/naming convention (method names, whether a tangential concern like
  a job queue gets its own repository or folds into the main one, whether
  controllers that queried the database directly get routed through a service or
  straight to the repository). Let the first sub-area PR establish the pattern
  or fold into it and merge, then hand the next agent that PR's actual files as
  its reference example — "mirror `src/modules/duty/repositories`" is enough
  for the *first* split, but "mirror the `NWorkspaceRepository` you'll find at
  this path, including how it named X" is what keeps three more splits
  consistent with each other, not just with duty.
- **When PR N+1 needs the combined result of two sibling PRs that both branched
  from PR N but haven't merged to `dev` yet** (e.g. the repository PR needs
  both statusCode splits already applied, since it's editing the same throw
  sites), build a local integration branch: `git worktree add <dir> -b
  <int-branch> <sibling-A-branch>` then `git merge <sibling-B-branch> --no-edit`
  inside it, verify green (test/lint/audit), and branch PR N+1 off that. State
  in PR N+1's body every upstream PR number it stacks on — GitHub shows all
  their commits in the diff until they merge, which is expected, not a mistake.
- **A large module's authorization holes are usually structural, not a typo** —
  entire route files with only `authMiddleware` and no per-resource check
  (N-Task's `/gdrive/*`, 13 routes, any user could grant Drive access to any
  work) are a different, more urgent kind of finding than a message-sniffing
  bug, and belong in their own T-SEC-style PR the plan calls out as a real
  behavior change needing reviewer sign-off — never fold it silently into a
  refactor PR. When reusing an existing permission middleware for such routes,
  check whether it resolves ids from the same casing convention the new
  routes' controllers actually use (`work_id` vs `workId`) — see SKILL.md
  gotcha 22 — and whether every id type the new routes introduce has a lookup
  branch at all, or falls back to trusting a client-supplied parent id (gotcha
  23).

## Phase B3 — Verify and release

- `bun test`, `bun run lint`, `bun run openapi:audit` green.
- Frontend: refresh the OpenAPI snapshot in the module repo and nquoc-user,
  `pnpm run contract:check` — gaps for this module should shrink, never grow.
- Staging: deploy backend (Railway) **before** the frontend that depends on new
  endpoints; run the module's embed checklist against real accounts, including
  a user without permission.
- Production: backend `dev → main` first, then the frontend cutover
  (`rollout.md`). Check `git -C nquoc-backend rev-list --count origin/main..origin/dev`
  and that the module's endpoints are on `main`.

## Definition of done (backend)

- [ ] everything the module owns lives in `src/modules/<m>/`, reachable from outside only via `index.ts`
- [ ] every endpoint the module web calls is documented in OpenAPI and passes `openapi:audit`
- [ ] services use a repository interface; SQL appears only in `postgres-<m>.repository.ts` / its queries
- [ ] permissions are explicit policy functions with tests
- [ ] the module web reaches data, files and live updates only through the backend
- [ ] a boundary test enforces the module's import rules
- [ ] module-owned tables/buckets listed in the audit
