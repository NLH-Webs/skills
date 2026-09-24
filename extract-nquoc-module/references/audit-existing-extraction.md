# Auditing an extraction someone else did

> **Kit update (2026-09-16):** add one check to the list — `pnpm kit:diff`
> against `nquoc-module-template`. Any drift in a kit file is either a missing
> `pnpm kit:sync` or an undocumented exception (`kit-exceptions.json`).

Use this when a module repo arrives as a zip, from another machine, or as a set
of PRs, and the question is "is it done, and what is left". The N-Design audit
followed this order. Its reports were mostly accurate, and the things they
missed are below.

## 1. Where things really are

Do this per repo:

```bash
git -C <repo> branch -a -vv
```

```bash
git -C <repo> log --oneline --all --graph | head -30
```

```bash
git -C <repo> status --short
```

- **The checkout is often not the tip.** N-Design's working tree was on branch
  3 of a 5-branch stack. Audit the tip.
- Compare `origin/dev` with the stack. Nothing may have reached `dev` at all.
- Other people's branches in the repo can be unrelated projects. N-Design had
  nine `ui/*` HTML demos on top of the Readme commit. Report them; do not touch them.
- The local `origin/*` refs are only as fresh as the zip. `git fetch` when you
  have access, and check access first (`access-checklist.md`).

## 2. Re-run everything instead of trusting the reports

```bash
node_modules/.bin/tsc -p tsconfig.app.json --noEmit
```

```bash
node_modules/.bin/eslint .
```

```bash
node scripts/openapi-contract-check.mjs --check
```

```bash
node_modules/.bin/vite build
```

- Drift against `nquoc-user origin/dev`: use `scripts/drift-by-basename.cjs`
  when there is no `filemap.json`. Every DIFF needs a named reason.
- Check whether the legacy source moved on `dev` after the migration:
  `git -C nquoc-user log --since=<migration date> origin/dev -- src/pages/<Module> src/components/order-*`.
- Guardrail probes (`guardrails.md`), including `fetch()`, which is not blocked.
- Grep for `navigate('/`, `href="/`, and `window.location` inside
  `modules/**` and `shared/**`.
- Grep for the previous module's name (`n-it`, `N-IT`, `NIT_`, `preview.it`) in
  `src`, `deploy`, `scripts`, `README`, and `CLAUDE.md`.

## 3. What copied repos got wrong

| Look for | Found on N-Design (proxy era) / what to check now |
| --- | --- |
| A `deploy/reverse-proxy`, `platform/` or proxy config in the module repo | There must be none |
| `@nlh-nquoc-labs/shell`, an `AppShell`, a sidebar or a logout button in the module | nquoc-user owns the chrome; none in the module |
| Login / auth-callback / reset-password pages, any auth client | Embedded modules never sign in (standalone ones use the kit's auth-central login, never their own) |
| `VITE_BASE_PATH`, `basename`, `dist/<m>/`, `_redirects` | Root build only |
| `embed-protocol.ts` differing from nquoc-user's | Must be byte-identical |
| No `_headers` generated, `frame-ancestors *`, or localhost in a prod build | Only that environment's nquoc-user origins |
| Sentences claiming verification | "Verified locally with wrangler dev", copied from IT, never run |
| Instructions naming resources that never existed | "Rename Worker `nquoc-design-preview`" |
| Numbers from the other module | "audited at 23 files, turned out 103" belonged to N-IT |
| Lint green in one repo, red in the other | The same guardrail fix existed only in nquoc-design |
| Infrastructure files that differ between module repos | 6 files, within a day |

## 4. Live state, before advising deploys

```bash
curl -s -D - -o /dev/null https://preview.nquoc.vn/n-<m>/
```

- `x-nquoc-route: n-<m>` → the old edge proxy still sends the path to the module
  Worker (`rollout.md` §2 first). `nquoc-user…` or no header → nquoc-user answers.
- Whether nquoc-user embeds the module: download its bundle
  (`curl -s https://preview.nquoc.vn/ | grep -oE '/assets/index-[^"]+\.js'`) and
  grep for the module domain (`preview.<m>.nquoc.vn`).
- The module itself: `pnpm run smoke https://preview.<m>.nquoc.vn`; its bundle
  shows the API host and parent origins it was built for.

## 5. Reviews

Run the parity audit and both review prompts (`review-prompts.md`) as parallel
background agents, on detached worktrees. Then reproduce the high-severity
findings in the code yourself before reporting them. On N-Design, every one of
the auth findings held up when traced through the code.

## 6. Report shape

1. **TL;DR.** Is the code good, and has anything reached `dev` or users?
2. **What you re-ran,** with results in a table.
3. **Findings ranked** as blocks-deploy, plan/DoD gaps, then nice-to-fix.
   Each has a concrete scenario.
4. **Proposed order of work.**

Write the audit to `plans/<module>-*.md` so the next session starts from it.
