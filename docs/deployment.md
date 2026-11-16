# HackerLab web dashboard deployment

The dashboard is a static, read-only learning interface. It does not execute security tools, call the Kali host, or expose OWASP Juice Shop.

## Vercel environments

- Production branch: `main`
- Preview branch: feature branches and pull requests (including `preview-dashboard`)
- Framework preset: Other / static
- Build command: none
- Output directory: repository root (or `.`)

## Safety boundary

Keep the Docker Compose lab on the local Kali machine or a private, isolated Docker host. Do not deploy Juice Shop publicly. Do not add scanner endpoints, credentials, API tokens, or private lab network addresses to this static site.

## Local check

Open `index.html` in a browser. The page has no build-time dependencies and uses only browser-native HTML, CSS and JavaScript.
