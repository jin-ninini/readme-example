# ✍️ Writing

> Claude Code skill that applies the Google and Microsoft style guides to English prose in `README.md` and other docs.

<br>

## Structure

```text
writing/
└── .claude/
    └── skills/
        └── english-writing/
            └── SKILL.md   # Voice, sentences, lists, punctuation, code, links, and a review checklist
```

<br>

## Installation

Copy the skill into the target project.

```bash
git clone --depth 1 https://github.com/jin-ninini/readme-example /tmp/readme-example
mkdir -p /path/to/project/.claude/skills
cp -r /tmp/readme-example/writing/.claude/skills/english-writing /path/to/project/.claude/skills/
```

<br>

## Usage

Claude loads the skill whenever it writes or edits `README.md` or other English docs. You can also run `/english-writing`.

The README template's structure and the rules in its top comment take precedence. The skill governs the sentences inside each section.

<br>

## Notes

- Sources: [Google developer documentation style guide](https://developers.google.com/style/) and [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- Both guides use sentence case for headings, but the README template keeps Title Case as a project rule
