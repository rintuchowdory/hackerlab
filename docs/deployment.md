# HackerLab web dashboard deployment

The dashboard is a static, read-only learning interface with browser-side utilities. It does not execute security tools, call the Kali host, accept scan targets, or expose OWASP Juice Shop.

## Vercel environments

- Production branch: `main`
- Preview branch: feature branches and pull requests
- Framework preset: Other / static
- Build command: none
- Output directory: repository root (`.`)

## Dashboard capabilities

See [dashboard-guide.md](dashboard-guide.md) for the feature guide. The dashboard contains a searchable security-tool catalogue, guided workflows, local browser utilities, learning progress and a finding-report draft builder. External catalogue entries are links to independent projects; they are not installed or connected integrations.

## Safety boundary

Keep the Docker Compose lab on the local Kali machine or a private, isolated Docker host. Do not deploy Juice Shop publicly. Do not add scanner endpoints, remote command execution, credentials, API tokens, or private lab network addresses to this static site. Do not make the dashboard an unrestricted public scanning service.

Browser-side utility logic runs on the user's device. Learning progress is saved in browser local storage. Do not enter real secrets or sensitive production data into shared browser profiles.

## Local check

Open `index.html` in a browser. The page has no build-time dependencies and uses browser-native HTML, CSS and JavaScript. SHA-256 and secure password generation rely on the Web Crypto API and a secure browser context such as HTTPS.
