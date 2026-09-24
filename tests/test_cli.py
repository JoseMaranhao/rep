from pathlib import Path
import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_help_does_not_require_optional_runtime_packages(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "apartment_condition_report.cli", "--help"],
            cwd=Path(__file__).parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--analyze", result.stdout)
        self.assertIn("--drive-folder-id", result.stdout)
