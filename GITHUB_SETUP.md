# Publish HackerLab to GitHub

From the repository root:

```bash
git init -b main
git add .
git commit -m "feat: add safe lab-only security learning toolkit"
gh auth status
gh repo create hackerlab --public --source=. --remote=origin --push
```

Suggested GitHub topics: `cybersecurity`, `ethical-hacking`, `kali-linux`, `nmap`, `owasp-juice-shop`, `python`, `security-learning`.
