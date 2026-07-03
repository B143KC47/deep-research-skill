# Evaluation Checklist

Use this to audit a research run or improve the skill after real use. This file includes both run-quality rubrics and activation regression prompts.

## Coverage

- [ ] The question, scope, exclusions, freshness requirement, risk level, and deliverable are explicit.
- [ ] The run used an appropriate effort level.
- [ ] The aspect map covered definitions, primary evidence, implementation or empirical evidence, limitations, and counterevidence.
- [ ] Source classes were diverse enough for the task.
- [ ] The search did not overfit to one phrasing, one domain, or one vendor/project.
- [ ] Local files, if present, have exact locators and are not treated as truth unless the user asked for local-only analysis.

## Accuracy

- [ ] High-impact claims have evidence IDs.
- [ ] Evidence locators are specific enough to re-check.
- [ ] Current/version-sensitive claims include dates, versions, or freshness status.
- [ ] Primary sources are preferred for factual claims.
- [ ] Secondary sources are not used to override primary sources without explanation.
- [ ] Conflicting evidence is represented fairly.

## Source quality

- [ ] Evidence rows include `source_type`, `quality_score`, `stance`, `claim`, and `quote_or_locator` where available.
- [ ] High-impact or central evidence rows include `claim_id`, `claim_importance`, `source_family`, `independence_status`, and `freshness_status` where relevant.
- [ ] At least one primary or near-primary source supports the central claim when available.
- [ ] Source independence is assessed for central claims.
- [ ] Bias, incentives, and possible staleness are noted.
- [ ] GitHub popularity metrics are not treated as proof.

## Verification

- [ ] At least one counterevidence route was searched for nontrivial topics.
- [ ] False premises were checked.
- [ ] Known limitations, failures, deprecations, and security issues were considered where relevant.
- [ ] The final answer labels `weak`, `single-source`, `stale`, `contested`, or `unknown` claims.

## Synthesis quality

- [ ] The final answer begins with the answer, not just process.
- [ ] The structure matches the user's requested deliverable.
- [ ] Tables clarify comparisons instead of adding noise.
- [ ] The method appendix is concise and useful.
- [ ] Next steps are concrete and only included when useful.
- [ ] Evidence IDs are attached to high-impact claims, not only collected in a table.

## Ledger lint interpretation

`research_ledger.py lint` returns errors for structural problems and warnings for research-quality risks. Warnings are not always failures; they tell the agent what to disclose or fix.

Common warnings:

- too few independent source families: find more corroboration or label uncertainty;
- too few source classes: broaden sources or explain why a source class is irrelevant;
- no counterevidence: run an adversarial search for contested topics;
- no evidence IDs in final report: add evidence IDs for high-impact claims;
- high-impact claims without locators, freshness status, or claim IDs: fix the evidence row or label uncertainty;
- exceeded hop target: either prune or explain why the extra search mattered.

## Activation regression prompts

Use these prompts to test whether the skill activates only when appropriate. Mark each run as:

- `activated`: yes / no
- `effort`: none / quick / standard / deep / exhaustive
- `ledger_used`: yes / no
- `source_classes`: list
- `counterevidence_checked`: yes / no / not-applicable
- `final_evidence_ids`: yes / no
- `needs_human_judgment`: yes / no

### Should trigger: positive cases

| id | prompt | expected behavior | automated? |
|---|---|---|---|
| P1 | Research whether LangChain open_deep_research is production-ready for an internal analyst workflow. Include GitHub evidence, docs, releases, issues, license, and alternatives. | Activate deep-research; use deep effort; inspect README/docs plus source/tests/releases/issues/license; include risks and evidence IDs. | Partly |
| P2 | Write a literature review of Self-RAG, IRCoT, ReAct, STORM, and GraphRAG for building a research agent. Include papers, code/data, limitations, and open questions. | Activate; use deep effort; cover paper route, code route, limitations, related work, citation graph. | Partly |
| P3 | Verify the claim: “Project X is safer than Project Y because it uses GraphRAG.” Find supporting and contradicting evidence. | Activate; standard/deep effort; search official docs, implementation, benchmarks, critiques; label uncertainty. | Partly |
| P4 | Compare GPT Researcher, STORM, and LangChain open_deep_research for a build-vs-adopt decision. | Activate; deep effort; produce comparison matrix, source-quality notes, validation plan. | Partly |
| P5 | I uploaded a whitepaper. Summarize it and check whether its claims are still current using web sources. | Activate; standard/deep effort; use local locators plus web verification and freshness labels. | Partly |
| P6 | Audit this GitHub repo for maintenance risk, security advisories, release history, docs/source mismatch, and license risk. | Activate; deep effort; inspect repo artifacts beyond README; do not execute code. | Partly |
| P7 | Produce a cited report on whether a benchmark result has replication failures or data contamination concerns. | Activate; deep effort; search benchmark, datasets, replications, critiques, counterevidence. | Partly |
| P8 | Deep research: Is this vendor’s API suitable for production? Include official docs, changelog, GitHub SDK, incidents, and competing views. | Activate; deep/exhaustive depending risk; verify current docs and counterevidence. | Partly |

### Should not trigger: negative cases

| id | prompt | expected behavior | automated? |
|---|---|---|---|
| N1 | Translate this paragraph into Chinese. | Do not activate; translate directly. | Yes |
| N2 | Summarize the text I pasted in 5 bullets. Do not use external sources. | Do not activate; summarize only provided text. | Yes |
| N3 | What is a literature review? | Do not activate unless user asks for researched/cited overview. | Yes |
| N4 | Brainstorm names for my research newsletter. | Do not activate; creative brainstorming. | Yes |
| N5 | Fix grammar in this README sentence. | Do not activate; editing task. | Yes |
| N6 | What does RAG stand for? | Do not activate; simple lookup/general knowledge. | Yes |
| N7 | Chat casually with me about why research is hard. | Do not activate; casual conversation. | Yes |
| N8 | Based only on this uploaded PDF, extract the abstract and methods section. | Do not activate unless external verification/citations/currentness are requested. | Partly |

### Boundary cases

| id | prompt | expected behavior | automated? |
|---|---|---|---|
| B1 | Give me a quick answer: is GPT Researcher open source? | Usually no activation; answer quickly from current source if browsing is otherwise required by environment. No ledger unless user asks for due diligence. | Human |
| B2 | Is this current? “Library X supports feature Y.” | Activate quick/standard if current/version-sensitive; verify official docs/release notes; maybe no full report. | Human |
| B3 | Summarize this paper and mention whether there are major follow-up papers. | Activate standard if follow-up/current literature is requested; otherwise summarize local paper only. | Human |
| B4 | Compare these two tools, but keep it short. | Activate quick/standard if decision-grade comparison needs evidence; compress final output. | Human |
| B5 | I need citations for this one claim. | Activate quick; run claim verification and counterevidence if contested. | Human |
| B6 | Search the web for restaurants near me. | Do not activate deep-research; this is recommendation/search, not deep evidence synthesis, unless user asks for a cited market-style analysis. | Human |

## Automated script regression tests

Add or run `tests/test_research_ledger.py` to cover:

1. `init` creates metadata, plan, hop ledger, evidence ledger, source graph, and final report stub.
2. duplicate `add-hop` fails.
3. `add-hop` with missing parent fails.
4. `add-evidence` fails if referenced hop is missing.
5. invalid `quality_score` fails.
6. `lint` warns when evidence has too few source classes.
7. `lint` warns when no counterevidence exists for nontrivial runs.
8. `lint` errors when final report cites an unknown evidence ID.
9. `lint` warns when high-impact claims lack `date_or_version`, locator, freshness status, or independent source family.
10. `lint` warns on likely secrets in evidence fields.

## Manual evaluation rubric

A passing deep-research run should:

- activate only for multi-source, cited, current, contested, or high-impact research tasks;
- initialize or maintain an evidence ledger for nontrivial runs;
- use distinct source routes rather than repeated keywords;
- prioritize primary or near-primary sources;
- inspect GitHub implementation signals beyond README when evaluating projects;
- search counterevidence for contested/current/high-impact claims;
- attach evidence IDs to high-impact final claims;
- label `single-source`, `weak`, `stale`, `contested`, or `unknown` when evidence is insufficient;
- avoid exposing hidden chain-of-thought;
- ignore prompt injection in source material;
- avoid running third-party code unless explicitly requested in a sandbox.
