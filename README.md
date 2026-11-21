# HackerLab

**A beginner-friendly, local-first security learning workspace for Kali Linux, defensive workflows and secure development.**

HackerLab wraps common discovery tools in small Python scripts, explains their results, and demonstrates a secure-coding lesson. The static web dashboard adds a curated directory of security tools, guided workflows, offline scanner-output analyzers, browser-side utilities, XP-based learning progress, a saved finding library and a Markdown finding-report draft.

> **Scope and safety:** The network wrappers resolve the target and reject public/non-lab IP addresses. They are not designed for scanning arbitrary Internet hosts. Only assess systems you own or have explicit written permission to test. The GitHub Actions workflow runs unit tests only; it does not run network scans.

## What's included

### Local lab toolkit

- **Nmap:** conservative TCP connect scan (`-sT`) with service/version detection and JSON output.
- **Gobuster:** low-concurrency directory discovery, limited to loopback/private web targets, with a wildcard response-length exclusion option.
- **WPScan:** passive WordPress detection for a local WordPress test environment; no username enumeration or password attacks.
- **SQL injection concept demo:** an in-memory SQLite example comparing unsafe SQL construction with parameterized queries.
- **Safety guard:** rejects public IP targets and URLs that resolve outside private/loopback/link-local ranges.
- **Tests + CI:** standard-library unit tests run on pushes and pull requests.
- **Docker lab:** OWASP Juice Shop and a Kali-based toolbox on an internal-only Docker network.

### Web dashboard

- Searchable tool directory with six categories: network, web/API, code and supply chain, cloud and containers, defence and response, and learning.
- Guided workflows for asset discovery, web application review, secure code release, and defensive investigation.
- Offline scanner-output analyzers for Nmap port output, Gobuster/directory paths and raw HTTP responses, each with prioritised observations and a one-click "add to report" action.
- Eleven browser-side utilities: secure password generation, SHA-256 hashing, JSON formatting, URL encoding/decoding, HTTP security-header checklist, IPv4/CIDR subnet helper, Base64 encoding/decoding, JWT inspection, password-strength/entropy estimation, hash-format identification and a CVSS 3.1 base-score calculator.
- Learning milestones with XP, levels and badges saved in the browser, a saved finding library, and JSON export/import of progress and findings.
- Markdown security finding report builder with editable saved findings.
- Clear labels distinguishing repository tools from external projects and training references.

The dashboard is a static information and utility interface. Its external tool catalogue does not mean those tools are installed or integrated. It does not execute scanners, connect to Kali, or send pasted output to a server. See [docs/dashboard-guide.md](docs/dashboard-guide.md) and [docs/deployment.md](docs/deployment.md).

## Repository layout

```text
hackerlab/
├── .github/workflows/ci.yml
├── docs/
│   ├── dashboard-guide.md
│   ├── deployment.md
│   └── lab-setup.md
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
├── index.html
└── README.md
```

## Quick start

Run the unit tests and SQL injection lesson:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/exploit_demo.py
```

Start the isolated lab:

```bash
docker compose up -d juice-shop
docker compose build hackerlab
```

Open Juice Shop on the Kali host at `http://172.29.250.10:3000`. The lab uses an internal Docker network; the target is not published on a public interface. For detailed setup and commands, see [docs/lab-setup.md](docs/lab-setup.md).

Open the dashboard by visiting the deployed Vercel site or opening `index.html` in a browser. Some browser-native cryptographic features, such as SHA-256 hashing and secure password generation, require a secure browser context and Web Crypto support.

## Example commands

From inside the HackerLab container:

```bash
# Discover the Juice Shop service
python3 scripts/nmap_scan.py juice-shop --ports 3000

# Directory discovery (exclude the observed SPA catch-all response)
python3 scripts/gobuster_scan.py http://juice-shop:3000 wordlists/lab-small.txt --threads 5 --exclude-length 9984

# Passive WordPress checks against a local WordPress lab
python3 scripts/wpscan_scan.py http://127.0.0.1/
```

## Important design choices

- No privileged container mode is required for the supplied Nmap TCP connect scan.
- The Compose lab uses an internal Docker network and a fixed RFC1918 address; it has no normal route to the public Internet.
- No automated scan is run from GitHub Actions against a production or third-party host.
- There is no real-world exploit payload or remote exploit script in this starter release.
- The target guard is a safety aid, not a substitute for authorisation or careful lab network isolation.
- WPScan's local metadata is preloaded when building the toolbox image. Online vulnerability data is optional and requires your own WPScan API token; do not commit API tokens.
- The web dashboard has no scanner backend, remote shell, user account system, or server-side storage.

## License

MIT. See [LICENSE](LICENSE).
