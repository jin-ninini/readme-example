# 🧹 Refactor

> Claude Code skill that reorganizes a Python/ML project into a standard, reusable layout.

<br>

## Structure

```text
refactor/
└── .claude/
    └── skills/
        └── refactor-project/
            └── SKILL.md   # Full refactoring requirements (layout, src/ modules, requirements, README)
```

<br>

## Installation

Copy the skill into the target project.

```bash
git clone --depth 1 https://github.com/jin-ninini/readme-example /tmp/readme-example
mkdir -p /path/to/project/.claude/skills
cp -r /tmp/readme-example/refactor/.claude/skills/refactor-project /path/to/project/.claude/skills/
```

<br>

## Usage

Run `/refactor-project` in Claude Code. It runs only when invoked (`disable-model-invocation: true`).

Result:

```text
project/
├── data/
├── src/
├── models/
├── requirements.txt
├── README.md
├── train.py
├── valid.py
└── test.py
```
