import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "research_ledger.py"


class ResearchLedgerCliTests(unittest.TestCase):
    def run_cli(self, *args, expect_success=True):
        cmd = [sys.executable, "-S", str(SCRIPT), *args]
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if expect_success and proc.returncode != 0:
            self.fail(f"command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        if not expect_success and proc.returncode == 0:
            self.fail(f"command unexpectedly succeeded: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        return proc

    def init_run(self, tmpdir, effort="standard"):
        proc = self.run_cli(
            "init",
            "--question",
            "Verify whether Project X is production-ready",
            "--out-dir",
            tmpdir,
            "--name",
            "run",
            "--force",
            "--effort",
            effort,
        )
        return Path(proc.stdout.strip().splitlines()[-1])

    def test_init_creates_expected_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            for name in [
                "metadata.json",
                "plan.md",
                "hop_ledger.csv",
                "evidence_ledger.csv",
                "source_graph.json",
                "open_questions.md",
                "final_report.md",
            ]:
                self.assertTrue((run_dir / name).exists(), name)
            with (run_dir / "evidence_ledger.csv").open(newline="", encoding="utf-8") as f:
                fields = next(csv.reader(f))
            self.assertIn("claim_id", fields)
            self.assertIn("freshness_status", fields)
            self.assertIn("independence_status", fields)

    def test_duplicate_hop_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            self.run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--mode",
                "seed",
                "--tool-or-source",
                "web",
                "--query-or-action",
                "search official docs",
                "--result-summary",
                "found docs",
            )
            self.run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--mode",
                "seed",
                "--tool-or-source",
                "web",
                "--query-or-action",
                "duplicate",
                "--result-summary",
                "duplicate",
                expect_success=False,
            )

    def test_add_hop_missing_parent_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            self.run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "2",
                "--parent-hop",
                "1",
                "--tool-or-source",
                "web",
                "--query-or-action",
                "search",
                "--result-summary",
                "x",
                expect_success=False,
            )

    def test_evidence_references_missing_hop_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            self.run_cli(
                "add-evidence",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--source-id",
                "S001",
                "--title",
                "Doc",
                "--url-or-path",
                "https://example.com/doc",
                "--source-type",
                "official-doc",
                "--quality-score",
                "5",
                "--stance",
                "supports",
                "--claim",
                "Project X has docs",
                expect_success=False,
            )

    def test_invalid_quality_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            self.run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--tool-or-source",
                "web",
                "--query-or-action",
                "search",
                "--result-summary",
                "found source",
            )
            self.run_cli(
                "add-evidence",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--source-id",
                "S001",
                "--title",
                "Doc",
                "--url-or-path",
                "https://example.com/doc",
                "--source-type",
                "official-doc",
                "--quality-score",
                "6",
                "--stance",
                "supports",
                "--claim",
                "Project X has docs",
                expect_success=False,
            )

    def test_lint_errors_on_unknown_final_report_evidence_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp)
            (run_dir / "final_report.md").write_text("# Report\n\nClaim [E9999]\n", encoding="utf-8")
            proc = self.run_cli("lint", "--run-dir", str(run_dir), expect_success=False)
            data = json.loads(proc.stdout)
            self.assertTrue(any("unknown evidence" in error for error in data["errors"]))

    def test_lint_warns_for_high_impact_missing_counterevidence_and_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = self.init_run(tmp, effort="deep")
            self.run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--mode",
                "seed",
                "--tool-or-source",
                "web",
                "--query-or-action",
                "search official docs",
                "--result-summary",
                "found official docs",
            )
            self.run_cli(
                "add-evidence",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--source-id",
                "S001",
                "--claim-id",
                "C001",
                "--claim-importance",
                "high",
                "--title",
                "Official docs",
                "--url-or-path",
                "https://example.com/docs",
                "--publisher-or-owner",
                "Example Project",
                "--source-family",
                "Example Project",
                "--source-type",
                "official-doc",
                "--quality-score",
                "5",
                "--stance",
                "supports",
                "--independence-status",
                "same-family",
                "--freshness-status",
                "current",
                "--claim",
                "Project X supports feature Y",
                "--quote-or-locator",
                "docs section; token=sk-abcdefghijklmnopqrstuvwxyz",
            )
            proc = self.run_cli("lint", "--run-dir", str(run_dir))
            data = json.loads(proc.stdout)
            warnings = "\n".join(data["warnings"])
            self.assertIn("counterevidence", warnings)
            self.assertIn("secret/token", warnings)


if __name__ == "__main__":
    unittest.main()
