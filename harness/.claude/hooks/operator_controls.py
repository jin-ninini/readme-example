"""PreToolUse operator controls (from anthropics/cwc-long-running-agents).

AGENT_STOP — while this file exists in the project root, every tool call is denied (kill switch).
STEER.md   — if it has content, deny the next tool call once with that content as steering, then clear it.
This is a convenience channel, not a trust boundary: the agent can write these files itself.
"""
import json
import os
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
STOP_FILE = os.path.join(ROOT, "AGENT_STOP")
STEER_FILE = os.path.join(ROOT, "STEER.md")


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


def main():
    try:
        json.load(sys.stdin)
    except ValueError:
        pass
    if os.path.exists(STOP_FILE):
        deny("Kill switch engaged: AGENT_STOP exists in the project root. Stop working and tell the user. "
             "Do not remove the file yourself.")
        return
    try:
        with open(STEER_FILE, encoding="utf-8") as f:
            note = f.read().strip()
    except OSError:
        return
    if not note:
        return
    try:
        open(STEER_FILE, "w").close()  # deliver once
    except OSError:
        pass
    deny("OPERATOR STEERING: " + note + "\n\nPause what you were about to do, incorporate this guidance, "
         "update PROGRESS.md if the plan changes, then continue.")


if __name__ == "__main__":
    main()
