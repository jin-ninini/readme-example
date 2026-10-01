"""Stop gate: if files changed this turn after PROGRESS.md was last updated, record progress before stopping."""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
STATE_FILES = {"PROGRESS.md", "DECISIONS.md"}


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_files():
    try:
        top = git("rev-parse", "--show-toplevel").strip()
        out = git("status", "--porcelain", "-uall", "--", ".")
    except (OSError, subprocess.CalledProcessError):
        return []  # not a git repo — do not block
    files = []
    for line in out.splitlines():
        # Porcelain paths are relative to the repo root, which may sit above the project dir.
        path = os.path.join(top, line[3:].split(" -> ")[-1].strip('"'))
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if rel not in STATE_FILES and os.path.isfile(path):
            files.append(rel)
    return files


def mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    if event.get("stop_hook_active"):
        return  # already blocked once — avoid a loop
    # Only files touched this turn count: pre-existing uncommitted changes must not block Q&A turns.
    # context.py marks the turn start on UserPromptSubmit.
    turn_marker = os.path.join(tempfile.gettempdir(), "claude-harness-%s.turn" % event.get("session_id", ""))
    cutoff = max(mtime(os.path.join(ROOT, "PROGRESS.md")), mtime(turn_marker))
    stale = [f for f in changed_files() if mtime(os.path.join(ROOT, f)) > cutoff]
    if not stale:
        return
    reason = ("State on disk: these files changed after PROGRESS.md was last updated: "
              + ", ".join(stale[:10])
              + ". Update PROGRESS.md (Status with evidence, Definition of Done checkboxes, Next) "
              "and log any decision in DECISIONS.md before stopping. "
              "Check a DoD item only with real command output; use the evaluator subagent for the final check.")
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
