import tempfile
import unittest
from pathlib import Path

from scripts.gobuster_scan import EXCLUDE_LENGTHS, run_gobuster


class GobusterValidationTests(unittest.TestCase):
    def test_accepts_single_exclude_length(self):
        self.assertIsNotNone(EXCLUDE_LENGTHS.fullmatch("9984"))

    def test_accepts_multiple_lengths_and_ranges(self):
        self.assertIsNotNone(EXCLUDE_LENGTHS.fullmatch("9984,1000-1010"))

    def test_rejects_non_numeric_exclude_length(self):
        self.assertIsNone(EXCLUDE_LENGTHS.fullmatch("all"))

    def test_limits_concurrency(self):
        with tempfile.TemporaryDirectory() as directory:
            wordlist = Path(directory) / "words.txt"
            wordlist.write_text("admin\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "between 1 and 10"):
                run_gobuster(
                    "http://127.0.0.1:3000", str(wordlist), threads=11
                )

    def test_rejects_invalid_exclude_length(self):
        with tempfile.TemporaryDirectory() as directory:
            wordlist = Path(directory) / "words.txt"
            wordlist.write_text("admin\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Exclude length"):
                run_gobuster(
                    "http://127.0.0.1:3000", str(wordlist), exclude_length="invalid"
                )


if __name__ == "__main__":
    unittest.main()
