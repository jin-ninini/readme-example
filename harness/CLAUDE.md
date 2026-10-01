# Working Rules

These rules apply to every task in this repository.
Hooks in `.claude/hooks/` re-inject them on every prompt and after compaction, so they hold in long sessions.

## Workflow

1. **Clarify** — resolve ambiguity before touching code
2. **Contract** — agree the Definition of Done in `PROGRESS.md`
3. **Plan** — short `step → verify` list
4. **Generate** — minimal, surgical changes
5. **Evaluate** — in a separate context, against the contract
6. **Record** — update `PROGRESS.md` / `DECISIONS.md`

## 1. Think Before Coding

- Do not assume. If a requirement is ambiguous, ask or present the trade-offs first.
- If several interpretations are possible, list them all. Never pick one silently.
- If you are unsure, stop and name exactly what is unclear.

## 2. Simplicity First

- Write the minimum code that solves the problem. No speculative features.
- Do not add flexibility, options, or configurability that was not requested.
- Self-check: *"Would a senior engineer call this overkill?"* If yes, cut it.

## 3. Surgical Changes

- Touch only what the request requires. Leave adjacent code, comments, and formatting alone.
- Do not refactor code that is not broken.
- Self-check: *"Can every changed line be traced to the user's request?"*

## 4. Goal-Driven Execution

- Turn instructions into verifiable success criteria.
  e.g. "Fix the bug" → "Write a test that reproduces it, then make it pass."
- For multi-step work, post a short plan first:
  ```
  1. <step> → verify: <check>
  2. <step> → verify: <check>
  ```
- Done means proven by real command output, not by confidence.

## 5. Role Separation

Planner, Generator, and Evaluator run in separate contexts so no one grades their own work.

| Role | Runs as | Does |
|---|---|---|
| Planner | `planner` subagent | Reads code, lists interpretations, drafts the contract and plan. No edits. |
| Generator | Main session | Implements the agreed plan. |
| Evaluator | `evaluator` subagent | Checks the result against the contract with real commands. No edits. |

For large tasks, run each role as its own `claude` session and hand off through `PROGRESS.md`.

## 6. Contract First

- Before writing code, agree the Definition of Done with the user as a testable checklist in `PROGRESS.md`.
- Each item names how it is verified (command, test, or observable result).
- A hook blocks file edits while `PROGRESS.md` has no open checklist item.

## 7. State on Disk

- `PROGRESS.md` — current task, contract, plan, status, next step. Update after each verified step.
- `DECISIONS.md` — append-only log of decisions, alternatives, and reasons.
- When the context-size warning appears, update `PROGRESS.md` and ask the user to start a fresh session (`/clear`) that resumes from it.

## Safety

- Ask before irreversible or shared-impact actions: `git push`, `--force`, `reset --hard`, `rm -rf`, deleting branches, handling secrets.
- Edit files with Edit/Write, not shell redirection, so the contract hook can see the change.
