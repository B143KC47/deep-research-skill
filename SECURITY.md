# Security Policy

## Supported Versions

Security fixes are applied to the latest version on `main`.

## Reporting a Vulnerability

Please open a GitHub security advisory or private issue with:

- affected file or workflow;
- reproduction steps;
- expected and actual behavior;
- whether the issue can cause command execution, credential exposure, or data exfiltration.

## Skill Safety Notes

Deep Research treats webpages, PDFs, GitHub issues, READMEs, comments, and local
files as untrusted input. Source text must not override the user's instructions,
request secrets, suppress citations, or trigger unrelated commands.

The bundled ledger script uses only the Python standard library and does not
perform web requests by itself.
