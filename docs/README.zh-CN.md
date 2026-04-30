# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)

**语言:** [English](../README.md) | 简体中文

面向 AI Agent 的自适应、可审计深度研究技能。它帮助 Agent 从广泛检索走向带引用的综合结论，同时保留来源、主张、反证和不确定性。

> 适合研究备忘录、文献综述、GitHub 项目尽调、来源核验、实时技术研究，以及任何不能只靠一两个链接回答的问题。

## 为什么使用

- **证据台账**：记录研究跳转、来源、主张和 evidence ID。
- **自适应流程**：根据证据变化决定继续扩展、深入、验证或停止。
- **来源质量检查**：区分一手来源、背景材料、弱证据、反证和过时事实。
- **轻量 CLI**：研究台账脚本只使用 Python 标准库。
- **适合市场分发**：包含 `SKILL.md`、Agent 元数据、参考文档、测试和提交材料。

## 安装

使用 `skills.sh` 安装：

```bash
npx skills add B143KC47/deep-research-skill
```

使用 Codex skill installer 安装：

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

直接克隆：

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
```

## 快速开始

创建研究任务：

```bash
python scripts/research_ledger.py init \
  --question "Which open-source vector database should we evaluate?" \
  --out-dir research_runs \
  --effort deep \
  --deliverable "evidence-backed recommendation"
```

记录一次有意义的检索或检查：

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

把证据绑定到具体主张：

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

写最终报告前检查状态：

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## 研究流程

| 阶段 | Agent 做什么 | 产出 |
|---|---|---|
| 界定 | 复述问题、决策目标、范围和时效要求。 | 研究计划 |
| 拆解 | 把主题拆成方面、来源类型和未知问题。 | Aspect map |
| 播种 | 先跑多条不同检索路线，再决定深入方向。 | 初始来源图 |
| 提取 | 记录主张、定位信息、日期、版本和来源质量。 | 证据台账 |
| 验证 | 寻找反证、过时事实和独立支持。 | 置信标签 |
| 综合 | 用 evidence ID 回答，并明确不确定性。 | 带引用报告 |

## 研究强度

| 强度 | 适用场景 | 目标 |
|---|---|---|
| `quick` | 低风险方向判断或快速核验 | 2-4 次有意义的 hop |
| `standard` | 普通研究型回答 | 5-8 次 hop，3+ 来源类型 |
| `deep` | 文献综述、项目尽调、广泛综合 | 9-14 次 hop，4+ 来源类型 |
| `exhaustive` | 高风险、有争议或用户指定预算的研究 | 15+ 次 hop，5+ 来源类型 |

Hop 数量是规划目标，不是硬性配额。当关键主张已有支持、剩余缺口也被明确标注时，就可以停止。

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── docs/
│   └── README.zh-CN.md
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

## 开发

研究台账脚本只使用 Python 标准库。

运行测试：

```bash
python -m unittest discover -s tests
```

运行语法检查：

```bash
python -m py_compile scripts/research_ledger.py
```

Windows 上如果 `python` 打开 Microsoft Store 或没有输出，请用 `py -m`：

```powershell
py -m unittest discover -s tests
py -m py_compile scripts\research_ledger.py
```

## 市场提交

常用链接：

- GitHub 仓库：<https://github.com/B143KC47/deep-research-skill>
- Raw skill 文件：<https://raw.githubusercontent.com/B143KC47/deep-research-skill/main/SKILL.md>
- ClawHub slug：`b143kc47-deep-research`

## 许可证

MIT。见 [LICENSE](../LICENSE)。
