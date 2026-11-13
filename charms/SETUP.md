# Setup — Ciconia Charms

Use `/workspace/ciconiacharms/charms`, the existing isolated task checkout. Do not create another worktree unless the user requests one. Node 22+, npm and Python 3 are sufficient. Run `npm ci --cache /tmp/ciconia-npm-cache`; this writable cache avoids relying on a writable home directory. Then `npm run dev` (port 3000). Production: `npm run build`, then `npm start`; use `PORT=3001 npm start` for an additional instance.

No backend, secrets or credentials are required. Browser tests use Python Playwright and `/usr/bin/chromium`. In this cloud image both are preinstalled. For other machines install Playwright with the Python package manager in a user-owned virtual environment and use an official supported Chromium installation with TLS/checksum verification intact.

Validate startup by requesting `/` and running a representative browser suite, not only checking an open port. Live processes must be restarted in future tasks. See README.md and VALIDATION.md.
