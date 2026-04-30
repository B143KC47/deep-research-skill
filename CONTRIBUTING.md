# Contributing

Thanks for improving Deep Research.

## Development Setup

This repository has no runtime dependency beyond Python 3.10+.

```bash
python -m unittest discover -s tests
python -m py_compile scripts/research_ledger.py
```

On Windows systems where `python` is the Microsoft Store alias, use `py -m`
for the same commands.

## Change Guidelines

- Keep `SKILL.md` concise and operational.
- Put reusable research guidance in `references/`.
- Keep `scripts/research_ledger.py` portable and standard-library only.
- Add or update tests for ledger behavior changes.
- Avoid committing generated `research_runs/` output unless a fixture is
  deliberately needed.

## Pull Request Checklist

- [ ] Tests pass locally.
- [ ] New commands or workflows are documented in `README.md` or `SKILL.md`.
- [ ] Changes preserve relative links used by the skill.
- [ ] Generated files, caches, and local run outputs are not committed.
