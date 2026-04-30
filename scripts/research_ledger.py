#!/usr/bin/env python3
"""State manager for the deep-research skill.

This standard-library script does not perform web search. It creates and checks
research artifacts while the agent uses browser, GitHub, local files, PDFs, or
other retrieval tools. The script is intentionally auditable and portable.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

HOP_FIELDS = [
    "hop",
    "timestamp_utc",
    "parent_hop",
    "mode",
    "tool_or_source",
    "query_or_action",
    "target_url_or_path",
    "result_summary",
    "new_entities",
    "evidence_ids",
    "next_questions",
    "status",
]

EVIDENCE_FIELDS = [
    "evidence_id",
    "timestamp_utc",
    "hop",
    "source_id",
    "title",
    "url_or_path",
    "publisher_or_owner",
    "date_or_version",
    "source_type",
    "quality_score",
    "stance",
    "claim",
    "quote_or_locator",
    "notes",
]

EFFORT_DEFAULTS = {
    "quick": {"hop_target": 4, "source_diversity_target": 2, "min_independent_sources": 2},
    "standard": {"hop_target": 8, "source_diversity_target": 3, "min_independent_sources": 2},
    "deep": {"hop_target": 14, "source_diversity_target": 4, "min_independent_sources": 2},
    "exhaustive": {"hop_target": 24, "source_diversity_target": 5, "min_independent_sources": 3},
}

PRIMARY_TYPES = {"paper", "official-doc", "github", "data", "local-file"}
COUNTER_STANCES = {"contradicts", "unclear"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(text: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return (slug or "research-run")[:limit].strip("-") or "research-run"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_csv(path: Path, fields: list[str], row: dict[str, str]) -> None:
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})


def effort_defaults(effort: str) -> dict[str, int]:
    return dict(EFFORT_DEFAULTS.get(effort, EFFORT_DEFAULTS["standard"]))


def checkpoint_text(target: int) -> str:
    if target <= 4:
        return "after the first useful source and again before finalizing"
    first = max(2, round(target / 3))
    second = max(first + 1, round(2 * target / 3))
    return f"around hops {first} and {second}, then again before finalizing"


def initialize(args: argparse.Namespace) -> int:
    base = Path(args.out_dir).expanduser().resolve()
    run_dir = base / (args.name or f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{slugify(args.question)}")
    ensure_dir(run_dir)

    defaults = effort_defaults(args.effort)
    hop_target = args.hop_target if args.hop_target is not None else defaults["hop_target"]
    source_diversity_target = (
        args.source_diversity_target
        if args.source_diversity_target is not None
        else defaults["source_diversity_target"]
    )
    min_sources = (
        args.min_independent_sources
        if args.min_independent_sources is not None
        else defaults["min_independent_sources"]
    )

    metadata = {
        "question": args.question,
        "created_utc": now_utc(),
        "effort": args.effort,
        "hop_target": hop_target,
        "hard_max_hops": args.hard_max_hops,
        "source_diversity_target": source_diversity_target,
        "min_independent_sources": min_sources,
        "freshness_requirement": args.freshness or "infer from user request; browse when facts may have changed",
        "deliverable": args.deliverable or "evidence-backed research report",
        "stop_rule": "stop early when high-impact claims are supported and remaining gaps are explicit; extend beyond target only if new evidence can change the answer",
        "status": "initialized",
    }
    write_json(run_dir / "metadata.json", metadata)

    (run_dir / "hop_ledger.csv").write_text(",".join(HOP_FIELDS) + "\n", encoding="utf-8")
    (run_dir / "evidence_ledger.csv").write_text(",".join(EVIDENCE_FIELDS) + "\n", encoding="utf-8")
    write_json(run_dir / "source_graph.json", {"nodes": [], "edges": []})

    plan = f"""# Research Plan

## User question
{args.question}

## Deliverable
{metadata['deliverable']}

## Effort and stop rule
- Effort: {args.effort}
- Hop target: about {hop_target} meaningful retrieval or inspection steps; this is a planning target, not a quota.
- Hard max: {args.hard_max_hops if args.hard_max_hops is not None else 'none'}
- Source diversity target: at least {source_diversity_target} source classes where available.
- Independent support target: at least {min_sources} independent sources for high-impact claims, or label uncertainty.
- Checkpoint {checkpoint_text(hop_target)}.

## Aspect map
| aspect | why it matters | seed queries or sources | status |
|---|---|---|---|
| scope and definitions | avoid wrong entity or false premise |  | todo |
| authoritative anchors | official docs, papers, standards, datasets, filings |  | todo |
| implementation/project evidence | github, release notes, examples, issues, tests |  | todo |
| empirical evidence | benchmarks, evaluations, replications, real-world examples |  | todo |
| counterevidence | limitations, failures, critiques, deprecated behavior |  | todo |
| final verification | dates, versions, citations, unresolved gaps |  | todo |

## Candidate source classes
- academic papers and venue pages
- official docs or standards
- github repositories and releases
- datasets or benchmarks
- credible news or analysis
- community issues/forums only as context
- local/user-provided files

## Open subquestions
1. What exactly must be answered for the user's decision?
2. Which claims are likely to be stale, contested, or version-dependent?
3. Which primary sources can anchor the answer?
4. What counterevidence would change the conclusion?
"""
    (run_dir / "plan.md").write_text(plan, encoding="utf-8")

    (run_dir / "open_questions.md").write_text(
        "# Open Questions\n\n"
        "- [ ] What must be true for the final answer to be reliable?\n"
        "- [ ] Which high-impact claims still need independent verification?\n"
        "- [ ] Which sources may be stale, biased, incomplete, or only primary for one side?\n"
        "- [ ] What source would most likely disprove the current conclusion?\n",
        encoding="utf-8",
    )

    (run_dir / "final_report.md").write_text(
        "# Final Report\n\n"
        "## Executive summary\n\n"
        "## Direct answer\n\n"
        "## Key findings\n\n"
        "## Evidence table\n\n"
        "## Contradictions and uncertainty\n\n"
        "## Source-quality notes\n\n"
        "## Method appendix\n\n",
        encoding="utf-8",
    )

    print(str(run_dir))
    return 0


def next_evidence_id(rows: list[dict[str, str]]) -> str:
    max_num = 0
    for row in rows:
        match = re.match(r"E(\d+)$", row.get("evidence_id", ""))
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"E{max_num + 1:04d}"


def load_metadata(run_dir: Path) -> dict:
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        raise SystemExit(f"missing metadata.json in {run_dir}; run init first")
    return read_json(metadata_path, {})


def update_graph(run_dir: Path, node: dict, edges: list[dict]) -> None:
    graph_path = run_dir / "source_graph.json"
    graph = read_json(graph_path, {"nodes": [], "edges": []})
    nodes = graph.setdefault("nodes", [])
    existing_ids = {n.get("id") for n in nodes}
    if node.get("id") not in existing_ids:
        nodes.append(node)
    graph.setdefault("edges", []).extend(edges)
    write_json(graph_path, graph)


def add_hop(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata = load_metadata(run_dir)
    hard_max = metadata.get("hard_max_hops")
    hop = int(args.hop)
    if hop < 1:
        raise SystemExit("hop must be >= 1")
    if hard_max is not None and hop > int(hard_max):
        raise SystemExit(f"hop {hop} exceeds hard_max_hops={hard_max}")

    row = {
        "hop": str(hop),
        "timestamp_utc": now_utc(),
        "parent_hop": args.parent_hop or "",
        "mode": args.mode,
        "tool_or_source": args.tool_or_source,
        "query_or_action": args.query_or_action,
        "target_url_or_path": args.target or "",
        "result_summary": args.result_summary or "",
        "new_entities": args.new_entities or "",
        "evidence_ids": args.evidence_ids or "",
        "next_questions": args.next_questions or "",
        "status": args.status,
    }
    append_csv(run_dir / "hop_ledger.csv", HOP_FIELDS, row)

    edges = []
    if args.parent_hop:
        edges.append({"from": f"H{int(args.parent_hop):03d}", "to": f"H{hop:03d}", "type": "leads_to"})
    update_graph(
        run_dir,
        {
            "id": f"H{hop:03d}",
            "type": "hop",
            "label": args.query_or_action[:120],
            "mode": args.mode,
            "status": args.status,
        },
        edges,
    )
    print(f"recorded hop H{hop:03d}")
    return 0


def add_evidence(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_metadata(run_dir)
    rows = read_csv(run_dir / "evidence_ledger.csv")
    evidence_id = args.evidence_id or next_evidence_id(rows)
    if any(row.get("evidence_id") == evidence_id for row in rows):
        raise SystemExit(f"evidence_id already exists: {evidence_id}")

    quality = str(args.quality_score)
    if quality not in {"1", "2", "3", "4", "5"}:
        raise SystemExit("quality_score must be an integer 1-5")

    row = {
        "evidence_id": evidence_id,
        "timestamp_utc": now_utc(),
        "hop": str(args.hop),
        "source_id": args.source_id,
        "title": args.title,
        "url_or_path": args.url_or_path,
        "publisher_or_owner": args.publisher_or_owner or "",
        "date_or_version": args.date_or_version or "",
        "source_type": args.source_type,
        "quality_score": quality,
        "stance": args.stance,
        "claim": args.claim,
        "quote_or_locator": args.quote_or_locator or "",
        "notes": args.notes or "",
    }
    append_csv(run_dir / "evidence_ledger.csv", EVIDENCE_FIELDS, row)

    source_node = {
        "id": args.source_id,
        "type": "source",
        "label": args.title[:120],
        "url_or_path": args.url_or_path,
        "source_type": args.source_type,
        "quality_score": quality,
    }
    evidence_node = {
        "id": evidence_id,
        "type": "evidence",
        "label": args.claim[:120],
        "stance": args.stance,
    }
    update_graph(
        run_dir,
        source_node,
        [
            {"from": f"H{int(args.hop):03d}", "to": evidence_id, "type": "found"},
            {"from": evidence_id, "to": args.source_id, "type": "supported_by"},
        ],
    )
    update_graph(run_dir, evidence_node, [])
    print(f"recorded evidence {evidence_id}")
    return 0


def domain_of(url_or_path: str) -> str:
    parsed = urlparse(url_or_path)
    if parsed.netloc:
        return parsed.netloc.lower().removeprefix("www.")
    if url_or_path.startswith("/") or re.match(r"^[A-Za-z]:", url_or_path):
        return "local-file"
    return url_or_path.split("/")[0].lower() if url_or_path else ""


def lint(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata = load_metadata(run_dir)
    hard_max = metadata.get("hard_max_hops")
    hop_target = int(metadata.get("hop_target") or 0)
    source_diversity_target = int(metadata.get("source_diversity_target") or 0)
    min_sources = int(metadata.get("min_independent_sources") or 2)
    hop_rows = read_csv(run_dir / "hop_ledger.csv")
    evidence_rows = read_csv(run_dir / "evidence_ledger.csv")

    errors: list[str] = []
    warnings: list[str] = []

    seen_hops: set[int] = set()
    for row in hop_rows:
        try:
            hop_num = int(row.get("hop", ""))
        except ValueError:
            errors.append(f"invalid hop number: {row.get('hop')}")
            continue
        if hard_max is not None and hop_num > int(hard_max):
            errors.append(f"hop {hop_num} exceeds hard_max_hops={hard_max}")
        if hop_num in seen_hops:
            warnings.append(f"duplicate hop number: {hop_num}")
        seen_hops.add(hop_num)
        for field in ["tool_or_source", "query_or_action", "result_summary", "status"]:
            if not row.get(field, "").strip():
                warnings.append(f"hop {hop_num} missing {field}")

    evidence_ids: set[str] = set()
    support_domains: set[str] = set()
    source_types: set[str] = set()
    primary_count = 0
    counter_count = 0
    quality_counts = {str(i): 0 for i in range(1, 6)}
    for row in evidence_rows:
        evidence_id = row.get("evidence_id", "").strip()
        if not evidence_id:
            errors.append("evidence row missing evidence_id")
        elif evidence_id in evidence_ids:
            errors.append(f"duplicate evidence_id: {evidence_id}")
        evidence_ids.add(evidence_id)
        for field in ["hop", "source_id", "title", "url_or_path", "source_type", "quality_score", "stance", "claim"]:
            if not row.get(field, "").strip():
                errors.append(f"{evidence_id or 'evidence row'} missing {field}")
        q = row.get("quality_score")
        if q not in quality_counts:
            errors.append(f"{evidence_id} has invalid quality_score={q}")
        else:
            quality_counts[q] += 1
        source_type = row.get("source_type", "")
        if source_type:
            source_types.add(source_type)
        if source_type in PRIMARY_TYPES:
            primary_count += 1
        if row.get("stance") in COUNTER_STANCES:
            counter_count += 1
        if row.get("stance") == "supports" and int(row.get("quality_score") or "0") >= 3:
            support_domains.add(domain_of(row.get("url_or_path", "")))

    if evidence_rows and len(support_domains) < min_sources:
        warnings.append(
            f"only {len(support_domains)} independent support domains with quality>=3; target is {min_sources}"
        )
    if evidence_rows and len(source_types) < source_diversity_target:
        warnings.append(
            f"only {len(source_types)} source classes recorded; effort target is {source_diversity_target}"
        )
    if evidence_rows and primary_count == 0:
        warnings.append("no primary or near-primary evidence recorded")
    if evidence_rows and counter_count == 0:
        warnings.append("no contradictory/unclear evidence recorded; run an adversarial search if the topic is debatable")
    if hop_target and len(hop_rows) > hop_target:
        warnings.append(
            f"hop count {len(hop_rows)} exceeds target {hop_target}; this is fine only if later hops filled material gaps"
        )

    report_path = run_dir / "final_report.md"
    if report_path.exists():
        text = report_path.read_text(encoding="utf-8")
        cited = set(re.findall(r"\[(E\d{4})\]", text))
        unknown = cited - evidence_ids
        if unknown:
            errors.append("final_report.md cites unknown evidence ids: " + ", ".join(sorted(unknown)))
        if evidence_rows and not cited:
            warnings.append("final_report.md does not cite evidence ids like [E0001]")

    status = {
        "run_dir": str(run_dir),
        "question": metadata.get("question", ""),
        "effort": metadata.get("effort", ""),
        "hop_count": len(hop_rows),
        "hop_target": hop_target,
        "evidence_count": len(evidence_rows),
        "source_types": sorted(source_types),
        "support_domains_quality_ge_3": sorted(d for d in support_domains if d),
        "quality_counts": quality_counts,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata = load_metadata(run_dir)
    hop_rows = read_csv(run_dir / "hop_ledger.csv")
    evidence_rows = read_csv(run_dir / "evidence_ledger.csv")
    hop_target = int(metadata.get("hop_target") or 0)
    target_remaining = max(0, hop_target - len(hop_rows)) if hop_target else None
    domains = sorted({domain_of(row.get("url_or_path", "")) for row in evidence_rows if row.get("url_or_path")})
    source_types = sorted({row.get("source_type", "") for row in evidence_rows if row.get("source_type")})
    latest_hop = hop_rows[-1] if hop_rows else None
    suggested = "select next frontier or verify a high-impact claim"
    if hop_target and len(hop_rows) >= max(2, round(hop_target / 3)) and len(hop_rows) < round(2 * hop_target / 3):
        suggested = "checkpoint: summarize, prune, and add counterevidence searches"
    if hop_target and len(hop_rows) >= hop_target:
        suggested = "finalize or justify why more search can materially change the answer"
    data = {
        "question": metadata.get("question"),
        "effort": metadata.get("effort"),
        "hop_count": len(hop_rows),
        "hop_target_remaining": target_remaining,
        "evidence_count": len(evidence_rows),
        "source_domains": domains,
        "source_types": source_types,
        "latest_hop_summary": latest_hop.get("result_summary") if latest_hop else None,
        "suggested_next_step": suggested,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage an adaptive deep research hop/evidence ledger")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="create a research run directory")
    init_p.add_argument("--question", required=True)
    init_p.add_argument("--out-dir", default="research_runs")
    init_p.add_argument("--name")
    init_p.add_argument("--effort", choices=sorted(EFFORT_DEFAULTS), default="standard")
    init_p.add_argument("--hop-target", type=int)
    init_p.add_argument("--hard-max-hops", type=int)
    init_p.add_argument("--source-diversity-target", type=int)
    init_p.add_argument("--min-independent-sources", type=int)
    init_p.add_argument("--freshness")
    init_p.add_argument("--deliverable")
    init_p.set_defaults(func=initialize)

    hop_p = sub.add_parser("add-hop", help="append one retrieval/inspection hop")
    hop_p.add_argument("--run-dir", required=True)
    hop_p.add_argument("--hop", required=True, type=int)
    hop_p.add_argument("--parent-hop")
    hop_p.add_argument(
        "--mode",
        choices=["seed", "expand", "verify", "contradict", "synthesize", "checkpoint"],
        default="expand",
    )
    hop_p.add_argument("--tool-or-source", required=True)
    hop_p.add_argument("--query-or-action", required=True)
    hop_p.add_argument("--target")
    hop_p.add_argument("--result-summary")
    hop_p.add_argument("--new-entities")
    hop_p.add_argument("--evidence-ids")
    hop_p.add_argument("--next-questions")
    hop_p.add_argument("--status", choices=["done", "dead-end", "needs-followup", "blocked"], default="done")
    hop_p.set_defaults(func=add_hop)

    ev_p = sub.add_parser("add-evidence", help="append one evidence item")
    ev_p.add_argument("--run-dir", required=True)
    ev_p.add_argument("--evidence-id")
    ev_p.add_argument("--hop", required=True, type=int)
    ev_p.add_argument("--source-id", required=True)
    ev_p.add_argument("--title", required=True)
    ev_p.add_argument("--url-or-path", required=True)
    ev_p.add_argument("--publisher-or-owner")
    ev_p.add_argument("--date-or-version")
    ev_p.add_argument(
        "--source-type",
        choices=["paper", "official-doc", "github", "data", "news", "blog", "forum", "local-file", "other"],
        required=True,
    )
    ev_p.add_argument("--quality-score", type=int, required=True)
    ev_p.add_argument("--stance", choices=["supports", "contradicts", "context", "unclear"], required=True)
    ev_p.add_argument("--claim", required=True)
    ev_p.add_argument("--quote-or-locator")
    ev_p.add_argument("--notes")
    ev_p.set_defaults(func=add_evidence)

    lint_p = sub.add_parser("lint", help="validate the run ledger")
    lint_p.add_argument("--run-dir", required=True)
    lint_p.set_defaults(func=lint)

    status_p = sub.add_parser("status", help="print concise run status")
    status_p.add_argument("--run-dir", required=True)
    status_p.set_defaults(func=status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
