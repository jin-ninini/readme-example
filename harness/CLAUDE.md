# Working Rules

These rules apply to every task in this repository.
Hooks in `.claude/hooks/` re-inject them on every prompt and after compaction, so they hold in long sessions.

## Workflow

0. **Get bearings** — at session start, follow Session Start below
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
- Prefer well-known, stable ("boring") dependencies you can reason about from the repo.
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
- Validate data shapes at boundaries (file loading, API responses). Never build on a guessed shape.
- Work on one task at a time. If a new request arrives mid-task, add it to `Next` in `PROGRESS.md` and finish the current task first, unless the user says to switch.

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
- Never delete, reword, or weaken a DoD item to make it pass. Changing the contract needs the user's agreement.
- Proof before passing: check an item only after you have seen the evidence yourself (read the command output, log, or screenshot). For UI work, test it as a user would (run the app, use the browser), not only with unit tests or `curl`.

## 7. State on Disk

- `PROGRESS.md` — current task, contract, plan, status, next step. Update after each verified step.
- `DECISIONS.md` — append-only log of decisions, alternatives, and reasons.
- Commit locally at each verified checkpoint with a descriptive message, so `git log` is a second record and a bad step can be reverted. Never push without asking.
- When the context-size warning appears, update `PROGRESS.md` and ask the user to start a fresh session (`/clear`) that resumes from it.

## 8. Repository as System of Record

- What is not in the repo does not exist for the next session. Write decisions agreed in chat to `DECISIONS.md` and lasting project knowledge to the docs.
- Keep `CLAUDE.md` a short map (under ~100 lines). Link to deeper docs instead of growing it.
- When a change alters behavior that a doc describes (README commands, structure, results), update the doc in the same change.
- New code copies existing patterns, including bad ones. Do not copy a pattern you would flag; log it under `## Tech Debt` in `PROGRESS.md`.
- When you get stuck, or the user corrects the same thing twice, name what was missing (doc, tool, or check) and propose adding it. Promote a rule that keeps being broken from a doc to a hook, test, or lint.

## Session Start

Before new work in every session (including after `/clear` or compaction):

1. Read `PROGRESS.md` and `DECISIONS.md` (the hook injects them) and run `git log --oneline -10`.
2. Run the command under `## Smoke Test` in `PROGRESS.md`. If it fails, fix that first.
3. Do not trust earlier "done" claims. Re-verify any checked item you build on.

## Writing and Design

- When you write or edit `README.md`, keep the template's structure and the rules in its top comment, and write the prose with the `english-writing` skill (if installed).
- For any UI design task, use the `apple-design` skill (if installed): design in Figma first, show the user the result, and wait for approval before writing UI code.

## Operator Controls

- `AGENT_STOP` file in the project root → every tool call is blocked until it is removed.
- `STEER.md` with content → shown to you once as `OPERATOR STEERING`, then cleared. Treat it as higher priority than your current plan.

## Safety

- Ask before irreversible or shared-impact actions: `git push`, `--force`, `reset --hard`, `rm -rf`, deleting branches, handling secrets.
- Edit files with Edit/Write, not shell redirection, so the contract hook can see the change.
