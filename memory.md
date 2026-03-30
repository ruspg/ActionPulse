# Project Memory

Updated: 2026-03-30

## Durable Rules

- Always start from fresh `origin/main`, not local `main`, not detached `HEAD`.
- Run `git fetch origin --prune` before any implementation, Plane updates, or PR creation.
- Stop immediately if `git status --short --branch` does not show a real branch.
- If the worktree cannot fetch because `.git` metadata is outside the writable sandbox, create a fresh clone/worktree inside the writable workspace and work there.
- Do not update Plane issue states or open a PR until the branch base and test baseline are verified on the branch that will actually be used.
- If a PR was opened from stale `main`, close it and restack from fresh `origin/main`. Do not try to salvage bad history.
- Treat live git state, test results, and Plane as the source of truth for current status. This file stores only invariant workflow rules.
- Do not store commit hashes, PR numbers, local paths, or transient verification results here.

## Working Preflight

1. Fetch and confirm current `origin/main`.
2. Ensure work is on a real branch cut from current `origin/main`.
3. Run required baseline checks from that branch.
4. Only then edit code.
5. Only after that update Plane and open a PR.
