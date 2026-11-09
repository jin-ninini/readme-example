---
name: english-writing
description: English writing rules for README.md and other project docs, based on the Google developer documentation style guide and the Microsoft Writing Style Guide. Use whenever you write, rewrite, or review English prose in README.md, docs, comments meant for readers, or commit/PR text.
---

# English Writing

Rules for English prose in this project. Sources:

- [Google developer documentation style guide](https://developers.google.com/style/) ([highlights](https://developers.google.com/style/highlights))
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) ([top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice))

## Precedence

1. **Template first.** When writing `README.md`, keep the template's section order, headings, and the rules in its top HTML comment (for example, Title Case headings and no trailing period on bullets). Both guides say project style overrides them.
2. **This guide** for everything the template does not decide: the sentences you write inside each section.
3. Spelling: US English, [Merriam-Webster](https://www.merriam-webster.com/).

## Voice and tone

- Write like a knowledgeable friend: clear, direct, and respectful. Not pushy, not cute
- Get to the point. Put the most important information first
- Use bigger ideas and fewer words. Cut every word that adds nothing
- Avoid jargon, buzzwords, slang, idioms, pop-culture references, and exclamation points
- Don't write "simply," "just," "easy," "quickly," or "obviously." What is easy for you may not be easy for the reader
- Don't use "please" in instructions. Write "Run `make`," not "Please run `make`"
- Drop filler: "please note," "at this time," "in order to" (use "to"), "it should be noted that"
- Don't pre-announce features. Document what exists now

## Sentences

- Use active voice. Make clear who or what performs the action
  - ✅ "The script downloads the dataset"
  - ❌ "The dataset is downloaded by the script"
- Use present tense. "The model returns a score," not "The model will return a score"
- Address the reader as "you." Use imperatives for steps ("Install the dependencies")
- Avoid "we" except when the authors speak as a group, and make the group clear
- Start statements with a verb when you can. Remove "you can" and "there is/are" when the sentence works without them
  - ✅ "Run `python train.py` to train the model"
  - ❌ "There is a script that you can run to train the model"
- Put the condition before the instruction: "To retrain, run `python train.py`"
- One idea per sentence. Keep most sentences under 25 words, but don't make them choppy
- Use contractions in prose (it's, don't, you'll). Microsoft recommends them, and Google allows them. Don't contract in tables or code
- Use the same word for the same thing every time. Don't switch between "dataset," "data," and "corpus" for one thing

## Headings

- Follow the template's heading case in `README.md` (Title Case). Elsewhere, both guides default to sentence case
- No period or colon at the end of a heading
- Make headings describe the content ("Getting Started," not "Info")

## Lists and tables

- Numbered lists for steps in order. Bulleted lists for everything else
- Keep list items parallel: all start with a verb, or all start with a noun
- In `README.md`, start bullets with a capital letter and leave off the trailing period (template rule)
- Introduce a list or table with a sentence or a heading, not by itself
- Use a table only for data with two or more dimensions

## Punctuation and numbers

- Use the serial (Oxford) comma: "data, models, and results"
- Use one space after a period
- Use unspaced em dashes for asides ("the model—a gradient-boosted tree—runs on CPU"), or rewrite with commas
- Spell out zero through nine in prose; use numerals for 10 and up, and for all measurements, versions, and metrics ("3 GB," "Python 3.11," "0.92 F1")
- Use unambiguous dates: "November 9, 2026" or `2026-11-09`, never "11/09/26"
- Define an abbreviation on first use: "exploratory data analysis (EDA)." Skip it for common ones (API, CPU, URL)

## Code and UI

- Put code, commands, file names, paths, flags, and package names in `code font`
- Put commands in fenced code blocks with a language (`bash`, `python`). Show only commands that exist and work
- Use **bold** for UI elements the reader clicks, such as **Run** or **Settings**
- Don't use code font for product names (Python, PyTorch, GitHub)

## Links

- Use descriptive link text that says where the link goes: "see [the setup guide](SETUP.md)"
- Never use "click here," "this link," "this article," or a bare URL as link text
- Put key words at the start of the link text, and keep punctuation outside the link

## Inclusive and global language

- Write for a global audience: plain words, short sentences, no culture-specific references
- Use gender-neutral terms. Use "they" for a person whose pronouns you don't know
- Prefer neutral technical terms: "primary/replica" (not "master/slave"), "allowlist/denylist" (not "whitelist/blacklist"), "stop responding" (not "hang")
- Add alt text to every image: `![Confusion matrix of the final model](images/cm.png)`

## Review checklist

Before you finish, read the text aloud once and check:

- [ ] Template structure and its comment rules are intact
- [ ] Active voice, present tense, "you"
- [ ] No filler words, no "simply/just/easy/please"
- [ ] Serial commas, consistent terms, defined abbreviations
- [ ] Code font for code, descriptive link text, alt text on images
- [ ] Every command and number is real and current
