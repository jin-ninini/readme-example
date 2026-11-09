# 🧭 Harness

> Claude Code harness that keeps Karpathy-style working principles enforced, even in long sessions.

Rules live in `CLAUDE.md`; hooks in `.claude/settings.json` re-inject and enforce them so they do not fade as the conversation grows.

<br>

## Techniques

| # | Technique | What it does | Prevents |
|---|---|---|---|
| 1 | Think Before Coding | Ask or list interpretations and trade-offs; stop when unsure | Silent assumptions |
| 2 | Simplicity First | Minimum code, no speculative options or abstractions | Overcomplication |
| 3 | Surgical Changes | Touch only what was asked; every changed line traces to the request | Collateral edits |
| 4 | Goal-Driven Execution | Verifiable success criteria and a `step → verify` plan | Vague "done" |
| 5 | Role Separation | Planner / Generator / Evaluator in separate contexts | Self-grading |
| 6 | Contract First | Testable Definition of Done agreed before code | Moving goalposts |
| 7 | State on Disk | Progress and decisions in `PROGRESS.md` / `DECISIONS.md`; local commits per verified step; fresh session before overload | Lost context in long sessions |
| 8 | Session Start | `git log`, smoke test, and re-verification before new work | Building on a broken or falsely "done" base |
| 9 | Proof Before Passing | Check a DoD item only after reading the evidence; never weaken an item | Premature victory |
| 10 | One Task at a Time | New requests go to `Next`; the current task finishes first | One-shot overreach |
| 11 | Operator Controls | `AGENT_STOP` kill switch and one-shot `STEER.md` messages | No way to stop or redirect a long run |
| 12 | Repository as System of Record | Chat decisions go to the repo; `CLAUDE.md` stays a short map; docs change with the code | Knowledge lost in chat; stale docs |
| 13 | Garbage Collection | Drift goes to `## Tech Debt` and is cleaned up in small steps; repeated mistakes become hooks or tests | Bad patterns spreading |

<br>

## Structure

```text
harness/
├── CLAUDE.md                 # Always-on working rules
├── PROGRESS.md               # Task, contract (DoD), plan, status — template
├── DECISIONS.md              # Append-only decision log — template
└── .claude/
    ├── settings.json         # Hook registration + destructive-command permissions
    ├── hooks/
    │   ├── context.py        # Re-injects rules and state (every prompt, session start, after compaction)
    │   ├── operator_controls.py  # AGENT_STOP kill switch + STEER.md steering
    │   ├── contract_gate.py  # Blocks edits until a Definition of Done exists
    │   └── stop_gate.py      # Blocks stopping until PROGRESS.md is updated
    └── agents/
        ├── planner.md        # Read-only: interpretations, contract, plan
        └── evaluator.md      # Read-only: verifies against the contract
```

<br>

## Principles → Enforcement

| Principle | `CLAUDE.md` | Mechanism |
|---|---|---|
| Think Before Coding | §1 | `context.py` reminder · `planner` lists interpretations |
| Simplicity First | §2 | `context.py` reminder · `evaluator` overkill check |
| Surgical Changes | §3 | `context.py` reminder · `evaluator` diff check |
| Goal-Driven Execution | §4 | `step → verify` plan in `PROGRESS.md` |
| Role Separation | §5 | `planner` / main session / `evaluator` in separate contexts |
| Contract First | §6 | `contract_gate.py` denies edits without an open DoD item |
| State on Disk | §7 | `stop_gate.py` · `context.py` reloads state and warns on long sessions |
| Session Start | Session Start | `context.py` session reminder · `## Smoke Test` in `PROGRESS.md` |
| Proof Before Passing | §6 | `evaluator` opens evidence, flags weakened DoD items, starts with `PASS` / `NEEDS_WORK` |
| One Task at a Time | §4 | `context.py` reminder |
| Operator Controls | Operator Controls | `operator_controls.py` |
| Repository as System of Record | §8 | `context.py` reminder · `evaluator` docs-in-sync check |
| Garbage Collection | §8 | `## Tech Debt` in `PROGRESS.md` |
| Writing / Design | Writing and Design | `english-writing` and `apple-design` skills (see [SETUP.md](../SETUP.md)) |
| Safety | Safety | `permissions.ask` for push, `reset --hard`, `clean`, `branch -D`, `rm -rf` |

<br>

## Installation

Requires `python3` and `git`. Copy the contents of `harness/` into the target project root.

```bash
git clone --depth 1 https://github.com/jin-ninini/readme-example /tmp/readme-example
cp -rn /tmp/readme-example/harness/{CLAUDE.md,PROGRESS.md,DECISIONS.md,.claude} /path/to/project/
```

If the project already has `CLAUDE.md` or `.claude/settings.json`, merge instead of overwriting (see [SETUP.md](../SETUP.md)).
Restart Claude Code and run `/hooks` to confirm the hooks are loaded.

<br>

## Usage

0. Write the project's smoke-test command under `## Smoke Test` in `PROGRESS.md`.
1. Ask for a task. Claude asks about ambiguities, or delegates to `planner`.
2. Agree the Definition of Done; Claude writes it to `PROGRESS.md`. Edits are blocked until then.
3. Claude implements the `step → verify` plan and records progress.
4. Ask Claude to run `evaluator` for the final PASS/FAIL table.
5. When the long-session warning appears, run `/clear` — the new session resumes from `PROGRESS.md`.
6. To stop a run, create `AGENT_STOP` in the project root. To redirect it, write a note to `STEER.md`.

<br>

## Notes

- Edits made through shell commands (`sed`, `>`) bypass `contract_gate.py`; `CLAUDE.md` asks Claude to use Edit/Write.
- The long-session warning uses transcript file size (`TRANSCRIPT_WARN_BYTES` in `context.py`) as a rough proxy for context usage.
- On Windows, replace `python3` with `python` in `.claude/settings.json` if needed.
- For an unattended loop, Claude Code's built-in `/goal` command checks a completion condition after every turn, for example `/goal every Definition of Done item in PROGRESS.md is checked with evidence`.
- After each model upgrade, disable harness pieces one at a time and keep only what still prevents failures.
- Sources: [Harness engineering (OpenAI)](https://openai.com/index/harness-engineering/), [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), [anthropics/cwc-long-running-agents](https://github.com/anthropics/cwc-long-running-agents), and [nexu-io/harness-engineering-guide](https://github.com/nexu-io/harness-engineering-guide).
