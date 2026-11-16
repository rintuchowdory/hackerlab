import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.helper import TargetError, load_wordlist, validate_lab_target, validate_lab_url


class HelperTests(unittest.TestCase):
    def test_allows_loopback_ip(self):
        self.assertEqual(validate_lab_target("127.0.0.1"), "127.0.0.1")

    def test_rejects_public_ip(self):
        with self.assertRaises(TargetError):
            validate_lab_target("8.8.8.8")

    def test_rejects_documentation_range(self):
        with self.assertRaises(TargetError):
            validate_lab_target("203.0.113.99")

    def test_rejects_url_when_host_expected(self):
        with self.assertRaises(TargetError):
            validate_lab_target("https://example.com")

    def test_validates_private_url(self):
        with patch("scripts.helper.socket.getaddrinfo") as resolver:
            resolver.return_value = [(None, None, None, None, ("192.168.56.10", 0))]
            self.assertEqual(validate_lab_url("http://lab.test:3000/"), "http://lab.test:3000/")

    def test_rejects_url_with_public_dns(self):
        with patch("scripts.helper.socket.getaddrinfo") as resolver:
            resolver.return_value = [(None, None, None, None, ("8.8.8.8", 0))]
            with self.assertRaises(TargetError):
                validate_lab_url("https://lab.example/")

    def test_wordlist_skips_comments_and_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("# comment\nadmin\n\nlogin\n  # another\n", encoding="utf-8")
            self.assertEqual(load_wordlist(path), ["admin", "login"])


if __name__ == "__main__":
    unittest.main()
