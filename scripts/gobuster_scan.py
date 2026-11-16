#!/usr/bin/env python3
"""Run low-concurrency Gobuster directory discovery against a private lab web app."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    from helper import TargetError, load_wordlist, validate_lab_url
else:
    from .helper import TargetError, load_wordlist, validate_lab_url


def run_gobuster(target: str, wordlist: str, extensions: str = "", threads: int = 5,
                 output: str = "gobuster-results.txt", timeout: int = 300) -> dict:
    safe_url = validate_lab_url(target)
    wordlist_path = Path(wordlist).expanduser().resolve()
    if not wordlist_path.is_file():
        raise FileNotFoundError(f"Wordlist not found: {wordlist_path}")
    if not 1 <= threads <= 10:
        raise ValueError("Thread count must be between 1 and 10 for this learning tool.")
    if extensions and not all(part.strip(" .").isalnum() for part in extensions.split(",")):
        raise ValueError("Extensions must be simple comma-separated suffixes such as php,html,txt.")
    if shutil.which("gobuster") is None:
        raise RuntimeError("Gobuster is not installed. Install it with your system package manager.")
    output_path = Path(output).expanduser().resolve()
    if output_path.exists():
        output_path.unlink()
    command = ["gobuster", "dir", "--url", safe_url, "--wordlist", str(wordlist_path),
               "--threads", str(threads), "--output", output]
    if extensions:
        command.extend(["--extensions", extensions])
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or
                           f"Gobuster exited with code {completed.returncode}")
    content = output_path.read_text(encoding="utf-8", errors="replace") if output_path.exists() else completed.stdout
    return {"scanner": "gobuster", "target": safe_url, "output_file": str(output_path),
            "raw_output": content, "return_code": completed.returncode}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="http(s) URL hosted on loopback/private lab network")
    parser.add_argument("wordlist", help="Path to a local wordlist")
    parser.add_argument("--extensions", default="", help="Optional suffixes: php,html,txt")
    parser.add_argument("--threads", type=int, default=5, help="1-10 (default: 5)")
    parser.add_argument("--output", default="gobuster-results.txt")
    args = parser.parse_args()
    try:
        result = run_gobuster(args.target, args.wordlist, args.extensions, args.threads, args.output)
        print(json.dumps(result, indent=2))
        return 0
    except (TargetError, ValueError, FileNotFoundError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
