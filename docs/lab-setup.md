# Isolated lab setup

HackerLab is designed for systems you own or are explicitly authorised to assess. Its network wrappers reject targets that resolve to public IP addresses. The Compose lab uses an internal Docker bridge network with a fixed private address for Juice Shop; it is not published on a public interface and the lab containers have no normal route to the public Internet.

## Option A: Docker Compose + OWASP Juice Shop

Requirements: Docker Engine and the Docker Compose plugin.

From the repository root:

```bash
docker compose up -d juice-shop
docker compose build hackerlab
docker compose run --rm hackerlab
```

The Juice Shop container has the fixed private address `172.29.250.10`. On the Kali host, open:

```text
http://172.29.250.10:3000
```

The HackerLab container reaches the same service by its Compose DNS name `juice-shop`. The Docker network is marked internal so the lab containers do not have a normal route to the public Internet. The private bridge address is reachable from the Docker host; it is not a public Internet address.

Open a toolbox shell:

```bash
docker compose run --rm hackerlab
```

Inside the toolbox:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/nmap_scan.py juice-shop --ports 3000
python3 scripts/gobuster_scan.py http://juice-shop:3000 wordlists/lab-small.txt --threads 5
```

Juice Shop is a single-page application that can return the same HTTP 200 response for unknown paths. Gobuster will stop if it detects this wildcard behaviour. In the supplied image, the default response length observed during validation was 9984 bytes. Exclude that length for this specific image/version:

```bash
python3 scripts/gobuster_scan.py http://juice-shop:3000 wordlists/lab-small.txt --threads 5 --exclude-length 9984
```

If the response length changes after an image update, check the new random-path response length and update the value. Do not use `--force` to suppress the precheck.

The Docker image runs `wpscan --update` at build time to preload WPScan's local metadata. The vulnerability data service is separate and requires an optional WPScan API token; no token is included in this repository.

Stop the lab with:

```bash
docker compose down
```

## Option B: Kali or Debian/Ubuntu host

Install Python 3 and the scanner tools using your distribution package manager. On Kali:

```bash
sudo apt update
sudo apt install -y python3 nmap gobuster wpscan seclists
```

Run WPScan's one-time local metadata update before using the wrapper on a fresh host installation:

```bash
wpscan --update
```

Then run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Use a private/loopback lab address, for example `127.0.0.1`, `192.168.56.10`, or a Docker service name resolving to a private container address.

## Tool examples

Nmap, limited to selected ports:

```bash
python3 scripts/nmap_scan.py 172.29.250.10 --ports 22,80,443,3000 --output nmap-results.json
```

Gobuster, low concurrency:

```bash
python3 scripts/gobuster_scan.py http://172.29.250.10:3000 wordlists/lab-small.txt --threads 5 --output gobuster-results.txt
```

If the lab app has a catch-all response, use its observed response length with `--exclude-length`.

WPScan, passive detection only, for a local WordPress lab:

```bash
python3 scripts/wpscan_scan.py http://127.0.0.1/ --output wpscan-results.json
```

The WPScan wrapper intentionally uses passive detection with a 500 ms request throttle. It does not enumerate usernames, attempt passwords, or request aggressive plugin/theme enumeration. Vulnerability details from WPScan's online API require the user's own API token; do not commit that token.

## Safe SQL injection concept demo

This simulation uses a temporary in-memory SQLite database. It does not connect to a network service or exploit a website:

```bash
python3 scripts/exploit_demo.py
```

It contrasts unsafe string concatenation with a parameterized query and explains the defensive fix.
