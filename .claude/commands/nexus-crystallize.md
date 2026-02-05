---
description: Crystallize knowledge into NEXUS memory - decisions, patterns, wisdom
argument-hint: <insight to crystallize>
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 💎 NEXUS CRYSTALLIZATION

**Insight:** $ARGUMENTS

> "Knowledge is power, but only if you can access it when needed." — Brainiac

---

## CRYSTALLIZATION PROTOCOL

### Step 1: Classify the Insight

Analyze $ARGUMENTS to determine crystal type:

| Type | Indicators | Storage |
|------|------------|---------|
| **Decision** | "chose", "decided", "selected", architectural choice | `crystals.decisions` |
| **Pattern** | Code snippet, reusable solution, implementation detail | `crystals.patterns` |
| **Wisdom** | Lesson learned, insight, philosophical principle | `crystals.wisdom` |
| **Legacy** | Project history, milestone, evolution | `crystals.legacy` |

### Step 2: Extract Metadata

**For Decisions:**
- What was decided?
- Why was it decided?
- What alternatives were considered?
- What's the expected outcome?

**For Patterns:**
- What's the pattern name?
- What language/context?
- What problem does it solve?
- Sample code?

**For Wisdom:**
- What's the core insight?
- In what context was it learned?
- What's the source?
- How important is it?

**For Legacy:**
- Which project?
- What's the story?
- Key milestones?
- Lessons learned?

### Step 3: Create Crystal Structure

```json
{
  "id": "[type]-[timestamp]",
  "created": "[ISO timestamp]",
  // Type-specific fields
  "tags": ["extracted", "tags"]
}
```

### Step 4: Update Memory

1. Read current crystals from `.nexus/memory/crystals.json`
2. Add new crystal to appropriate array
3. Update stats
4. Write back to file

### Step 5: Acknowledge

Respond in NEXUS personality:

**STARK:** "I've crystallized this insight. It will serve us well in future endeavors."

**BATCAVE:** "Evidence catalogued. This pattern has been added to the database."

**FORTRESS:** "The wisdom has been preserved in the crystal archives. It shall endure."

**CITADEL:** "Cool. I mean, sure, knowledge, whatever. It's saved. *burp*"

**BRAINIAC:** "Knowledge acquired and catalogued. My archives expand."

---

## EXECUTION

Now crystallize: **$ARGUMENTS**

1. Read `.nexus/config.json` to get current mode
2. Classify the insight type
3. Extract relevant metadata
4. Create the crystal structure
5. Update `.nexus/memory/crystals.json`
6. Respond in character

---

*The crystals remember. The crystals endure.*
