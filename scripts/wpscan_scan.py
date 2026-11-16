#!/usr/bin/env python3
"""Run passive WPScan checks against a private lab WordPress site."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    from helper import TargetError, validate_lab_url
else:
    from .helper import TargetError, validate_lab_url


def run_wpscan(target: str, output: str = "wpscan-results.json", timeout: int = 300) -> dict:
    safe_url = validate_lab_url(target)
    if shutil.which("wpscan") is None:
        raise RuntimeError("WPScan is not installed. Install it with your system package manager.")
    output_path = Path(output).expanduser().resolve()
    if output_path.exists():
        output_path.unlink()
    command = [
        "wpscan", "--url", safe_url, "--format", "json", "--output", str(output_path),
        "--no-update", "--detection-mode", "passive", "--throttle", "500",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    if output_path.exists():
        try:
            report = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"WPScan output was not valid JSON: {exc}") from exc
    else:
        report = {"raw_output": completed.stdout}
    return {
        "scanner": "wpscan",
        "target": safe_url,
        "report": report,
        "return_code": completed.returncode,
        "stderr": completed.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="WordPress URL hosted on loopback/private lab network")
    parser.add_argument("--output", default="wpscan-results.json")
    args = parser.parse_args()
    try:
        result = run_wpscan(args.target, args.output)
        print(json.dumps(result, indent=2))
        return 0 if result["return_code"] == 0 else 1
    except (TargetError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
