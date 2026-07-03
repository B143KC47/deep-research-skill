# Design Bibliography and Influences

This file is for explaining or adapting the skill design. It is not required for every research run. Do not treat these references as fixed facts about the current state of any project; re-check current docs, repos, releases, and papers during an actual research run.

## Skill architecture and trigger design

- **OpenAI Codex Skills documentation**. Pattern borrowed: a skill is a folder with `SKILL.md`, scripts, and supporting files; the skill description should make activation intent clear.
  - https://developers.openai.com/codex/skills

- **Anthropic Agent Skills / Claude Skills documentation**. Pattern borrowed: progressive disclosure through `SKILL.md`, references, and scripts; metadata and description guide skill discovery and use.
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Academic and research-agent patterns

- **ReAct: Synergizing Reasoning and Acting in Language Models**. Pattern borrowed: alternate reasoning, retrieval/action, and observation so the agent updates the plan as evidence arrives.
  - https://react-lm.github.io/
  - https://arxiv.org/abs/2210.03629

- **Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions (IRCoT)**. Pattern borrowed: one-shot retrieval is insufficient for multi-step questions; retrieval should depend on what has already been derived.
  - https://arxiv.org/abs/2212.10509
  - https://github.com/stonybrooknlp/ircot

- **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection**. Pattern borrowed: retrieve adaptively and critique whether retrieved evidence supports the generation.
  - https://arxiv.org/abs/2310.11511

- **FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation**. Pattern borrowed: fast-changing knowledge and false-premise questions require fresh search evidence and concise factual answers.
  - https://aclanthology.org/2024.findings-acl.813/
  - https://github.com/freshllms/freshqa

- **STORM: Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models**. Pattern borrowed: focus on the pre-writing research stage, question asking, breadth, outline construction, and grounded long-form synthesis.
  - https://storm-project.stanford.edu/research/storm/

- **Microsoft GraphRAG**. Pattern borrowed: preserve source relationships and graph structure when simple flat retrieval misses cross-document connections.
  - https://www.microsoft.com/en-us/research/project/graphrag/
  - https://github.com/microsoft/graphrag

## Open-source deep research projects and skills

- **GPT Researcher**. Pattern borrowed: planner/executor/publisher style separation, autonomous source gathering, and cited reports.
  - https://gptr.dev/
  - https://github.com/assafelovic/gpt-researcher

- **LangChain open_deep_research**. Pattern borrowed: configurable research agent that can work across model providers, search tools, and MCP servers.
  - https://github.com/langchain-ai/open_deep_research

- **nickscamara/open-deep-research**. Pattern borrowed: web-scale extraction plus reasoning model for open deep research.
  - https://github.com/nickscamara/open-deep-research

- **AgentSkills marketplace deep-research examples**. Pattern borrowed: trigger only for multi-source research, not simple lookups; require synthesis, verification, and citation tracking.
  - https://agentskills.so/

- **Skill Researcher / Docs Researcher examples**. Pattern borrowed: systematic technical research across official docs, GitHub, MCP directories, and project-specific knowledge bases.
  - https://mcpmarket.com/

## OpenClaw skill format

- **OpenClaw Skills documentation**. Pattern borrowed: AgentSkills-compatible folder layout with `SKILL.md`, local/workspace skill locations, and security cautions for third-party skills.
  - https://docs.openclaw.ai/tools/skills
  - https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md
