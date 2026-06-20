---
name: dependabot-merge-train
description: Merge open Dependabot PRs safely, one at a time, oldest first — rebasing each onto the freshly-moved main, waiting for green checks, then merging. Use when asked to clear, process, or merge the Dependabot/dependency-update PR queue, or to "run the dependabot merge train".
---

# Dependabot merge train

Merge a queue of open Dependabot PRs serially. Each merge moves `main`, which can
stale or conflict the remaining PRs, so every PR is rebased onto the latest `main`
and re-verified green **before** it is merged.

## Prerequisites

- `gh` CLI authenticated for the repo.
- Authorization to merge to `main` (the user asked you to run the train).

## Procedure

### 0. Survey the queue

```bash
gh pr list --state open --author "app/dependabot" \
  --json number,title,createdAt,reviewDecision,mergeable,mergeStateStatus \
  --jq 'sort_by(.createdAt)'
```

Process **oldest first**. If some PRs are approved (`reviewDecision == "APPROVED"`)
and the user asked to prioritize approved ones, do those first, still oldest-first
within each group.

### 1. Check that `main` itself is green FIRST

Before merging anything, confirm the blocking checks pass on `main` as it stands.
A red check on a Dependabot PR is often **not** caused by the bump — it is a
pre-existing `main` problem surfacing on the PR. Common cause in this repo:

- The `Code quality` workflow (`.github/workflows/biome.yml`) runs `biome ci`.
  If `with: version:` is `latest` (unpinned), the Biome **CLI** drifts to newer
  releases with stricter lint rules even though the `setup-biome` **action** SHA
  is pinned. (These are two different versions — the `@<sha> # vX` pins the
  action; `with: version:` pins the CLI binary it installs.)

Reproduce a suspected check failure locally to find the real cause, e.g.:

```bash
npx @biomejs/biome@latest ci ./src   # what CI runs when version: latest
npx @biomejs/biome ci ./src          # what the pinned local dep runs
```

If `main` is red, **fix the root cause in its own PR and merge that first**, then
run the train. Do not try to merge dependency PRs on top of a broken `main`.

### 2. Merge the oldest PR

```bash
gh pr checks <N>          # confirm all required/blocking checks pass
gh pr merge <N> --merge --delete-branch
```

Use `--merge` (merge commit) to match this repo's history. Confirm:

```bash
gh pr view <N> --json state --jq .state   # expect MERGED
```

### 3. For each remaining PR: rebase → wait green → merge

After a merge, `main` has moved. The next PR is almost always **behind** `main`,
and may now **conflict** (PRs that touch the same files — e.g. several touching
`package.json` / `pnpm-lock.yaml` — will conflict once one of them lands).

GitHub recomputes mergeability asynchronously; right after a merge a PR shows
`mergeable=UNKNOWN`. Poll until it settles, then:

**Rebase the PR if it is behind `main` OR conflicting.** Dependabot's auto-rebase
is slow and unreliable, so trigger it explicitly — this both resolves conflicts
and pulls in any `main` fixes (like the Biome pin) so checks can go green:

```bash
OLD=$(gh pr view <N> --json headRefOid --jq '.headRefOid[0:7]')
gh pr comment <N> --body "@dependabot rebase"
```

> Key lesson: rebase is needed even with **no merge conflict** when a sibling
> merge changed CI-relevant state. The rule is "rebase if behind OR conflicted",
> not "rebase only on conflict".

Wait for Dependabot to push the rebased commit (head changes off `$OLD`), then
wait for checks to finish, then verify green and merge:

```bash
# wait for rebase (head moves)
until [ "$(gh pr view <N> --json headRefOid --jq '.headRefOid[0:7]')" != "$OLD" ]; do sleep 10; done
# wait for checks to settle
until ! gh pr checks <N> 2>/dev/null | grep -qi pending; do sleep 10; done
gh pr checks <N>                                                  # confirm all pass
gh pr view <N> --json mergeable,mergeStateStatus                  # expect MERGEABLE / CLEAN
gh pr merge <N> --merge --delete-branch
```

If checks come back **red after** a clean rebase, stop and report — that failure
is real (caused by the bump), not drift. Do not merge.

Repeat step 3 for every remaining PR.

### 4. Finish

```bash
git checkout main && git pull --ff-only
gh pr list --state open --author "app/dependabot"   # confirm queue is empty
```

## Notes

- Run the long rebase/checks waits as background commands; foreground `sleep`
  loops may be blocked by the harness.
- `--delete-branch` keeps the Dependabot branch list clean.
- If `@dependabot rebase` produces no new commit within ~10 min, Dependabot may
  be paused or the PR un-rebaseable — report to the user instead of looping.
