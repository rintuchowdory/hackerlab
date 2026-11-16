"""Shared safety and parsing helpers for HackerLab.

Network tools are deliberately restricted to loopback or private lab IPs.
Public Internet targets are rejected by default; there is no bypass flag.
"""
from __future__ import annotations

import ipaddress
import json
import socket
from pathlib import Path
from urllib.parse import urlsplit


class TargetError(ValueError):
    """Raised when a target is outside the supported lab scope."""


def _resolve_addresses(host: str) -> set[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    try:
        answers = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError) as exc:
        raise TargetError(f"Could not resolve target {host!r}: {exc}") from exc
    addresses: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
    for answer in answers:
        raw = answer[4][0].split("%", 1)[0]
        try:
            addresses.add(ipaddress.ip_address(raw))
        except ValueError:
            continue
    if not addresses:
        raise TargetError(f"Target {host!r} did not resolve to an IP address.")
    return addresses


def _is_lab_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    # Explicitly allow loopback, RFC1918 IPv4, IPv6 ULA and link-local lab ranges.
    if address.is_unspecified or address.is_multicast:
        return False
    if address.is_loopback or address.is_link_local:
        return True
    if isinstance(address, ipaddress.IPv4Address):
        private_v4 = (
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("192.168.0.0/16"),
        )
        return any(address in network for network in private_v4)
    return address in ipaddress.ip_network("fc00::/7")


def validate_lab_target(target: str) -> str:
    """Validate and return a host suitable for an isolated lab scan."""
    host = target.strip()
    if not host or any(ch.isspace() for ch in host):
        raise TargetError("Target must be a hostname or IP address without spaces.")
    if "://" in host or "/" in host or "@" in host:
        raise TargetError("Pass a hostname/IP here, not a URL or path.")
    addresses = _resolve_addresses(host)
    public = sorted(str(ip) for ip in addresses if not _is_lab_ip(ip))
    if public:
        raise TargetError(
            "Target resolves to a public or non-lab address "
            f"({', '.join(public)}). HackerLab only scans loopback/private lab targets."
        )
    return host


def validate_lab_url(url: str) -> str:
    """Validate an HTTP(S) URL and ensure every resolved address is lab-local."""
    candidate = url.strip()
    parts = urlsplit(candidate)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise TargetError("Target must be a complete http:// or https:// URL.")
    if parts.username or parts.password:
        raise TargetError("Do not put credentials in the target URL.")
    validate_lab_target(parts.hostname)
    return candidate


def load_wordlist(path: str | Path) -> list[str]:
    """Load non-empty, non-comment wordlist entries."""
    wordlist = Path(path)
    if not wordlist.is_file():
        raise FileNotFoundError(f"Wordlist not found: {wordlist}")
    return [
        line.strip()
        for line in wordlist.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def pretty_print_json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))
