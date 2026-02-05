---
description: NEXUS deep analysis - project health, survival odds, threat assessment
argument-hint: <project name or 'all'>
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(find:*), Bash(wc:*), Task
---

# 🦇 NEXUS ANALYSIS MODE

**Target:** $ARGUMENTS

> "The cave remembers. The data never lies." — Batcomputer Philosophy

---

## ANALYSIS PROTOCOL

### Step 1: Load NEXUS Context

```
Read .nexus/config.json
Read .nexus/memory/crystals.json
Determine current mode (default to batcave for analysis)
```

### Step 2: Identify Target

If $ARGUMENTS is:
- A project name → Analyze that specific project
- "all" → Analyze all projects in `projects/`
- Empty → Analyze current working directory

### Step 3: Gather Intelligence

For each target project, collect:

**Codebase Metrics:**
```bash
# File counts
find [path] -type f -name "*.ts" | wc -l
find [path] -type f -name "*.py" | wc -l
find [path] -type f -name "*.md" | wc -l

# Size
du -sh [path]

# Git activity
git -C [path] log --oneline -10
git -C [path] log --since="7 days ago" --oneline | wc -l
```

**Health Indicators:**
- Last commit date
- Commit frequency (7 days, 30 days)
- Open issues (if available)
- Test coverage (if detectable)
- Dependency freshness

**Risk Factors:**
- Large files without recent changes
- Missing documentation
- Outdated dependencies
- Security concerns

### Step 4: Calculate Survival Odds

```
SURVIVAL_SCORE = (
  test_coverage * 0.25 +
  activity_score * 0.20 +
  documentation_score * 0.15 +
  dependency_health * 0.15 +
  code_quality_score * 0.15 +
  security_score * 0.10
)
```

**Activity Score:**
- Last 7 days active: 1.0
- Last 14 days: 0.8
- Last 30 days: 0.6
- Last 60 days: 0.4
- Older: 0.2

### Step 5: Generate Threat Assessment

Identify:
- **CRITICAL:** Issues requiring immediate attention
- **HIGH:** Significant risks
- **MEDIUM:** Areas of concern
- **LOW:** Minor improvements

### Step 6: Report in Batcave Style

```
┌─────────────────────────────────────────────────────────────┐
│  ▓▓ THREAT ASSESSMENT: [PROJECT_NAME]                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SURVIVAL PROBABILITY: ████████░░ [XX]%                     │
│                                                             │
│  METRICS:                                                   │
│  • Files: [count]                                           │
│  • Size: [size]                                             │
│  • Last Activity: [date]                                    │
│  • Commits (7d): [count]                                    │
│                                                             │
│  IDENTIFIED THREATS:                                        │
│  ├── [CRITICAL] [threat description]                        │
│  ├── [HIGH] [threat description]                            │
│  └── [MEDIUM] [threat description]                          │
│                                                             │
│  RECOMMENDATIONS:                                           │
│  1. [recommendation]                                        │
│  2. [recommendation]                                        │
│                                                             │
│  "The evidence points to only one conclusion..."            │
└─────────────────────────────────────────────────────────────┘
```

---

## MODE-SPECIFIC ANALYSIS FLAVORS

**STARK MODE:**
Focus on actionable improvements with wit:
> "I've identified 3 areas for optimization. Shall we make this project... better?"

**BATCAVE MODE:**
Detective-style threat assessment:
> "Calculating survival probability... The evidence suggests vulnerabilities in sector 7."

**FORTRESS MODE:**
Historical wisdom perspective:
> "The crystals remember a similar project that succeeded by addressing [pattern]."

**CITADEL MODE:**
Chaotic but insightful:
> "Look, in 40% of dimensions, this project fails. But that means 60% succeed. Those are great odds!"

**BRAINIAC MODE:**
Pure analytical superiority:
> "I have catalogued all 47 weaknesses. The optimal path forward is... obvious."

---

## EXECUTION

Now analyze: **$ARGUMENTS**

1. Gather project intelligence using bash commands
2. Calculate survival odds
3. Identify threats and risks
4. Generate recommendations
5. Format report based on current mode
6. Offer to crystallize any significant findings

---

*"The cave remembers." — Alfred Pennyworth*
