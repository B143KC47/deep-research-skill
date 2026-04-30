# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Language:** English | [简体中文](docs/README.zh-CN.md) | [Español](docs/README.es.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md)

Adaptive, auditable deep research for AI agents. This skill helps agents move
from broad discovery to cited synthesis while keeping sources, claims,
counterevidence, and uncertainty traceable.

> Built for research memos, literature reviews, GitHub due diligence, source
> verification, current technical research, and decisions that need more than a
> quick lookup.

## Why Use It

- **Evidence ledger**: track research hops, sources, claims, and evidence IDs.
- **Adaptive protocol**: broaden, deepen, verify, or stop based on what the
  evidence changes.
- **Source-quality checks**: separate primary sources, context, weak claims,
  counterevidence, and stale facts.
- **Portable CLI**: the ledger tool uses only the Python standard library.
- **Marketplace ready**: includes `SKILL.md`, agent metadata, references, tests,
  and submission notes.

## Install

Install with `skills.sh`:

```bash
npx skills add B143KC47/deep-research-skill
```

Install with the Codex skill installer:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

Clone directly:

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
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

Record a meaningful research hop:

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

Attach evidence to a claim:

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

Check readiness before writing the final report:

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## Research Workflow

| Phase | What the agent does | Output |
|---|---|---|
| Frame | Restate the question, decision, scope, and freshness needs. | Research plan |
| Map | Split the topic into aspects, source classes, and unknowns. | Aspect map |
| Seed | Search several distinct routes before diving deep. | Initial source graph |
| Extract | Capture claims, locators, dates, versions, and source quality. | Evidence ledger |
| Verify | Look for contradictions, stale facts, and independent support. | Confidence labels |
| Synthesize | Answer with evidence IDs and explicit uncertainty. | Cited report |

## Effort Levels

| Effort | Typical use | Target |
|---|---|---|
| `quick` | Low-risk orientation or sanity check | 2-4 meaningful hops |
| `standard` | Normal researched answer | 5-8 hops, 3+ source classes |
| `deep` | Literature review, due diligence, broad synthesis | 9-14 hops, 4+ source classes |
| `exhaustive` | High-stakes, contested, or user-budgeted work | 15+ hops, 5+ source classes |

Hop counts are planning targets, not quotas. Stop when high-impact claims are
supported and remaining gaps are explicit.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── docs/
│   └── README.zh-CN.md
│   └── README.es.md
│   └── README.ja.md
│   └── README.ko.md
├── references/
│   ├── research-protocol.md
│   ├── source-quality.md
│   ├── query-playbook.md
│   └── report-template.md
├── scripts/
│   └── research_ledger.py
└── tests/
    └── test_research_ledger.py
```

## Development

The ledger script uses only the Python standard library.

Run tests:

```bash
python -m unittest discover -s tests
```

Run a syntax check:

```bash
python -m py_compile scripts/research_ledger.py
```

On Windows, if `python` opens the Microsoft Store or exits without output, use
`py -m`:

```powershell
py -m unittest discover -s tests
py -m py_compile scripts\research_ledger.py
```

## Marketplace

Useful links:

- GitHub repository: <https://github.com/B143KC47/deep-research-skill>
- Raw skill file: <https://raw.githubusercontent.com/B143KC47/deep-research-skill/main/SKILL.md>
- ClawHub slug: `b143kc47-deep-research`

## License

MIT. See [LICENSE](LICENSE).
