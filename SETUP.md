# Setup for Claude Code

When a user gives you the link `https://github.com/jin-ninini/readme-example`, apply this repository to their project as follows.

| Component | Source | Applies |
|---|---|---|
| Harness | `harness/` | Working rules + hooks (`CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`) |
| Refactor | `refactor/` | `/refactor-project` skill |
| Writing | `writing/` | `english-writing` skill (English prose rules for `README.md` and docs) |
| Design | `design/` | `apple-design` skill (Apple-style design, built in Figma and approved before UI code) |
| README template | `README.md` | Style and structure for the project's README |

Apply all of them unless the user asks for only some.

## 1. Fetch

```bash
git clone --depth 1 https://github.com/jin-ninini/readme-example /tmp/readme-example \
  || git -C /tmp/readme-example pull --ff-only
```

## 2. Install the harness

First check which targets already exist (`cp -n` skips them silently):

```bash
ls -d CLAUDE.md PROGRESS.md DECISIONS.md .claude/settings.json 2>/dev/null
```

Copy into the project root without overwriting existing files:

```bash
cp -rn "/tmp/readme-example/harness/"{CLAUDE.md,PROGRESS.md,DECISIONS.md,.claude} .
```

If a file already existed, merge instead:

- `CLAUDE.md` — append the harness rules as a new section; keep the existing content.
- `.claude/settings.json` — add the harness entries to `permissions.ask` and each `hooks` event array; keep existing entries.
- `PROGRESS.md` / `DECISIONS.md` — keep the existing files.

## 3. Install the skills

```bash
mkdir -p .claude/skills
for kit in refactor/.claude/skills/refactor-project \
           writing/.claude/skills/english-writing \
           design/.claude/skills/apple-design; do
  cp -rn "/tmp/readme-example/$kit" .claude/skills/
done
```

Do not run the refactor now. The user triggers it with `/refactor-project`.
`english-writing` and `apple-design` load automatically when Claude writes docs or designs UI. `apple-design` needs the Figma MCP server.

## 4. Verify

```bash
python3 -m json.tool .claude/settings.json > /dev/null && echo "settings OK"
echo '{"tool_input":{"file_path":"x.py"}}' | python3 .claude/hooks/contract_gate.py   # expect "deny" (unless PROGRESS.md already has an open item)
```

Then tell the user:

- which files were added or merged
- to restart Claude Code (or run `/hooks`) so the hooks load
- that code edits are blocked until a Definition of Done is written in `PROGRESS.md`
- to fill in `## Smoke Test` in `PROGRESS.md`
- that UI design happens in Figma and waits for their approval before code
