"""Re-inject the working rules and on-disk state so they survive long sessions.

session — SessionStart (startup, resume, /clear, after compaction): full PROGRESS.md + recent DECISIONS.md
prompt  — UserPromptSubmit: short rule reminder, current task, context-size warning
"""
import json
import os
import sys
import tempfile

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
# Rough heuristic: transcript JSONL size at which the session is getting heavy.
TRANSCRIPT_WARN_BYTES = 1_500_000

REMINDER = """[Harness rules — CLAUDE.md]
1. Think first: ambiguous → ask or list interpretations/trade-offs. Never assume silently.
2. Simplicity: minimum code, nothing speculative. "Would a senior engineer call this overkill?"
3. Surgical: touch only what was asked. "Is every changed line traceable to the request?"
4. Goal-driven: verifiable criteria; multi-step → `step → verify` plan first. One task at a time.
5. Roles: planner / generator (you) / evaluator are separate contexts. Do not grade your own work.
6. Contract first: Definition of Done in PROGRESS.md before code. Never weaken an item to pass it; check it only after you saw the evidence.
7. State on disk: update PROGRESS.md / DECISIONS.md and commit locally after each verified step.
8. Repo is the system of record: log chat decisions to DECISIONS.md, keep docs in sync with behavior, log drift under Tech Debt.
9. README prose → `english-writing` skill. UI design → `apple-design` skill: Figma first, user approval before UI code."""

SESSION_START = """[Session start — CLAUDE.md]
Before new work: run `git log --oneline -10`, run the Smoke Test in PROGRESS.md (fix it first if it fails),
and re-verify any checked DoD item you build on instead of trusting earlier "done" claims."""


def read(name):
    try:
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def section(text, heading):
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip() == heading
            continue
        if inside and line.strip() and not line.strip().startswith("<!--"):
            lines.append(line)
    return "\n".join(lines)


def session_context():
    parts = [REMINDER, SESSION_START]
    progress = read("PROGRESS.md")
    parts.append("[PROGRESS.md]\n" + progress if progress else
                 "[PROGRESS.md] missing — create it from the harness template before starting work.")
    decisions = read("DECISIONS.md")
    if decisions:
        parts.append("[DECISIONS.md — last 40 lines]\n" + "\n".join(decisions.splitlines()[-40:]))
    return "\n\n".join(parts)


def mark_turn_start(event):
    """Touch a per-session marker so stop_gate.py only judges files changed during this turn."""
    marker = os.path.join(tempfile.gettempdir(), "claude-harness-%s.turn" % event.get("session_id", ""))
    try:
        with open(marker, "w"):
            pass
    except OSError:
        pass


def prompt_context(event):
    mark_turn_start(event)
    parts = [REMINDER]
    progress = read("PROGRESS.md")
    task = section(progress, "Current Task")
    dod = section(progress, "Definition of Done")
    if task:
        parts.append("Current task: " + task)
    if dod:
        parts.append("Definition of Done:\n" + dod)
    path = event.get("transcript_path") or ""
    try:
        if path and os.path.getsize(path) > TRANSCRIPT_WARN_BYTES:
            parts.append("[Context warning] This session is long. Update PROGRESS.md (Status, Next) now, "
                         "then suggest the user start a fresh session (/clear) that resumes from it.")
    except OSError:
        pass
    return "\n\n".join(parts)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "prompt"
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    if mode == "session":
        name, ctx = "SessionStart", session_context()
    else:
        name, ctx = "UserPromptSubmit", prompt_context(event)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": name, "additionalContext": ctx}}))


if __name__ == "__main__":
    main()
