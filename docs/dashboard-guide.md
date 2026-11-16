# HackerLab dashboard guide

The HackerLab dashboard is a static, local-first learning workspace. It is designed to help a learner choose tools by task, follow repeatable defensive workflows, and document findings.

## Dashboard capabilities

- Search and category filters for network, web/API, code and supply-chain, cloud/container, defence/response, and learning resources.
- Clear distinction between tools already represented in this repository and third-party tools that are external references only.
- Guided workflows for asset discovery, web application review, secure code release, and defensive investigation.
- Six browser-side utilities: password generation with Web Crypto, SHA-256 text hashing, JSON formatting/validation, URL component encoding/decoding, a pasted HTTP security-header checklist, and an IPv4/CIDR subnet helper.
- Browser-local learning progress and a Markdown security finding report draft.

## What's actually in this repository

The local HackerLab lab includes the Python wrappers and exercises described in the root README: Nmap, Gobuster, passive WPScan checks, the in-memory SQLite parameterisation lesson, and the target safety helper. The dashboard's third-party directory links to external projects and documentation. Those projects are not installed, licensed, configured, or remotely connected by the dashboard.

## Local startup

Run these commands from the repository root on your Kali host:

```bash
docker compose up -d juice-shop
docker compose build hackerlab
docker compose run --rm hackerlab
```

Run the test suite without launching a scan:

```bash
python3 -m unittest discover -s tests -v
```

## Browser utility privacy

The utility calculations are performed in the browser. Learning progress is saved in the browser's local storage. The static dashboard does not send these utility inputs to an API. Do not paste live credentials, personal information, or sensitive production data into shared devices or browser profiles. SHA-256 uses the Web Crypto API and requires a secure browser context such as HTTPS.

## Safety and scope

- Only assess systems you own or are explicitly authorised to test.
- Keep OWASP Juice Shop on the private Docker lab network. Do not publish it to the public Internet.
- The Vercel dashboard does not execute scanners, connect to Kali, or accept scan targets.
- The third-party directory is a learning catalogue, not an endorsement or security guarantee. Review each project's documentation, licence, requirements, and current maintenance status before adopting it.
- The dashboard's HTTP header review is a basic checklist, not a full application security assessment. Subnet output is an educational planning aid; independently verify network configuration before making changes.
