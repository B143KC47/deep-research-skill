# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)

**언어:** [English](../README.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [日本語](README.ja.md) | 한국어

AI 에이전트를 위한 적응형, 감사 가능한 deep research skill입니다. 넓은 탐색에서 인용 가능한 종합 답변으로 이동하는 동안 출처, 주장, 반대 증거, 불확실성을 추적할 수 있습니다.

> 리서치 메모, 문헌 리뷰, GitHub 프로젝트 실사, 출처 검증, 최신 기술 조사, 단순 검색 이상의 의사결정에 적합합니다.

## 왜 사용하나요

- **Evidence ledger**: 조사 단계, 출처, 주장, evidence ID를 기록합니다.
- **적응형 프로토콜**: 증거가 바뀌는 정도에 따라 확장, 심화, 검증, 중단을 결정합니다.
- **출처 품질 확인**: 1차 출처, 맥락 자료, 약한 주장, 반대 증거, 오래된 사실을 구분합니다.
- **휴대 가능한 CLI**: ledger 도구는 Python 표준 라이브러리만 사용합니다.
- **Marketplace 준비**: `SKILL.md`, 에이전트 metadata, 참고 문서, 테스트를 포함합니다.

## 설치

`skills.sh` 사용:

```bash
npx skills add B143KC47/deep-research-skill
```

Codex skill installer 사용:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

직접 clone:

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
```

## 빠른 시작

리서치 run 생성:

```bash
python scripts/research_ledger.py init \
  --question "Which open-source vector database should we evaluate?" \
  --out-dir research_runs \
  --effort deep \
  --deliverable "evidence-backed recommendation"
```

의미 있는 조사 hop 기록:

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

증거 추가:

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

최종 보고서 작성 전 확인:

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## 리서치 흐름

| 단계 | 에이전트가 하는 일 | 결과 |
|---|---|---|
| Frame | 질문, 의사결정, 범위, 최신성 요구를 정리합니다. | 리서치 계획 |
| Map | 주제를 관점, 출처 유형, 미확인 질문으로 나눕니다. | Aspect map |
| Seed | 깊게 들어가기 전에 여러 탐색 경로를 시도합니다. | 초기 source graph |
| Extract | 주장, 위치, 날짜, 버전, 출처 품질을 기록합니다. | Evidence ledger |
| Verify | 모순, 오래된 사실, 독립적 근거를 찾습니다. | 신뢰도 라벨 |
| Synthesize | Evidence ID와 불확실성을 명시해 답합니다. | 인용 보고서 |

## Effort Levels

| 수준 | 사용 사례 | 목표 |
|---|---|---|
| `quick` | 낮은 위험의 방향 확인 | 2-4 meaningful hops |
| `standard` | 일반적인 조사 답변 | 5-8 hops, 3+ source classes |
| `deep` | 문헌 리뷰, 실사, 넓은 종합 | 9-14 hops, 4+ source classes |
| `exhaustive` | 중요하거나 논쟁적인 주제 | 15+ hops, 5+ source classes |

## 개발

```bash
python -m unittest discover -s tests
python -m py_compile scripts/research_ledger.py
```

Windows에서 `python`이 Microsoft Store를 열거나 출력이 없으면:

```powershell
py -m unittest discover -s tests
py -m py_compile scripts\research_ledger.py
```

## Marketplace

- GitHub repository: <https://github.com/B143KC47/deep-research-skill>
- Raw skill file: <https://raw.githubusercontent.com/B143KC47/deep-research-skill/main/SKILL.md>
- ClawHub slug: `b143kc47-deep-research`

## 라이선스

MIT. [LICENSE](../LICENSE)를 참고하세요.
