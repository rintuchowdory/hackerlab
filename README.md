# HackerLab

**A beginner-friendly, lab-only security learning toolkit for Kali Linux and GitHub.**

HackerLab wraps common discovery tools in small Python scripts, explains their results, and demonstrates one secure-coding lesson. It is intended for your own loopback/private lab machines, such as OWASP Juice Shop or a deliberately vulnerable WordPress VM.

> **Scope and safety:** The network wrappers resolve the target and reject public/non-lab IP addresses. They are not designed for scanning arbitrary Internet hosts. Only assess systems you own or have explicit written permission to test. The GitHub Actions workflow runs unit tests only; it does not run network scans.

## Features

- **Nmap:** conservative TCP connect scan (`-sT`) with service/version detection and JSON output.
- **Gobuster:** low-concurrency directory discovery, limited to loopback/private web targets.
- **WPScan:** passive WordPress detection with a 500 ms throttle; no username enumeration or password attacks.
- **SQL injection concept demo:** an in-memory SQLite example comparing unsafe SQL construction with parameterized queries.
- **Safety guard:** rejects public IP targets and URLs that resolve outside private/loopback/link-local ranges.
- **Tests + CI:** standard-library unit tests run on pushes and pull requests.
- **Docker lab:** optional OWASP Juice Shop service and a Kali-based toolbox container.

## Repository layout

```text
hackerlab/
├── .github/workflows/ci.yml
├── docs/lab-setup.md
├── scripts/
│   ├── helper.py
│   ├── nmap_scan.py
│   ├── gobuster_scan.py
│   ├── wpscan_scan.py
│   └── exploit_demo.py
├── tests/
├── wordlists/lab-small.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 scripts/exploit_demo.py
```

See [docs/lab-setup.md](docs/lab-setup.md) for installing scanner binaries and starting the isolated Juice Shop lab.

## Example commands

```bash
# Local machine only
python3 scripts/nmap_scan.py 127.0.0.1 --ports 22,80,443,3000

# Directory discovery against a local lab web app
python3 scripts/gobuster_scan.py http://127.0.0.1:3000 wordlists/lab-small.txt --threads 5

# Passive WordPress checks against a local WordPress lab
python3 scripts/wpscan_scan.py http://127.0.0.1/
```

## Important design choices

- No privileged container mode is required for the supplied Nmap TCP connect scan.
- No automated scan is run from GitHub Actions against a production or third-party host.
- There is no real-world exploit payload or remote exploit script in this starter release.
- The target guard is a safety aid, not a substitute for authorisation or careful lab network isolation.

## License

MIT. See [LICENSE](LICENSE).
