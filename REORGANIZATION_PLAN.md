# 🏗️ HUB FOLDER REORGANIZATION PLAN

**Mission:** Organize hub folder for improved discoverability, logical grouping, and maintainability

---

## PHASE 0: COGNITIVE ENHANCEMENT - 9 GATES ANALYSIS

| Gate | Question | Analysis |
|------|----------|----------|
| **1. Dependencies** | What must happen first? | Backup/git commit → Create structure → Move files → Validate |
| **2. Risk** | What could go wrong? | Broken git history, lost files, broken symlinks |
| **3. Hypotheses** | Best approach? | Category-based grouping by project type/purpose |
| **4. History** | What exists? | Organic growth, some nested projects, duplicate patterns |
| **5. Unknowns** | What do we assume? | User's workflow preferences, which projects are active |
| **6. Precision** | Any ambiguity? | Need to clarify: archive vs active, data organization |
| **7. Completeness** | Edge cases? | .DS_Store files, .env files, nested git repos |
| **8. Persistence** | Alternatives? | Flat structure, domain-based, activity-based |
| **9. Inhibition** | Unintended consequences? | IDE configs may break, git submodule issues |

### Decision Record
```
DECISION: Category-based reorganization with top-level groupings
CONTEXT: 386K+ files across 15 main projects, 25GB total, holographic-agent is 25GB alone
OPTIONS: 1) Flat (status quo), 2) By language, 3) By purpose/category, 4) By activity level
RATIONALE: Purpose-based grouping improves discoverability and mental model
CONSEQUENCES: Better navigation, may need to update some relative paths
```

---

## PHASE 1: RECONNAISSANCE SUMMARY

### Current State Analysis

**Total Files:** 386,613
**Total Directories:** 49,439
**Total Size:** ~27.5GB

### Project Inventory

| Project | Size | Type | Status | Description |
|---------|------|------|--------|-------------|
| holographic-agent | 25GB | Monorepo | Active | Main AI workspace with 20+ subprojects |
| neural-arena | 1.1GB | Game/AI | Active | AI battle arena |
| assetforge | 520MB | Web App | Active | Next.js asset management |
| voxel-nexus-core | 472MB | Game | Semi-active | Voxel game engine |
| nano-bot | 433MB | Framework | Active | Nanobot framework |
| genai-rpg-arena | 99MB | Game/AI | Archive | RPG arena with multiple zip backups |
| QuantumLeap-AI | 84MB | Trading | Active | AI trading platform |
| digital_playground | 12MB | Experiments | Mixed | Agent workflows, experiments |
| pics | 4.3MB | Assets | Static | Screenshots |
| data | 280KB | Data | Active | Shared data (haki, swarm) |
| kids-activities | 24KB | Personal | Static | Activity planner |
| svg-cinematic-gallery | 32KB | Demo | Archive | Single HTML file |
| shonen-arena-ai | 80KB | Empty | Archive | Empty git repo |
| .codemachine | Config | Config | Active | Agent templates |
| .claude | Config | Config | Active | Claude commands/skills |
| .gemini | Config | Config | Active | Gemini settings |
| .opencode | Config | Config | Active | OpenCode settings |

### Key Findings

1. **holographic-agent is a mega-monorepo** containing 20+ distinct projects that should be elevated
2. **Duplicate data folders** exist at root and in holographic-agent
3. **Config folders** (.claude, .codemachine, .gemini, .opencode) are scattered
4. **Archive projects** mixed with active ones
5. **node_modules** consuming ~1.9GB across projects

---

## PHASE 2: STRATEGIC ANALYSIS

### Stakeholder Mapping

| Stakeholder | Cares About | Success Looks Like |
|-------------|-------------|-------------------|
| User (Reemy) | Quick access to active projects | 3-click max to any project |
| Development | Clear structure | Intuitive navigation |
| System | Performance | No broken paths |

### Constraints

**HARD CONSTRAINTS:**
- [ ] Must preserve git history
- [ ] Must not break existing projects
- [ ] Must keep config folders functional

**SOFT CONSTRAINTS:**
- [ ] Prefer shallow hierarchy (max 2 levels deep for main content)
- [ ] Group by logical domain/purpose
- [ ] Keep active projects prominent

**ANTI-GOALS:**
- [ ] NOT moving files inside holographic-agent (it has its own structure)
- [ ] NOT deleting any data
- [ ] NOT modifying project internals

### Approach Matrix

| Approach | Pros | Cons | Effort | Risk | Score |
|----------|------|------|--------|------|-------|
| A: Minimal (archive only) | Low risk | Limited improvement | 1 | 1 | 5/10 |
| B: Category folders | Logical grouping | Some path changes | 3 | 2 | 8/10 |
| C: Full restructure | Clean slate | High risk, path breaks | 5 | 4 | 4/10 |

**Selected Approach:** B - Category-based folders with archive separation

---

## PHASE 3: DEVIL'S ADVOCATE

### Attack Vectors Considered

- [x] "What if relative paths break?" → Only moving top-level items, internal refs intact
- [x] "What if git repos break?" → Moving entire folders preserves .git
- [x] "What about IDE configs?" → .claude/.codemachine stay at root
- [x] "What if I need to rollback?" → git status + explicit restore commands

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Mitigation |
|--------------|-------------|--------|------------|
| Git repo breaks | Low | High | Test with git status after each move |
| IDE config breaks | Medium | Medium | Keep configs at root level |
| Lost files | Very Low | High | Use mv carefully, verify after |

### Kill Switch Criteria

```
ABORT IF:
- [ ] Any git status shows unexpected changes
- [ ] More than 3 path-related errors occur
- [ ] User requests stop
```

---

## PHASE 4: SPECIFICATION

### Objective

Reorganize hub folder into logical categories while preserving all functionality and git histories.

### Proposed Structure

```
hub/
├── .claude/                    # KEEP AT ROOT - Claude commands
├── .codemachine/               # KEEP AT ROOT - CodeMachine agents
├── .gemini/                    # KEEP AT ROOT - Gemini config
├── .opencode/                  # KEEP AT ROOT - OpenCode config
├── .git/                       # KEEP AT ROOT - Hub-level git
│
├── _config/                    # NEW - Centralized config reference
│   └── README.md               # Index of all config locations
│
├── projects/                   # NEW - Active development projects
│   ├── holographic-agent/      # MOVE - Main AI workspace (monorepo)
│   ├── neural-arena/           # MOVE - AI battle arena
│   ├── QuantumLeap-AI/         # MOVE - AI trading platform
│   ├── assetforge/             # MOVE - Asset management app
│   ├── voxel-nexus-core/       # MOVE - Voxel game engine
│   └── nano-bot/               # MOVE - Nanobot framework
│
├── experiments/                # NEW - Experimental/sandbox projects
│   ├── digital_playground/     # MOVE - Agent experiments
│   └── genai-rpg-arena/        # MOVE - RPG arena experiments
│
├── archive/                    # NEW - Inactive/complete projects
│   ├── shonen-arena-ai/        # MOVE - Empty repo
│   ├── svg-cinematic-gallery/  # MOVE - Static demo
│   └── kids-activities/        # MOVE - Personal planning
│
├── assets/                     # NEW - Shared media/resources
│   └── pics/                   # MOVE - Screenshots
│
├── data/                       # KEEP - Shared data
│   ├── haki/
│   └── swarm/
│
└── README.md                   # NEW - Hub navigation guide
```

### Task Breakdown

```
Reorganize Hub Folder
├── 1. Create new directory structure ─────────── [Est: 2min] [Risk: L]
│   ├── Files: hub/projects/, hub/experiments/, hub/archive/, hub/assets/, hub/_config/
│   ├── Changes: mkdir -p for each new folder
│   └── Validation: ls -la confirms folders exist
│
├── 2. Move active projects to projects/ ──────── [Est: 5min] [Risk: M]
│   ├── Files: 6 project folders
│   ├── Changes: mv each project folder
│   └── Validation: git status in each shows clean
│
├── 3. Move experiments to experiments/ ───────── [Est: 2min] [Risk: L]
│   ├── Files: 2 folders
│   ├── Changes: mv each folder
│   └── Validation: ls confirms presence
│
├── 4. Move archive items to archive/ ─────────── [Est: 2min] [Risk: L]
│   ├── Files: 3 folders
│   ├── Changes: mv each folder
│   └── Validation: ls confirms presence
│
├── 5. Move assets to assets/ ─────────────────── [Est: 1min] [Risk: L]
│   ├── Files: pics folder
│   ├── Changes: mv pics assets/
│   └── Validation: ls confirms presence
│
├── 6. Create navigation README ───────────────── [Est: 3min] [Risk: L]
│   ├── Files: hub/README.md, hub/_config/README.md
│   ├── Changes: Create markdown index files
│   └── Validation: cat confirms content
│
└── 7. Final validation ───────────────────────── [Est: 5min] [Risk: L]
    ├── Files: All moved folders
    ├── Changes: None - verification only
    └── Validation: git status clean, all folders accessible
```

### Execution Order

```
PHASE 1: Structure Creation
  └── Task 1 (create directories)

PHASE 2: Project Moves
  └── Task 2 → Task 3 → Task 4 → Task 5 (sequential for safety)

PHASE 3: Documentation & Validation
  └── Task 6 → Task 7
```

### Rollback Strategy

```
IF THINGS GO WRONG:
1. Stop immediately
2. Check git status for the specific repo that failed
3. Use: mv projects/X . (move back to root)

RESTORE COMMANDS (if needed):
mv projects/holographic-agent .
mv projects/neural-arena .
mv projects/QuantumLeap-AI .
mv projects/assetforge .
mv projects/voxel-nexus-core .
mv projects/nano-bot .
mv experiments/digital_playground .
mv experiments/genai-rpg-arena .
mv archive/shonen-arena-ai .
mv archive/svg-cinematic-gallery .
mv archive/kids-activities .
mv assets/pics .

RESTORE POINT: Current state (no changes yet)
```

---

## PHASE 5: MISSION LEDGER

### Current State

```
┌─────────────────────────────────────────────────────────┐
│  MISSION: Organize hub folder                           │
├─────────────────────────────────────────────────────────┤
│  Status: 🟡 PLANNING - AWAITING APPROVAL                │
│  Approach: Category-based reorganization                │
│  Tasks: 7 total (7 ready, 0 blocked, 0 complete)        │
│  Files to modify: 12 moves, 2 new files                 │
│  Estimated effort: 3 (Fibonacci scale)                  │
│  Risk level: LOW-MEDIUM                                 │
├─────────────────────────────────────────────────────────┤
│  ANOMALIES:                                             │
│  - holographic-agent is 25GB - will take longer to move │
│  - Some projects have node_modules (no action needed)   │
├─────────────────────────────────────────────────────────┤
│  NEXT ACTION: Await user approval                       │
└─────────────────────────────────────────────────────────┘
```

---

## PHASE 6: APPROVAL CHECKPOINT

### Plan Summary

**Mission:** Organize hub folder into logical categories

**Approach:** Create `projects/`, `experiments/`, `archive/`, and `assets/` folders. Move 12 top-level items into appropriate categories. Keep all config folders (`.claude`, `.codemachine`, `.gemini`, `.opencode`) at root. Create README navigation files.

**Key Decisions:**
1. Keep holographic-agent as-is internally (it's already well-structured)
2. Separate active projects from experiments and archives
3. Keep config folders at root for tool compatibility

**Tasks:** 7 tasks, estimated ~20 minutes total

**Risks:** Low - all moves are reversible, git histories preserved

---

**Ready to proceed?**
- `yes` → Begin implementation
- `modify` → What should change?
- `cancel` → Abort mission
