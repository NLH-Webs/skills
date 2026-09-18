# Access checklist

> **Kit update (2026-09-16):** a repo created from the template starts private
> with no collaborators, so the account doing the work needs **Write** added
> explicitly (nquoc-fit lost a round to a 403 here). Cloudflare access is a
> separate thing again — see `kit.md` for the Workers Builds settings.

Most of the lost time on 2026-09-15 was access, not code. Check all of it
before promising a step, and **test each repo separately**. One "not found"
does not mean the whole org is closed: `nquoc-user` was writable while
`nquoc-it` was not, and it was wrongly reported as "no access to the org".

## GitHub

```bash
gh auth status
```

```bash
gh api repos/NLH-NQUOC-LABS/<repo> -q .permissions
```

Repos are `nquoc-user`, `nquoc-it`, `nquoc-design`, and `nquoc-backend`, which
lives in the `NLH-NQUOC-CORE` org. You need `push: true` to push branches.

- A 404 right after someone "added you" usually means the **invitation is
  pending**. Find it with `gh api user/repository_invitations`, and ask before
  accepting anything. Accepting unrelated invitations is not your call.
- `git ls-remote origin` failing with "Repository not found" is the same issue
  showing up through git.
- Branch protection shows 404 without admin rights. That is not proof it is off.

### `read:packages`

No longer needed for module repos: the private `@nlh-nquoc-labs/shell` package
is gone and modules have no private dependencies. You only need it to read or
deprecate the old package. If you do, `gh auth refresh -s read:packages` waits
for Enter before it starts polling; run it with stdin closed so it polls
straight away, give the user the code and `https://github.com/login/device`:

```bash
gh auth refresh -h github.com -s read:packages > "$TEMP/ghrefresh.log" 2>&1 < /dev/null
```

## Cloudflare

- The account is **NhiLe Holding** (`a0b2a55f…`). It may be logged in on only one
  machine. Ask where, and run `wrangler` commands there instead of a fresh login.
- `wrangler login --browser=false` in the background times out within minutes,
  and the link dies. If a login is needed on this machine, the user runs
  `npx wrangler@4 login` in their own terminal, where it opens the browser itself.
- Before any deploy, have the user paste `npx wrangler@4 whoami`. It must show
  the right account, and the scopes must include `workers (write)`.
- Workers Builds (the dashboard Git integration) report as GitHub check runs
  named `Workers Builds: <worker>`. Use these to watch module builds without
  dashboard access.
- Module domains (`preview.<m>.nquoc.vn`, `<m>.nquoc.vn`) come from
  `routes = [{ pattern = "...", custom_domain = true }]` in `wrangler.toml`.
  The deploy token needs permission to edit DNS on the `nquoc.vn` zone; if the
  domain is already attached to that Worker, the deploy just keeps it.
- Switching a module on or off needs **no Cloudflare access**: it is the
  `enabled` flag in nquoc-user's `src/app/config/embedded-modules.ts`. Cloudflare
  access is needed for module Workers, custom domains and the emergency
  Rollback button on `nquoc-user-dev` / `nquoc-user-prod`.
- **A custom domain can belong to one Worker only.** Adding `preview.nquoc.vn`
  to `nquoc-user-dev` while it is still on `nquoc-proxy-dev` fails with
  "Hostname already in use by other custom domain". Remove it from the proxy
  first, then add it to nquoc-user straight away (1–3 minutes without the site).

## Supabase

| Project | Ref | Used by |
| --- | --- | --- |
| production | `yaxssarmqevxsbfsatxn` | `nquoc.vn`, `*-prod` Workers |
| staging | `myuhrgwsavyuukgqltog` | `preview.nquoc.vn`, `*-dev` Workers |

Authentication → URL Configuration → Redirect URLs needs only the nquoc-user
origin wildcards (`https://preview.nquoc.vn/**`, `https://nquoc.vn/**`).
Embedded modules never sign in, so they need no redirect URL. Old per-module
entries (`/n-it/auth-callback`, `/n-design/auth-callback`) can be removed once
both modules are embedded. Never change Site URL.

## nquoc-backend

`CORS_ORIGIN` (Railway env) lists allowed origins. `src/app/server.ts` also
appends `'*'` today, so module domains work without a change — add them to
`CORS_ORIGIN` anyway. Removing the `'*'` (it echoes any origin with
credentials) is a separate security task; do it only with the module domains
already listed.

## The machine you are on

- Git Bash on Windows rewrites `origin/dev:path`, so set `export MSYS_NO_PATHCONV=1`
  before any `git show <ref>:<path>`.
- A broken global pnpm is common. Use `npx -y pnpm@10.10.0 …` or the binaries in
  `node_modules/.bin`.
- **A repo copied from another machine (a zip) has broken pnpm symlinks.**
  Scripts that go through `node_modules/<pkg>` links, such as `tsup` in
  `packages/shell`, fail. Build with a repo that has a hoisted install instead
  (esbuild + tsc from nquoc-design worked), or reinstall.
- `cmd.exe` on the user's side does not support `&&` chains reliably in their
  setup. Give one command per code block.
