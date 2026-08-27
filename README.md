# Secure Coding Review

A Python security review project completed as part of my Internship.

## Project Overview

This project demonstrates the identification and remediation of common security vulnerabilities in a Python authentication application.

The project contains both a vulnerable version and a remediated secure version.

## Files

- `vulnerable_app.py` — Original application containing intentional security vulnerabilities.
- `bandit_report.txt` — Bandit report generated from the vulnerable application.
- `SECURITY_REVIEW.md` — Detailed security review documenting the vulnerabilities and their remediation.
- `secure_app.py` — Remediated version with security improvements.
- `secure_bandit_report.txt` — Bandit report for the secure application.

## Security Issues Reviewed

The vulnerable application was reviewed for issues including:

- Hardcoded credentials
- Weak MD5 password hashing
- SQL injection risks
- Unsafe file path handling
- Overly broad exception handling

## Security Improvements

The secure version implements:

- PBKDF2-HMAC-SHA256 password hashing
- Unique random password salts
- Parameterized SQL queries
- Input validation
- Path traversal protection
- Safer exception handling

## Security Verification

Bandit was used to perform automated static security analysis.

### Vulnerable Version

The initial scan identified:

- 2 High severity issues
- 2 Medium severity issues
- 1 Low severity issue

### Secure Version

The remediated application was scanned again:

```text
No issues identified.
```
