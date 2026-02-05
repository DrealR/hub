---
description: Query NEXUS knowledge base - search crystals, recall decisions, find patterns
argument-hint: <search query>
allowed-tools: Read, Glob, Grep
---

# 💎 NEXUS RECALL

**Query:** $ARGUMENTS

> "The crystals have preserved much. What wisdom would you access?" — Fortress Mode

---

## RECALL PROTOCOL

### Step 1: Load Knowledge Base

```
Read .nexus/memory/crystals.json
Parse all crystal types:
- decisions
- patterns
- wisdom
- legacy
```

### Step 2: Parse Search Query

Analyze $ARGUMENTS for:
- **Keywords:** Extract significant terms
- **Type hints:** "decision about", "pattern for", "why did we"
- **Time references:** "last week", "when we started"
- **Project references:** specific project names

### Step 3: Search Strategy

**Keyword Matching:**
- Search all crystal text fields
- Weight by relevance (title > content > tags)

**Type Filtering:**
- "why" queries → prioritize decisions
- "how" queries → prioritize patterns
- "lesson" queries → prioritize wisdom
- "history" queries → prioritize legacy

**Semantic Matching:**
- Related terms and synonyms
- Context similarity

### Step 4: Rank Results

Score each crystal:
```
score = (
  keyword_matches * 0.4 +
  type_relevance * 0.3 +
  recency * 0.15 +
  importance * 0.15
)
```

Return top 5 results.

### Step 5: Format Response (Fortress Style)

```
╔═══════════════════════════════════════════════════════════════╗
║               CRYSTAL ARCHIVES: "[query]"                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ◆ [CRYSTAL TYPE] - [Title/Summary]                          ║
║    Created: [date]                                            ║
║    ─────────────────────────────────────────────              ║
║    [Content]                                                  ║
║                                                               ║
║    Tags: [tag1] [tag2] [tag3]                                 ║
║    Relevance: ████████░░ [XX]%                                ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ◆ [Next Result...]                                           ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  The crystals remember [X] related insights.                  ║
║  "Learn from what came before, but do not be bound by it."    ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## SPECIAL QUERIES

### "why did we [decision]"
Searches decision crystals for architectural choices:
> "The crystals reveal: On [date], you decided to [decision] because [reasoning]."

### "how to [pattern]"
Searches pattern crystals for code solutions:
> "This pattern has been preserved: [code example with context]"

### "what happened with [project]"
Searches legacy crystals for project history:
> "The legacy records show: [project story and milestones]"

### "lessons about [topic]"
Searches wisdom crystals for insights:
> "The wisdom archive contains [X] insights about [topic]..."

---

## MODE-SPECIFIC RESPONSES

**STARK:**
> "Ah yes, I recall this quite clearly. On [date], we decided..."

**BATCAVE:**
> "Cross-referencing evidence database... Pattern match found."

**FORTRESS:**
> "The crystals remember this well. Let me share their wisdom..."

**CITADEL:**
> "Yeah, yeah, you did that thing. It's in here somewhere. Here."

**BRAINIAC:**
> "I have catalogued this information. Retrieving... complete."

---

## EXECUTION

Now search for: **$ARGUMENTS**

1. Load `.nexus/memory/crystals.json`
2. Parse the search query
3. Search across all crystal types
4. Rank results by relevance
5. Format response based on current mode
6. Suggest related crystals if available

---

*"What knowledge do you seek, Reemy?"*
