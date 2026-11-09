# 🎨 Design

> Claude Code skill for Apple-style UI design that is built in Figma and approved by you before any UI code is written.

<br>

## Structure

```text
design/
└── .claude/
    └── skills/
        └── apple-design/
            └── SKILL.md   # Figma-first workflow, review checklist, and Apple design principles
```

<br>

## Installation

Requires the Figma MCP server in Claude Code. Copy the skill into the target project.

```bash
git clone --depth 1 https://github.com/jin-ninini/readme-example /tmp/readme-example
mkdir -p /path/to/project/.claude/skills
cp -r /tmp/readme-example/design/.claude/skills/apple-design /path/to/project/.claude/skills/
```

<br>

## Usage

Ask for a screen or component. Claude loads the skill and follows this workflow:

1. Clarifies the target and any existing Figma file
2. Builds the design in Figma using the skill's principles
3. Reviews a screenshot against the checklist
4. Shares the Figma link and waits for your approval
5. Writes UI code only after you approve

<br>

## Notes

- Design knowledge comes from [emilkowalski/skills `apple-design`](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) (MIT License, Copyright © 2026 Emil Kowalski)
- To skip Figma for a task, say so explicitly
