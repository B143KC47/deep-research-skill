# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)

Adaptive, auditable research workflow for AI agents. This repository packages a
Codex-compatible skill, reference protocols, agent metadata, and a small
standard-library ledger tool for tracking research hops, sources, evidence, and
uncertainty.

GitHub: [B143KC47/deep-research-skill](https://github.com/B143KC47/deep-research-skill)

## What This Is

Deep Research helps an agent answer questions that need more than a quick lookup:
literature reviews, GitHub project due diligence, source verification, current
technical research, cited reports, and decisions that require counterevidence.

The workflow is intentionally evidence-first:

- plan the information need;
- retrieve or inspect sources;
- record meaningful research hops;
- attach reusable evidence IDs to claims;
- check source quality and contradictions;
- synthesize with explicit uncertainty.

## Repository Layout

```text
.
├── SKILL.md                         # Skill entrypoint and operating guide
├── agents/
│   └── openai.yaml                  # Agent display metadata
├── references/
│   ├── bibliography.md              # Design rationale references
│   ├── evaluation.md                # Run audit checklist
│   ├── openclaw-install.md          # OpenClaw installation notes
│   ├── project-and-paper-patterns.md# GitHub/paper inspection patterns
│   ├── query-playbook.md            # Search query patterns
│   ├── report-template.md           # Final report template
│   ├── research-protocol.md         # Adaptive research protocol
│   └── source-quality.md            # Source credibility rubric
├── scripts/
│   └── research_ledger.py           # Research run state manager
└── tests/
    └── test_research_ledger.py      # Standard-library regression tests
```

## Quick Start

Create a research run:

```bash
python scripts/research_ledger.py init \
  --question "Which open-source vector database should we evaluate?" \
  --out-dir research_runs \
  --effort deep \
  --deliverable "evidence-backed recommendation"
```

Add a research hop:

```bash
python scripts/research_ledger.py add-hop \
  --run-dir research_runs/<run-dir> \
  --hop 1 \
  --mode seed \
  --tool-or-source web \
  --query-or-action "search: official docs and benchmark pages" \
  --result-summary "Identified primary docs and benchmark sources" \
  --next-questions "Check implementation evidence and limitations"
```

Add evidence:

```bash
python scripts/research_ledger.py add-evidence \
  --run-dir research_runs/<run-dir> \
  --hop 1 \
  --source-id S001 \
  --title "Project documentation" \
  --url-or-path "https://example.com/docs" \
  --publisher-or-owner "Example Project" \
  --source-type official-doc \
  --quality-score 5 \
  --stance supports \
  --claim "The project supports the required deployment mode" \
  --quote-or-locator "Docs: deployment section"
```

Check status or lint the run before writing the final report:

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## Effort Levels

- `quick`: 2-4 meaningful hops for low-risk orientation.
- `standard`: 5-8 hops across at least three source classes.
- `deep`: 9-14 hops for broad synthesis and due diligence.
- `exhaustive`: 15+ hops for contested, high-stakes, or user-budgeted work.

Hop counts are planning targets, not quotas. Stop when high-impact claims are
supported and remaining gaps are explicit.

## Development

The ledger script uses only the Python standard library.

On Windows, if `python` opens the Microsoft Store or exits without output, use
`py -m` for module commands. For example:

```powershell
py -m unittest discover -s tests
```

Run tests:

```bash
python -m unittest discover -s tests
```

Run a syntax check:

```bash
python -m py_compile scripts/research_ledger.py
```

## Installation As A Skill

For Codex-style skill usage, place this directory under your skills directory
and keep `SKILL.md` at the repository root. The skill body references files by
relative path, so the directory structure should stay intact.

Install from GitHub with the Codex skill installer:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

Or clone directly:

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
```

## License

MIT. See [LICENSE](LICENSE).
