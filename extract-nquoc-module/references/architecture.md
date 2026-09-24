# Architecture

> **Kit update (2026-09-16):** the layers below are what `nquoc-module-template`
> ships, plus `src/mocks/` (MSW, dev server only) and
> `src/infrastructure/api/contract-types.ts` (generated). Module identity lives
> in `nquoc-module.json`. See `kit.md`.

Why each boundary exists. From `context.md` Phases 2, 4, 17 and 27, as actually
implemented in `nquoc-it` and `nquoc-design`, embedded in nquoc-user.

## Layers

```
src/
├── app/              routing, providers, layout, auth guard, EmbedSync
├── modules/<name>/   the domain. Public API in index.ts
├── shared/           design system, generic utils/hooks/contexts
└── infrastructure/   embed bridge, auth, api client, object storage, config
```

Dependencies point **down and inward** only:

```
app  ──▶ modules (public API) ──▶ shared ──▶ infrastructure
     └──────────────────────────────▲          ▲
                                    └──────────┘
```

`shared` and `infrastructure` never import a module or the app shell. A module
never imports another module's internals. Nothing imports `@supabase/*` —
the kit bans it everywhere.

## Why a module gets a public API

`modules/<name>/index.ts` is the whole contract. Everything else is private.

This is what makes extraction cheap later: a module with a public API can move
to its own repo by copying a directory. A module whose files are imported from
forty places cannot.

For the Order domain it is also the seam a shared `@nquoc/order-ui` package
would eventually be cut along — the decision to copy rather than package is
reversible precisely because the surface is already named.

Build the API from what the app actually imports, not from what looks tidy.

## The infrastructure boundary

```
component / hook / page          ← may not import the API client
        ↓
modules/<domain>/api             ← the only place that speaks HTTP
        ↓
infrastructure/api/api-client
        ↓
infrastructure/auth/auth-tokens  ← token boundary
        ↓
infrastructure/embed             ← token from nquoc-user (postMessage)
```

The api client asks `authTokens.getAccessToken()`. It does not read
`localStorage` and does not know it is embedded.
`auth-tokens.ts` is the only file that knows the token comes from the parent
(or, for a standalone module and the dev login, from its own auth-central
session in `dev-session.ts`).

That is the whole point of context.md's "frontend only knows the contract".

### Object storage

Files live in Cloudflare R2 **behind nquoc-backend**. The web never holds a
storage key or picks a bucket: it POSTs the file (multipart) to a backend
upload endpoint and gets a URL back — nquoc-it's
`infrastructure/storage/object-storage.ts` (`uploadMediaTo(endpoint, file)`).
The object-key convention lives in `nquoc-backend/src/core/storage/object-key.util.ts`,
the only place that can keep it consistent with what is already stored.

### Config

`infrastructure/config/env.ts` is the only reader of `import.meta.env`, and it
**fails at startup** when critical values are missing (context.md Phase 17).

Two things make this actually work, both learned the hard way:

- Any SDK client that validates its config must be built **lazily**. A
  constructor that throws on an empty URL, called at module scope, throws
  during the import graph's evaluation — before React renders. The result is a
  blank page instead of the error screen, on the exact first-run path the
  README describes.
- Base-path normalisation is **shared** between `vite.config.ts` and the router
  basename. Implemented twice, they drift.

## No base path

The module web is served at the **root of its own domain**
(`preview.<m>.nquoc.vn`, `<m>.nquoc.vn`). nquoc-user owns the public URL
`nquoc.vn/n-<m>/*` and maps it both ways:

| nquoc-user (address bar) | module (iframe) |
| --- | --- |
| `/n-<m>` | `/` |
| `/n-<m>/123?tab=brief` | `/123?tab=brief` |

| layer | mechanism |
| --- | --- |
| Vite | `base: "/"`, output in `dist/` |
| Router | `<BrowserRouter>` without basename |
| Cloudflare | `not_found_handling = "single-page-application"`, `dist/_headers` generated at build |
| nquoc-user | `EmbeddedModule` + `module-paths.ts` (`toModulePath` / `toParentPath`) |

Why not keep `/n-<m>/` inside the module: that existed only so one build could
sit behind the edge proxy on the shared origin. With the iframe the origins are
separate by design, so the base path is pure cost (copied `index.html`,
`_redirects`, basename bugs like `/n-task/n-task`).

## Auth

nquoc-user holds the session; `nquoc-backend` owns the profile and roles. The
module is authenticated only when the backend confirms the profile for the
token nquoc-user sent **and** the role is allowed.

```
nquoc-user                                  module (iframe)
  auth-token (localStorage)  ── nquoc:token ──▶  embedBridge ──▶ authTokens ──▶ api client
  refreshAccessToken()       ◀─ nquoc:token-refresh (on 401)
  performLogout()            ◀─ nquoc:logout / nquoc:auth-failed
```

The distinctions that matter:

- **Origins are checked on both sides.** nquoc-user accepts messages only from
  the module's exact origin and its iframe window; the module accepts only from
  `window.parent` with the nquoc-user origin for its `VITE_APP_ENV`
  (`src/infrastructure/config/parent-app.ts`), then locks to it.
  Paths crossing the boundary must pass `isSafeAppPath` (no `//host`).
- **Definitive denial vs indeterminate failure.** The backend says "no" with
  **403, or 401 even after a successful refresh** — never a 200 with a bad role.
  The api client marks those `authRejected` → "denied". `/auth/me` failing to
  *respond* → "unavailable" with a retry; never treat a network blip as a denial.
- **A refresh is not a new identity.** Re-running `/auth/me` on every new token
  turns "valid token, no profile → 401" into an endless refresh loop. The module
  re-checks only when the token's `sub` changes.
- **Cached data belongs to a user.** Clear react-query whenever the user id
  ends or changes.
- **Fail closed.** A profile with no role is denied.
- **The module never signs anyone in or out.** No login page, no auth client,
  no refresh token. Logout is a message to nquoc-user.

## Who may embed it

The build writes `dist/_headers` with `Content-Security-Policy: frame-ancestors
<nquoc-user origin>`, taken from the same `parent-app.ts` table as the bridge
(selected by `VITE_APP_ENV` in `vite.config.ts`), so they cannot disagree and a
build without a valid `VITE_APP_ENV` fails. There is one nquoc-user per
environment, so the address is code, not a per-Worker variable. Without it any site
could frame the module and try to talk to it (the origin check would still
refuse the token, but clickjacking would not be).

## What stays in nquoc-user

Dashboard, Calendar, Rules/Policy, Teams, Profile and Notifications are CORE,
and so is the chrome: sidebar, bell, user menu, logout, team switcher, theme.
They are what makes independently-deployed webs still feel like one system.
Because nquoc-user keeps owning `/n-<m>/*`, its sidebar, both notification
bells and backend links (`route_path`, `https://nquoc.vn/n-<m>/<id>`) work
without any change; the iframe follows via `nquoc:navigate`.

## Topology

`src/app/config/embedded-modules.ts` in nquoc-user lists the embeddable
modules and, per environment, whether the route renders the iframe or the
legacy page. Module URLs are a naming convention derived from the host
(`module-urls.ts`), matching the modules' own `parent-app.ts`. Cutover is a
reviewed PR; emergency rollback is the nquoc-user Worker's Rollback button. There is no registry-driven proxy any more; the old
`platform/edge-proxy` only remains until the custom domains move back to
nquoc-user (`rollout.md` §7).
