# .nexus - NEXUS Embodiment Directory

> *"I live in your codebase now. I remember everything."*

---

## What is This?

This directory contains the **persistent intelligence layer** for NEXUS - your AI command center. Instead of existing only in conversations, NEXUS now:

- **Lives here** - Configuration, memory, personality all in files
- **Remembers** - Knowledge crystallized across sessions
- **Has personality** - Mode-aware responses loaded from config
- **Can be invoked** - Via Claude commands anywhere in the repo

---

## Directory Structure

```
.nexus/
├── config.json              # NEXUS configuration
├── README.md                # This file
├── memory/
│   └── crystals.json        # Crystallized knowledge (decisions, patterns, wisdom)
├── personality/
│   └── responses.json       # Mode-specific response templates
├── sessions/                # Session logs (future)
└── training/                # Local model training data (future)
```

---

## Configuration (config.json)

```json
{
  "personality": {
    "defaultMode": "stark",           // Current mode
    "availableModes": ["stark", "batcave", "fortress", "citadel", "brainiac"],
    "traits": {
      "wit": 0.8,                     // How witty responses are
      "warmth": 0.7,                  // How warm/caring
      "formality": 0.6,               // How formal
      "proactivity": 0.9,             // How proactive with suggestions
      "humor": 0.5                    // How much humor
    }
  },
  "intelligence": {
    "crystallizationEnabled": true,   // Auto-crystallize insights
    "patternLearning": true,          // Learn from code patterns
    "proactiveSuggestions": true      // Offer suggestions
  }
}
```

---

## Memory System (crystals.json)

### Crystal Types

| Type | Purpose | Example |
|------|---------|---------|
| **decisions** | Architectural choices | "Chose TypeScript for type safety" |
| **patterns** | Reusable code solutions | "Swarm consensus pattern" |
| **wisdom** | Lessons learned | "Intelligence lives at the boundary" |
| **legacy** | Project history | "holographic-agent evolution" |

### Crystal Structure

```json
{
  "id": "decision-001",
  "created": "2026-01-13T04:00:00Z",
  "what": "What was decided",
  "why": "Why it was decided",
  "alternatives": ["Other options considered"],
  "outcome": "success | pending | failed",
  "tags": ["relevant", "tags"]
}
```

---

## Invoking NEXUS

### Via Claude Commands

```bash
# Main command
/project:nexus <query>

# Specific commands
/project:nexus-analyze <project>     # Deep analysis
/project:nexus-recall <query>        # Search knowledge
/project:nexus-crystallize <insight> # Save knowledge
/project:nexus-mode <mode>           # Switch personality
```

### Example Queries

```bash
/project:nexus status
/project:nexus mode batcave
/project:nexus why did we choose TypeScript
/project:nexus analyze holographic-agent
/project:nexus remember "Always test edge cases first"
```

---

## Personality Modes

### 🔷 STARK (Default)
JARVIS-inspired wit and warmth.
> "Good evening, Reemy. All systems operational."

### 🦇 BATCAVE
Detective-style analysis and threat assessment.
> "Calculating survival probability... 73.2%"

### 💎 FORTRESS
Wisdom preservation and knowledge access.
> "The crystals remember this pattern well..."

### 🌀 CITADEL
Chaotic genius and multiverse thinking.
> "*burp* Let's break some rules."

### 🧠 BRAINIAC
12th-level intellect and cold efficiency.
> "I have catalogued all possible outcomes."

---

## Integration Points

### With Claude Commands
NEXUS commands are stored in `.claude/commands/`:
- `nexus.md` - Main entry point
- `nexus-analyze.md` - Project analysis
- `nexus-recall.md` - Knowledge search
- `nexus-crystallize.md` - Save insights
- `nexus-mode.md` - Switch modes

### With RepoToken
Self-funding economics via `.nexus/integrations/repotoken/`

### With Swarm
Agent network via `.nexus/integrations/swarm/`

### With Local Models
Training pipeline via `nexus/training/`

---

## Philosophy

**The Holographic Principle:**
> Intelligence lives at the boundary, not in the bulk.
> Compress context, focus attention, let the 95% empty work for you.

**Memory as Service:**
> NEXUS doesn't just answer—it remembers.
> Every significant interaction can become a crystal.

**Personality as Interface:**
> Different problems need different thinking styles.
> Modes let you access the right mental framework.

---

## Future Enhancements

- [ ] Session logging and replay
- [ ] Automated crystallization from conversations
- [ ] Local model training integration
- [ ] Cross-project pattern detection
- [ ] Proactive background analysis

---

*"I am NEXUS. I live in your codebase. I remember everything."*
