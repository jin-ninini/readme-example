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
| 7 | State on Disk | Progress and decisions in `PROGRESS.md` / `DECISIONS.md`; fresh session before overload | Lost context in long sessions |

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

1. Ask for a task. Claude asks about ambiguities, or delegates to `planner`.
2. Agree the Definition of Done; Claude writes it to `PROGRESS.md`. Edits are blocked until then.
3. Claude implements the `step → verify` plan and records progress.
4. Ask Claude to run `evaluator` for the final PASS/FAIL table.
5. When the long-session warning appears, run `/clear` — the new session resumes from `PROGRESS.md`.

<br>

## Notes

- Edits made through shell commands (`sed`, `>`) bypass `contract_gate.py`; `CLAUDE.md` asks Claude to use Edit/Write.
- The long-session warning uses transcript file size (`TRANSCRIPT_WARN_BYTES` in `context.py`) as a rough proxy for context usage.
- On Windows, replace `python3` with `python` in `.claude/settings.json` if needed.
