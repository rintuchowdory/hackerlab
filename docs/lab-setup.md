# Isolated lab setup

HackerLab is designed for systems you own or are explicitly authorised to assess. Its network wrappers reject targets that resolve to public IP addresses. Keep the practice target isolated and do not publish vulnerable lab ports to the Internet.

## Option A: Docker Compose + OWASP Juice Shop

Requirements: Docker Engine and the Docker Compose plugin.

From the repository root:

```bash
docker compose up -d juice-shop
docker compose build hackerlab
docker compose run --rm hackerlab
```

Inside the HackerLab container, the Juice Shop service is reachable by its Compose DNS name:

```bash
python3 scripts/nmap_scan.py juice-shop --ports 3000
python3 scripts/gobuster_scan.py http://juice-shop:3000 wordlists/lab-small.txt --threads 5
```

The web app is also published to the host at `http://127.0.0.1:3000` only. Stop the lab with:

```bash
docker compose down
```

## Option B: Kali or Debian/Ubuntu host

Install Python 3 and the scanner tools using your distribution package manager. On Kali:

```bash
sudo apt update
sudo apt install -y python3 nmap gobuster wpscan seclists
```

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Use a private/loopback lab address, for example `127.0.0.1`, `192.168.56.10`, or a Docker service name resolving to a private container address.

## Tool examples

Nmap, limited to selected ports:

```bash
python3 scripts/nmap_scan.py 127.0.0.1 --ports 22,80,443,3000 --output nmap-results.json
```

Gobuster, low concurrency:

```bash
python3 scripts/gobuster_scan.py http://127.0.0.1:3000 wordlists/lab-small.txt --threads 5 --output gobuster-results.txt
```

WPScan, passive detection only, for a WordPress lab:

```bash
python3 scripts/wpscan_scan.py http://127.0.0.1/ --output wpscan-results.json
```

The WPScan wrapper intentionally does not enumerate usernames, attempt passwords, or use aggressive plugin/theme detection. It uses passive detection with a 500 ms request throttle.

## Safe SQL injection concept demo

This simulation uses a temporary in-memory SQLite database. It does not connect to a network service or exploit a website:

```bash
python3 scripts/exploit_demo.py
```

It contrasts unsafe string concatenation with a parameterized query and explains the defensive fix.
