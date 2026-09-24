# Embed checklist — before a module is switched on

> **Kit update (2026-09-16):** also confirm the deployed build has no dev login
> and no mocks (`pnpm smoke <url>` checks this), and that the module is reached
> through nquoc-user — opening `<key>.nquoc.vn` directly must redirect to
> `nquoc.vn/n-<key>`.

Run this on **staging** (`https://preview.nquoc.vn/n-<m>`) before enabling the
module for production in `embedded-modules.ts`, and again on production right after.
Use real accounts, never shared passwords typed by the agent: the human signs
in; the agent watches the network and console.

Mark each line PASS / FAIL / N-A and paste the result into the PR or the
rollout thread.

## Automated first

- [ ] module repo: `pnpm run verify` green (typecheck, lint, test, contract, build)
- [ ] nquoc-user: `pnpm run test:embed`, `pnpm run check:architecture`, lint and build green
- [ ] `embed-protocol.ts` is identical. **On Windows a bare `diff` reports the
  whole file** because nquoc-user has no `.gitattributes` and checks out CRLF
  while the module repos are LF. Use `diff --strip-trailing-cr …`, or compare
  git blob hashes (`git -C nquoc-user rev-parse HEAD:src/infrastructure/embed/embed-protocol.ts`
  vs the same in `nquoc-<m>`) — identical hash is definitive.
- [ ] `pnpm run smoke https://preview.<m>.nquoc.vn` passes every check

## One system

- [ ] Sidebar → N-<M>: the module appears inside the content area; the sidebar does not reload or flash
- [ ] Switch to another N-Quốc page and back: no full page reload of nquoc-user
- [ ] Light/dark theme toggled in nquoc-user applies inside the module
- [ ] No second sidebar, user menu, logout button or login page inside the module

## URLs and history

- [ ] Open `/n-<m>/<itemId>` directly (new tab): the item opens
- [ ] F5 on an item keeps the same item and the same URL
- [ ] Navigate inside the module: the address bar follows (`/n-<m>/…`)
- [ ] Back / Forward move through module pages without doubling or getting stuck
- [ ] Notification bell (both bells) opens the right item — with the module closed, and with the module already open on another item
- [ ] Opening `https://preview.<m>.nquoc.vn/<itemId>` directly lands on `https://preview.nquoc.vn/n-<m>/<itemId>`

## Auth and data

- [ ] First load shows data without asking to sign in
- [ ] Token expiry: in DevTools set localStorage `auth-token` on preview.nquoc.vn to an invalid value, then act in the module → it recovers after one refresh, no request loop in the Network tab
- [ ] Logout from nquoc-user's sidebar, sign in as another user, open the module → none of the first user's data or role shows
- [ ] An account without the role sees "Chưa có quyền truy cập" inside the content area (not a blank page, not a login form)
- [ ] Backend down / offline: "Không tải được …" with Thử lại, not a denial

## Module features

- [ ] Create / edit the module's main item end to end (for Order modules: create an order with an attachment, change status, comment)
- [ ] Every upload the module has (order files, pasted images; N-IT: blog media and release media via the backend upload endpoints)
- [ ] Browser permissions the module uses work inside the iframe (N-IT: speech-to-text microphone; clipboard copy)
- [ ] Modals, drawers, date pickers and toasts open and close correctly inside the content area

## Security

- [ ] Response header of `https://preview.<m>.nquoc.vn/` has `Content-Security-Policy: frame-ancestors` with **the matching environment's** nquoc-user origin — staging must be exactly `https://preview.nquoc.vn`, production `https://nquoc.vn`. A `-dev` Worker built with the wrong `VITE_APP_ENV` passes "an nquoc-user origin" but names the *other* environment, so the shell is refused as embedder and the iframe is silently blank. `curl -sI https://preview.<m>.nquoc.vn/ | grep -i frame-ancestors`
- [ ] Embedding the module from any other page (e.g. a local HTML file) is refused by the browser
- [ ] The deployed bundle is the embedded build (contains the embed bridge, `nquoc:ready`) — the smoke test checks this; no login page is reachable inside the module

## Rollback rehearsal (staging, once per module)

- [ ] Cloudflare → `nquoc-user-dev` → Deployments → Rollback to the version before the module was enabled → the legacy page is back at `/n-<m>`
- [ ] Roll forward to the latest version → embedded again
