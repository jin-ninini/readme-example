"""PreToolUse gate: no file edits until PROGRESS.md holds an agreed, open Definition of Done item."""
import json
import os
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
# State files and harness config can always be edited — that is how the contract gets written.
EXEMPT_FILES = {"PROGRESS.md", "DECISIONS.md", "CLAUDE.md"}
EXEMPT_DIRS = (".claude",)


def is_exempt(path):
    rel = os.path.relpath(os.path.abspath(os.path.join(ROOT, path)), ROOT).replace(os.sep, "/")
    if rel.startswith("../"):
        return True  # outside the project (e.g. scratch files)
    return rel in EXEMPT_FILES or rel.split("/")[0] in EXEMPT_DIRS


def has_open_contract():
    try:
        with open(os.path.join(ROOT, "PROGRESS.md"), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return False
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip() == "Definition of Done"
            continue
        item = line.strip()
        if inside and item.startswith("- [ ]") and "<criterion>" not in item:
            return True
    return False


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return  # never block on unreadable input
    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path or is_exempt(path) or has_open_contract():
        return
    reason = ("Contract first: PROGRESS.md has no open Definition of Done item. "
              "Agree a testable checklist with the user (e.g. '- [ ] <criterion> — verify: <command>'), "
              "write it under '## Definition of Done' in PROGRESS.md, then edit code.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


if __name__ == "__main__":
    main()
