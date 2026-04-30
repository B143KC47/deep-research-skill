import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "research_ledger.py"


def run_cli(*args, check=True):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed with {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


class ResearchLedgerTests(unittest.TestCase):
    def test_init_creates_expected_run_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(
                "init",
                "--question",
                "How should we evaluate this repository?",
                "--out-dir",
                tmp,
                "--effort",
                "quick",
                "--deliverable",
                "short memo",
            )

            run_dir = Path(result.stdout.strip())
            self.assertTrue(run_dir.exists())
            self.assertEqual(run_dir.parent, Path(tmp).resolve())

            metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["effort"], "quick")
            self.assertEqual(metadata["hop_target"], 4)
            self.assertEqual(metadata["deliverable"], "short memo")

            for name in [
                "hop_ledger.csv",
                "evidence_ledger.csv",
                "source_graph.json",
                "plan.md",
                "open_questions.md",
                "final_report.md",
            ]:
                self.assertTrue((run_dir / name).exists(), name)

    def test_add_hop_and_evidence_then_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(
                run_cli(
                    "init",
                    "--question",
                    "What evidence supports the claim?",
                    "--out-dir",
                    tmp,
                ).stdout.strip()
            )

            run_cli(
                "add-hop",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--mode",
                "seed",
                "--tool-or-source",
                "local-file",
                "--query-or-action",
                "inspect README",
                "--result-summary",
                "Found primary project context",
            )
            run_cli(
                "add-evidence",
                "--run-dir",
                str(run_dir),
                "--hop",
                "1",
                "--source-id",
                "S001",
                "--title",
                "Local README",
                "--url-or-path",
                str(ROOT / "README.md"),
                "--source-type",
                "local-file",
                "--quality-score",
                "4",
                "--stance",
                "supports",
                "--claim",
                "The project documents its usage.",
            )

            with (run_dir / "hop_ledger.csv").open(encoding="utf-8", newline="") as handle:
                hops = list(csv.DictReader(handle))
            self.assertEqual(hops[0]["mode"], "seed")

            status = json.loads(run_cli("status", "--run-dir", str(run_dir)).stdout)
            self.assertEqual(status["hop_count"], 1)
            self.assertEqual(status["evidence_count"], 1)
            self.assertIn("local-file", status["source_domains"])

    def test_duplicate_evidence_id_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(
                run_cli(
                    "init",
                    "--question",
                    "Can duplicate evidence be rejected?",
                    "--out-dir",
                    tmp,
                ).stdout.strip()
            )

            args = [
                "add-evidence",
                "--run-dir",
                str(run_dir),
                "--evidence-id",
                "E0001",
                "--hop",
                "1",
                "--source-id",
                "S001",
                "--title",
                "Source",
                "--url-or-path",
                "https://example.com",
                "--source-type",
                "official-doc",
                "--quality-score",
                "5",
                "--stance",
                "supports",
                "--claim",
                "A claim",
            ]
            run_cli(*args)
            duplicate = run_cli(*args, check=False)

            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn("evidence_id already exists", duplicate.stderr)


if __name__ == "__main__":
    unittest.main()
