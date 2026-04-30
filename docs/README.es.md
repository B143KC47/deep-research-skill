# Deep Research

[![CI](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/B143KC47/deep-research-skill/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/B143KC47/deep-research-skill?style=social)](https://github.com/B143KC47/deep-research-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)

**Idioma:** [English](../README.md) | [简体中文](README.zh-CN.md) | Español | [日本語](README.ja.md) | [한국어](README.ko.md)

Investigación profunda adaptable y auditable para agentes de IA. Esta skill ayuda a pasar de la exploración amplia a una síntesis citada, manteniendo trazables las fuentes, afirmaciones, contraevidencia e incertidumbre.

> Diseñada para informes de investigación, revisiones bibliográficas, evaluación de repositorios GitHub, verificación de fuentes, investigación técnica actual y decisiones que requieren más que una búsqueda rápida.

## Por Qué Usarla

- **Registro de evidencia**: rastrea pasos de investigación, fuentes, afirmaciones e IDs de evidencia.
- **Protocolo adaptable**: decide si ampliar, profundizar, verificar o detenerse según lo que cambie la evidencia.
- **Control de calidad de fuentes**: separa fuentes primarias, contexto, afirmaciones débiles, contraevidencia y hechos obsoletos.
- **CLI portable**: la herramienta de registro usa solo la biblioteca estándar de Python.
- **Lista para marketplaces**: incluye `SKILL.md`, metadatos de agente, referencias y pruebas.

## Instalación

Con `skills.sh`:

```bash
npx skills add B143KC47/deep-research-skill
```

Con Codex skill installer:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo B143KC47/deep-research-skill \
  --path .
```

Clonar directamente:

```bash
git clone https://github.com/B143KC47/deep-research-skill.git
```

## Inicio Rápido

Crear una ejecución de investigación:

```bash
python scripts/research_ledger.py init \
  --question "Which open-source vector database should we evaluate?" \
  --out-dir research_runs \
  --effort deep \
  --deliverable "evidence-backed recommendation"
```

Registrar un paso de investigación:

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

Agregar evidencia:

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

Comprobar el estado antes del informe final:

```bash
python scripts/research_ledger.py status --run-dir research_runs/<run-dir>
python scripts/research_ledger.py lint --run-dir research_runs/<run-dir>
```

## Flujo de Investigación

| Fase | Qué hace el agente | Resultado |
|---|---|---|
| Enmarcar | Replantea la pregunta, decisión, alcance y necesidad de actualidad. | Plan de investigación |
| Mapear | Divide el tema en aspectos, clases de fuentes e incógnitas. | Mapa de aspectos |
| Sembrar | Explora rutas distintas antes de profundizar. | Grafo inicial de fuentes |
| Extraer | Captura afirmaciones, localizadores, fechas, versiones y calidad. | Registro de evidencia |
| Verificar | Busca contradicciones, hechos obsoletos y apoyo independiente. | Etiquetas de confianza |
| Sintetizar | Responde con IDs de evidencia e incertidumbre explícita. | Informe citado |

## Niveles de Esfuerzo

| Esfuerzo | Uso típico | Objetivo |
|---|---|---|
| `quick` | Orientación de bajo riesgo | 2-4 pasos significativos |
| `standard` | Respuesta investigada normal | 5-8 pasos, 3+ tipos de fuente |
| `deep` | Revisión, due diligence o síntesis amplia | 9-14 pasos, 4+ tipos de fuente |
| `exhaustive` | Temas críticos, debatidos o con presupuesto definido | 15+ pasos, 5+ tipos de fuente |

## Desarrollo

```bash
python -m unittest discover -s tests
python -m py_compile scripts/research_ledger.py
```

En Windows, si `python` abre Microsoft Store o no muestra salida:

```powershell
py -m unittest discover -s tests
py -m py_compile scripts\research_ledger.py
```

## Marketplace

- Repositorio GitHub: <https://github.com/B143KC47/deep-research-skill>
- Archivo raw de la skill: <https://raw.githubusercontent.com/B143KC47/deep-research-skill/main/SKILL.md>
- Slug de ClawHub: `b143kc47-deep-research`

## Licencia

MIT. Consulta [LICENSE](../LICENSE).
