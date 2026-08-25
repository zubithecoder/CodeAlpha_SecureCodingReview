# Secure Coding Review

## 1. Executive Summary

A security review was performed on a small Python authentication application.

The review used two approaches:

1. Manual source-code inspection
2. Automated static analysis using Bandit 1.9.4

The initial Bandit scan identified five security findings, including hardcoded credentials, weak MD5 password hashing, and possible SQL injection vulnerabilities.

Manual inspection also identified unsafe file access and overly broad exception handling.

A secure version of the application was then created to address the identified security weaknesses.

The remediated application was scanned again with Bandit and returned no security findings.

---

## 2. Security Findings

### Finding 1 — Hardcoded Administrator Password

**Severity:** Low

**CWE:** CWE-259 — Use of Hard-coded Password

**Location:** `vulnerable_app.py`, line 6

```python
ADMIN_PASSWORD = "Admin123"
```
