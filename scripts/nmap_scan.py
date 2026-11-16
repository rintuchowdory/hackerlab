#!/usr/bin/env python3
"""Run a conservative Nmap TCP connect/version scan against a local lab target."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if __package__ in {None, ""}:
    from helper import TargetError, validate_lab_target
else:
    from .helper import TargetError, validate_lab_target

PORT_SPEC = re.compile(r"^[0-9,\-]+$")


def parse_nmap_xml(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)
    hosts: list[dict] = []
    for host in root.findall("host"):
        addresses = [item.get("addr") for item in host.findall("address") if item.get("addr")]
        hostnames = [item.get("name") for item in host.findall("hostnames/hostname") if item.get("name")]
        ports: list[dict] = []
        for port in host.findall("ports/port"):
            state = port.find("state")
            service = port.find("service")
            ports.append({
                "port": int(port.get("portid", "0")),
                "protocol": port.get("protocol", "tcp"),
                "state": state.get("state") if state is not None else "unknown",
                "service": service.get("name") if service is not None else "unknown",
                "product": service.get("product") if service is not None else None,
                "version": service.get("version") if service is not None else None,
                "extra_info": service.get("extrainfo") if service is not None else None,
            })
        hosts.append({"addresses": addresses, "hostnames": hostnames, "ports": ports})
    return {"scanner": "nmap", "hosts": hosts}


def run_scan(target: str, ports: str = "1-1024", timeout: int = 180) -> dict:
    safe_target = validate_lab_target(target)
    if not PORT_SPEC.fullmatch(ports) or not ports:
        raise ValueError("Ports must use Nmap's numeric form, e.g. 22,80,443 or 1-1024.")
    if shutil.which("nmap") is None:
        raise RuntimeError("Nmap is not installed. Install it with your system package manager.")
    command = [
        "nmap", "-sT", "-sV", "-T3", "--reason", "--max-retries", "2",
        "--host-timeout", "150s", "-p", ports, "-oX", "-", safe_target,
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr.strip() or f"Nmap exited with code {completed.returncode}")
    result = parse_nmap_xml(completed.stdout)
    result["target"] = safe_target
    result["command"] = command
    if completed.stderr.strip():
        result["warnings"] = completed.stderr.strip()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Loopback/private lab hostname or IP only")
    parser.add_argument("--ports", default="1-1024", help="Ports, e.g. 22,80,443 or 1-1024")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()
    try:
        result = run_scan(args.target, args.ports)
        rendered = json.dumps(result, indent=2)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0
    except (TargetError, ValueError, RuntimeError, subprocess.TimeoutExpired, ET.ParseError) as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
