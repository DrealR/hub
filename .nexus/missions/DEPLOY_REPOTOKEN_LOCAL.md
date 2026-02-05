# Deploy RepoToken Trading Daemon - Local Setup

**Time to complete:** 5-10 minutes
**Requirements:** Node.js 20+, npm, terminal

---

## Quick Start (Copy-Paste Ready)

### 1. Open Terminal and navigate to RepoToken
```bash
cd ~/hub/projects/holographic-agent/repotoken
```

### 2. Install dependencies
```bash
npm install --legacy-peer-deps
```

### 3. Verify your .env file exists
```bash
cat .env | grep -E "MNEMONIC|HELIUS"
```

You should see your mnemonic and API keys.

### 4. Start the daemon in SIMULATION mode
```bash
npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```

---

## What You'll See

```
╔════════════════════════════════════════════════════════════════════════╗
║   PASSIVE DAEMON                                                        ║
║   24/7 Autonomous Profit Generation System                              ║
╚════════════════════════════════════════════════════════════════════════╝

Mode:            🧪 SIMULATION
Starting Capital: $50.00 (~0.27 SOL)

Layer Allocation:
  💎 BASE:  50% ($25.00)
  📊 GRID:  30% ($15.00)
  🎯 ALPHA: 20% ($10.00)

[SCAN] #1 at 11:30:00 PM
[SCAN] SOL: $189.45 | sigma=1.23
[SCAN] JUP: $0.89 | sigma=0.87
...
```

---

## Go Live Checklist

### Phase 1: Simulation (Run for 1-24 hours)
```bash
# Default: simulation mode
npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```
Watch the logs. Understand the behavior. See simulated trades.

### Phase 2: Devnet (Free, real transactions)
```bash
# Get devnet SOL
solana config set --url devnet
solana airdrop 2

# Run with devnet
MOCK_MODE=false SOLANA_RPC_URL=https://api.devnet.solana.com npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```

### Phase 3: Mainnet (Real money)
```bash
# Fund your wallet first! (0.1-1 SOL to start)
# Then run with mainnet
MOCK_MODE=false npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```

---

## Keep It Running 24/7

### Option A: PM2 (Recommended)
```bash
# Install PM2
npm install -g pm2

# Start daemon
pm2 start "npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts" --name repotoken

# Monitor
pm2 logs repotoken
pm2 status

# Auto-restart on reboot
pm2 startup
pm2 save
```

### Option B: Screen/Tmux
```bash
# Start screen session
screen -S repotoken

# Run daemon
MNEMONIC="your mnemonic" npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts

# Detach: Ctrl+A, then D
# Reattach: screen -r repotoken
```

### Option C: Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/repotoken.service
```

```ini
[Unit]
Description=RepoToken Trading Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/hub/projects/holographic-agent/repotoken
Environment=MNEMONIC="your mnemonic here"
ExecStart=/usr/bin/npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable repotoken
sudo systemctl start repotoken
sudo systemctl status repotoken

# View logs
journalctl -u repotoken -f
```

---

## Configuration Tweaks

Edit `daemon-runner.ts` or pass environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MOCK_MODE` | `true` | Set to `false` for live trading |
| `MNEMONIC` | (required) | Your wallet mnemonic |
| `DURATION` | `0` (infinite) | Hours to run, 0 = forever |
| `TARGET_CAPITAL` | `100` | Target USD value |

### Adjust capital allocation:
```typescript
// In daemon-runner.ts DEFAULT_CONFIG
capitalUSD: 50,  // Change starting capital
layers: {
  base: { allocation: 0.50 },  // 50% to yield
  grid: { allocation: 0.30 },  // 30% to grid
  alpha: { allocation: 0.20 }, // 20% to signals
}
```

---

## Monitoring

### Check status via NEXUS command:
```bash
# In Claude Code
/project:nexus-value status
```

### Manual checks:
```bash
# View PM2 logs
pm2 logs repotoken --lines 100

# Check wallet balance
solana balance YOUR_WALLET_ADDRESS

# View positions (if state file exists)
cat ~/.repotoken/state/positions.json 2>/dev/null || echo "No positions file yet"
```

---

## Troubleshooting

### "Insufficient data" on all tokens
Normal on first few scans. The daemon needs to collect 168+ candles (7 days of hourly data) before trading. Just wait ~5-10 minutes for the API to warm up.

### API rate limits
DexScreener and GeckoTerminal have rate limits. The daemon has built-in delays between requests.

### Wallet not funded
```bash
# Check balance
solana balance $(solana address)

# If empty on devnet, airdrop
solana airdrop 2
```

### TypeScript errors on build
Use `--transpile-only` to skip type checking:
```bash
npx ts-node --transpile-only src/...
```

---

## Security Notes

- **Never share your MNEMONIC**
- Store .env with restricted permissions: `chmod 600 .env`
- Start with small amounts (0.1 SOL) until you trust the system
- Monitor the first 24-48 hours closely

---

## Next Steps After Deployment

1. **Run in simulation for 24 hours** - understand the patterns
2. **Fund with 0.1-0.5 SOL** - small initial capital
3. **Go live, monitor closely** - watch first few trades
4. **Adjust risk parameters** - tune stop loss, take profit
5. **Scale up** - increase capital as confidence grows

---

*"The daemon is built. The infrastructure is ready. Press Enter on YOUR machine."*
