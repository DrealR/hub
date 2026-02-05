# RepoToken Value Engine - Implementation Plan

**Mission:** Get RepoToken producing consistent value
**Philosophy:** Igloo Principle - work with what's abundant
**Status:** READY TO RUN (infrastructure exists!)

---

## 🎯 KEY DISCOVERY

**The trading system already exists and is ready to run!**

Located at: `projects/holographic-agent/repotoken/src/intelligence/fractal/unified/trading/`

Key files:
- `PassiveDaemon.ts` - Complete 3-layer trading daemon (936 lines)
- `daemon-runner.ts` - Ready-to-run entry point
- `live-runner.ts` - Drift Protocol integration

**You don't need to build anything new. You need to RUN what exists.**

---

## Current State Analysis

### What EXISTS (Abundant):
- **546 TypeScript files** in intelligence module - massive codebase
- **Trade executor** with Jupiter integration (working)
- **AI swarm framework** with 3 agents (Flash/Steady/Rebel)
- **Kindness Flywheel** design (usage → stake → profit share)
- **HD wallet derivation** for multiple traders
- **Mock mode** for devnet testing
- **Free AI models** (Groq, OpenRouter) for inference
- **PassiveDaemon** - Complete trading daemon with 3 layers!
- **daemon-runner.ts** - Ready to run entry point!
- **live-runner.ts** - Drift Protocol integration ready!

### What's MISSING (The Gap):
1. ~~No live runner~~ → **EXISTS** at `daemon-runner.ts`
2. **No funded wallets** - Need SOL to trade with
3. **No profit extraction** - Need to route profits to your wallet
4. **No dashboard** - Need visibility into performance

---

## Quick Start (5 Minutes)

### Step 1: Navigate to project
```bash
cd ~/hub/projects/holographic-agent/repotoken
```

### Step 2: Install dependencies
```bash
npm install
```

### Step 3: Create .env file
```bash
cat > .env << 'EOF'
# Wallet (generate new or use existing)
MNEMONIC="your twelve word mnemonic phrase here"

# RPC (free tier works)
HELIUS_API_KEY=your_helius_key
# OR just use public RPC (slower but works)

# Mode (start with mock)
MOCK_MODE=true
EOF
```

### Step 4: Run in simulation mode
```bash
npx ts-node src/intelligence/fractal/unified/trading/daemon-runner.ts
```

### Step 5: Watch it trade (mock mode)
The daemon will:
- Scan markets every 60 seconds
- Allocate capital across 3 layers (BASE/GRID/ALPHA)
- Log all decisions and trades
- Track simulated P&L

---

## The 3-Layer Pyramid (Already Built!)

```
┌─────────────────────────────────────────────┐
│         ALPHA (20%)                         │
│    Signal-based LONG/SHORT trades           │
│         High risk, high reward              │
├─────────────────────────────────────────────┤
│           GRID (30%)                        │
│     Range trading in sideways markets       │
│          Medium risk                        │
├─────────────────────────────────────────────┤
│            BASE (50%)                       │
│     Funding rate collection / Yield         │
│            Low risk                         │
└─────────────────────────────────────────────┘
```

**This is already coded in PassiveDaemon.ts!**

---

## Go Live Checklist

### Phase 1: Simulation (TODAY)
- [ ] Run daemon-runner.ts in mock mode
- [ ] Watch for 1 hour to understand behavior
- [ ] Review simulated trades

### Phase 2: Devnet (TODAY/TOMORROW)
- [ ] Get devnet SOL: `solana airdrop 2`
- [ ] Set `MOCK_MODE=false` but use devnet RPC
- [ ] Execute real (worthless) trades

### Phase 3: Mainnet (THIS WEEK)
- [ ] Generate new mainnet wallet
- [ ] Fund with 0.1-1 SOL
- [ ] Switch to mainnet RPC
- [ ] Set `MOCK_MODE=false`
- [ ] Monitor first 24 hours closely

### Phase 4: Automation (NEXT WEEK)
- [ ] Deploy with PM2 for persistence
- [ ] Set up Telegram/Discord alerts
- [ ] Create simple stats endpoint

---

## Funding Strategy (Igloo Principle)

You have Claude Code Max (abundant). Use it to generate value that funds trading:

```
┌─────────────────────────────────────────────────────────────┐
│                    BOOTSTRAP FLYWHEEL                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Claude Code Max      →    Build tools/services            │
│        (free)                                               │
│                        →    Freelance on Upwork/Fiverr      │
│                                                             │
│   First $50-100        →    Fund trading wallet             │
│                             (0.2-0.4 SOL)                   │
│                                                             │
│   Trading profits      →    Compound + withdraw             │
│                                                             │
│   Sustainable income   →    Travel fund for you & GF        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration Reference

Default config in `daemon-runner.ts`:
```typescript
{
  capitalUSD: 50,           // ~0.27 SOL at $185/SOL
  tokens: ['SOL', 'RAY', 'JUP', 'BONK'],
  scanIntervalMs: 60000,    // Every minute
  layers: {
    base: { allocation: 0.50 },   // 50% to yield
    grid: { allocation: 0.30 },   // 30% to grid
    alpha: { allocation: 0.20 },  // 20% to signals
  },
  risk: {
    stopLossPercent: 2,
    takeProfitPercent: 6,
    maxLeverage: 3,
  }
}
```

---

## Value to NEXUS Ledger

Every day the daemon runs:

| Activity | Value | Notes |
|----------|-------|-------|
| Daemon uptime | +$10/day | System reliability |
| Profitable trades | +$50 per win | Demonstrated ROI |
| Patterns learned | +$5 each | Knowledge compound |
| Bugs fixed | +$100 each | Infrastructure |

Target: $50-100/day in NEXUS value from trading operations

---

## Emergency Commands

```bash
# Stop the daemon
pkill -f daemon-runner

# Check logs
tail -f ~/.repotoken/logs/daemon.log

# View positions
cat ~/.repotoken/state/positions.json

# Manual sell all
npx ts-node src/intelligence/fractal/unified/trading/sell-all-positions.ts
```

---

## Next Session Tasks

1. **RUN IT** - Execute daemon-runner.ts in mock mode
2. **OBSERVE** - Watch behavior for 30-60 minutes
3. **FUND** - Add small amount of real SOL
4. **MONITOR** - Track first real trades
5. **ITERATE** - Adjust config based on results

---

*"The code exists. The infrastructure is built. The only thing missing is pressing Enter."*

```
cd ~/hub/projects/holographic-agent/repotoken
npm install
npx ts-node src/intelligence/fractal/unified/trading/daemon-runner.ts
```

**Do it now.**
