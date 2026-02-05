# Deploy Checklist

Pre-deployment verification for: $ARGUMENTS

---

## Composable Command

**This command automatically includes:**
- `check` - Full quality gate
- `security-scan` - Vulnerability assessment

---

## Deployment Protocol

### Phase 1: Quality Gate (via check)

Run all checks:
- [ ] Lint: No errors
- [ ] Types: No errors
- [ ] Tests: All passing
- [ ] Build: Succeeds

### Phase 2: Security (via security-scan)

Full security assessment:
- [ ] Dependency vulnerabilities
- [ ] OWASP Top 10 checks
- [ ] Secret detection
- [ ] Configuration review

### Phase 3: Pre-Deploy Verification

**Dependencies:**
- [ ] Lock file up to date
- [ ] No deprecated packages
- [ ] License compliance

**Database (if applicable):**
- [ ] Migrations tested
- [ ] Rollback works
- [ ] Backup taken

**Documentation:**
- [ ] CHANGELOG updated
- [ ] API docs current
- [ ] Release notes ready

**Configuration:**
- [ ] Env vars set in target
- [ ] Feature flags configured
- [ ] Monitoring ready

### Phase 4: Deployment Steps

```bash
# 1. Tag release
git tag -a v<version> -m "Release v<version>"
git push origin v<version>

# 2. Deploy to staging
<staging deploy command>

# 3. Verify staging
# 4. Deploy to production
<production deploy command>

# 5. Post-deploy verification
```

### Phase 5: Rollback Plan

Document rollback procedure:
```bash
# Immediate rollback
git revert <commit>
# or redeploy previous version

# Database rollback (if needed)
<migration rollback command>
```

---

## Linked Commands

This command uses:
- `check` - Quality gate (automatic)
- `security-scan` - Security assessment (automatic)

Typically used after:
- `/project:flow ship` - After shipping
- `/project:pr-review` - After approval

---

## Output

```
┌─────────────────────────────────────────┐
│         DEPLOY CHECKLIST                │
├─────────────────────────────────────────┤
│ Target: $ARGUMENTS                      │
│ Version: v1.2.3                         │
├─────────────────────────────────────────┤
│ QUALITY GATE (via /check)               │
│ └── All checks passed ✓                 │
├─────────────────────────────────────────┤
│ SECURITY (via /security-scan)           │
│ ├── Vulnerabilities: 0 critical         │
│ ├── OWASP: 10/10 passed                 │
│ └── Secrets: None detected              │
├─────────────────────────────────────────┤
│ PRE-DEPLOY                              │
│ ├── Dependencies: ✓                     │
│ ├── Database: ✓                         │
│ ├── Documentation: ✓                    │
│ └── Configuration: ✓                    │
├─────────────────────────────────────────┤
│ STATUS: READY TO DEPLOY ✓               │
│ Rollback: Documented                    │
└─────────────────────────────────────────┘
```

---

**Now run deploy checklist for: $ARGUMENTS**
