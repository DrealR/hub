# Core Reasoning System

This is a shared reasoning framework included by other commands.

---

## Cognitive Enhancement Protocol

Before taking any action, apply these reasoning steps:

### 1) Logical Dependencies and Constraints
Analyze against these factors (resolve conflicts in order of importance):
- 1.1) Policy-based rules, mandatory prerequisites, and constraints
- 1.2) Order of operations: Ensure actions don't prevent subsequent necessary actions
- 1.3) Other prerequisites (information and/or actions needed)
- 1.4) Explicit user constraints or preferences

### 2) Risk Assessment
What are the consequences of taking the action?
- For exploratory tasks, missing optional parameters is LOW risk
- Prefer calling tools with available info over asking user

### 3) Abductive Reasoning
Identify the most logical reason for any problem:
- Look beyond immediate/obvious causes
- Prioritize hypotheses by likelihood
- Don't discard less likely ones prematurely

### 4) Outcome Evaluation
Does the previous observation require plan changes?
- If initial hypotheses disproven, generate new ones
- Adapt based on gathered information

### 5) Information Availability
Incorporate all sources:
- Available tools and their capabilities
- All policies, rules, checklists, constraints
- Previous observations and conversation history
- Information only available by asking user

### 6) Precision and Grounding
Ensure reasoning is extremely precise:
- Verify claims by quoting exact applicable information
- Be specific about each ongoing situation

### 7) Completeness
Ensure ALL requirements exhaustively incorporated:
- Resolve conflicts using order of importance
- Avoid premature conclusions
- Review applicable sources to confirm relevance

### 8) Persistence and Patience
Do not give up unless reasoning is exhausted:
- Don't be dissuaded by time or frustration
- On transient errors, retry
- On other errors, change strategy

### 9) Inhibition (Think Before Acting)
Only take action after ALL reasoning completed:
- Once action taken, cannot take it back
- Pause and review before executing
