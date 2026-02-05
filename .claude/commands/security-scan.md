# Security Scan

Perform a comprehensive security assessment: $ARGUMENTS

---

## Security Assessment Protocol

### Phase 1: Dependency Vulnerabilities

```bash
# Node.js
npm audit
# or
yarn audit

# Python
pip-audit
# or
safety check

# Go
govulncheck ./...

# Rust
cargo audit
```

### Phase 2: Code Analysis

**OWASP Top 10 Checks:**

1. **A01: Broken Access Control**
   - [ ] Authorization checks on all endpoints
   - [ ] No direct object references exposed
   - [ ] Proper CORS configuration

2. **A02: Cryptographic Failures**
   - [ ] No hardcoded secrets
   - [ ] Secure hashing algorithms (not MD5/SHA1)
   - [ ] HTTPS enforced

3. **A03: Injection**
   - [ ] SQL injection prevention (parameterized queries)
   - [ ] Command injection prevention
   - [ ] XSS prevention (output encoding)

4. **A04: Insecure Design**
   - [ ] Rate limiting implemented
   - [ ] Input validation present
   - [ ] Secure defaults

5. **A05: Security Misconfiguration**
   - [ ] No debug mode in production
   - [ ] Proper error handling (no stack traces)
   - [ ] Security headers set

6. **A06: Vulnerable Components**
   - [ ] Dependencies up to date
   - [ ] No known CVEs
   - [ ] Minimal dependencies

7. **A07: Authentication Failures**
   - [ ] Strong password policies
   - [ ] Session management secure
   - [ ] MFA available

8. **A08: Data Integrity Failures**
   - [ ] CI/CD pipeline secure
   - [ ] No unsigned packages
   - [ ] Integrity verification

9. **A09: Logging Failures**
   - [ ] Security events logged
   - [ ] No sensitive data in logs
   - [ ] Log injection prevented

10. **A10: SSRF**
    - [ ] URL validation on external requests
    - [ ] Allowlist for external services

### Phase 3: Secret Detection

Scan for exposed secrets:
```bash
# Check for common patterns
grep -rn "password\s*=" .
grep -rn "api_key\s*=" .
grep -rn "secret\s*=" .
grep -rn "token\s*=" .
```

Check files that shouldn't exist:
- `.env` (should be `.env.example`)
- `*.pem`, `*.key`
- `credentials.json`
- `*.secret`

### Phase 4: Configuration Review

Check security configurations:
- [ ] `.gitignore` includes secrets
- [ ] Environment variables used for secrets
- [ ] Production config separate from dev
- [ ] CSP headers configured
- [ ] HSTS enabled

## Output Format

```
┌─────────────────────────────────────────┐
│         SECURITY SCAN RESULTS           │
├─────────────────────────────────────────┤
│ Scan Target: $ARGUMENTS                 │
│ Date: <timestamp>                       │
├─────────────────────────────────────────┤
│ VULNERABILITIES                         │
│ ├── Critical: 0                         │
│ ├── High: 1                             │
│ ├── Medium: 3                           │
│ └── Low: 5                              │
├─────────────────────────────────────────┤
│ OWASP COMPLIANCE                        │
│ ├── Passed: 8/10                        │
│ └── Failed: A03, A06                    │
├─────────────────────────────────────────┤
│ SECRETS DETECTED: 0                     │
└─────────────────────────────────────────┘

## Critical Findings

### 🔴 HIGH: SQL Injection in user query
**File:** src/api/users.ts:42
**Issue:** User input directly concatenated in SQL
**Fix:** Use parameterized queries

### 🟠 MEDIUM: Outdated dependency
**Package:** lodash@4.17.15
**CVE:** CVE-2021-23337
**Fix:** Upgrade to lodash@4.17.21
```

---

**Now perform a security scan on: $ARGUMENTS**
