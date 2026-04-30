# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)

**言語:** [English](../README.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | 日本語 | [한국어](README.ko.md)

AI エージェント向けの、適応的で監査可能な deep research skill です。幅広い探索から引用付きの統合へ進む過程で、情報源、主張、反証、不確実性を追跡できます。

> 調査メモ、文献レビュー、GitHub プロジェクトのデューデリジェンス、情報源の検証、最新技術調査、短い検索では足りない意思決定に向いています。

## 特長

- **Evidence ledger**: 調査ステップ、情報源、主張、evidence ID を記録します。
- **適応型プロトコル**: 証拠の変化に応じて、広げる、深掘りする、検証する、止めるを判断します。
- **情報源の品質チェック**: 一次情報、背景情報、弱い主張、反証、古い事実を区別します。
- **ポータブル CLI**: ledger ツールは Python 標準ライブラリのみで動作します。
- **Marketplace 対応**: `SKILL.md`、エージェント metadata、参考資料、テストを含みます。

## インストール

`skills.sh` を使う場合:

```bash
npx skills add B143KC47/deep-research-skill
```

Codex skill installer を使う場合:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

直接 clone する場合:

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
```

## クイックスタート

調査 run を作成:

```bash
python scripts/research_ledger.py init \
  --question "Which open-source vector database should we evaluate?" \
  --out-dir research_runs \
  --effort deep \
  --deliverable "evidence-backed recommendation"
```

調査 hop を記録:

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

証拠を追加:

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

最終レポート前の確認:

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## 調査フロー

| フェーズ | エージェントの作業 | 出力 |
|---|---|---|
| Frame | 質問、意思決定、範囲、鮮度要件を整理します。 | 調査計画 |
| Map | トピックを観点、情報源の種類、不明点に分解します。 | Aspect map |
| Seed | 深掘りの前に複数の探索ルートを試します。 | 初期 source graph |
| Extract | 主張、位置情報、日付、バージョン、品質を記録します。 | Evidence ledger |
| Verify | 矛盾、古い事実、独立した裏付けを探します。 | 信頼度ラベル |
| Synthesize | Evidence ID と不確実性を明示して回答します。 | 引用付きレポート |

## Effort Levels

| レベル | 用途 | 目安 |
|---|---|---|
| `quick` | 低リスクの確認 | 2-4 meaningful hops |
| `standard` | 通常の調査回答 | 5-8 hops、3+ source classes |
| `deep` | 文献レビュー、due diligence、広い統合 | 9-14 hops、4+ source classes |
| `exhaustive` | 重要、議論のある、または予算指定の調査 | 15+ hops、5+ source classes |

## 開発

```bash
python -m unittest discover -s tests
python -m py_compile scripts/research_ledger.py
```

Windows で `python` が Microsoft Store を開く、または出力しない場合:

```powershell
py -m unittest discover -s tests
py -m py_compile scripts\research_ledger.py
```

## Marketplace

- GitHub repository: <https://github.com/B143KC47/deep-research-skill>
- Raw skill file: <https://raw.githubusercontent.com/B143KC47/deep-research-skill/main/SKILL.md>
- ClawHub slug: `b143kc47-deep-research`

## ライセンス

MIT。詳しくは [LICENSE](../LICENSE) を参照してください。
