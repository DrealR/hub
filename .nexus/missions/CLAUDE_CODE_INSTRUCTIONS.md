# Instructions for Claude Code: Deploy RepoToken Trading Daemon

Copy everything below this line and paste it into Claude Code:

---

## TASK: Start the RepoToken Trading Daemon

I want you to start the RepoToken passive trading daemon and keep it running. Here's what to do:

### Step 1: Navigate to the project
```bash
cd ~/hub/projects/holographic-agent/repotoken
```

### Step 2: Install dependencies (if needed)
```bash
npm install --legacy-peer-deps
```

### Step 3: Run the daemon in SIMULATION mode first
```bash
MNEMONIC="van more thumb arch around cotton cluster success pulp ankle nose drum trend earth thought sudden breeze collect analyst room throw fall long more" npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```

### What I want you to do:
1. Start the daemon
2. Let it run for at least 5-10 minutes so it can collect market data
3. Watch the output and tell me:
   - Are the scans working? (Should show SOL, JUP, RAY, BONK prices)
   - Is it detecting trading signals?
   - Any errors?

### After simulation works, go LIVE:
```bash
MNEMONIC="van more thumb arch around cotton cluster success pulp ankle nose drum trend earth thought sudden breeze collect analyst room throw fall long more" MOCK_MODE=false npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts
```

### To keep it running permanently with PM2:
```bash
npm install -g pm2
pm2 start "MNEMONIC='van more thumb arch around cotton cluster success pulp ankle nose drum trend earth thought sudden breeze collect analyst room throw fall long more' npx ts-node --transpile-only src/intelligence/fractal/unified/trading/daemon-runner.ts" --name repotoken-daemon
pm2 save
pm2 logs repotoken-daemon
```

### Important notes:
- The daemon uses a 3-layer strategy: BASE (50% yield farming), GRID (30% range trading), ALPHA (20% signal trading)
- It scans every 60 seconds and ticks every 10 seconds
- First few scans may show "Insufficient data" - this is normal, wait for it to collect 168+ candles
- The .env file already has all API keys (HELIUS, GROQ, OPENROUTER)

### If you need to check wallet balance:
```bash
# Using the mnemonic to derive the wallet address
npx ts-node --transpile-only -e "
const bip39 = require('bip39');
const { derivePath } = require('ed25519-hd-key');
const { Keypair } = require('@solana/web3.js');

const mnemonic = 'van more thumb arch around cotton cluster success pulp ankle nose drum trend earth thought sudden breeze collect analyst room throw fall long more';
const seed = bip39.mnemonicToSeedSync(mnemonic);
const derivedSeed = derivePath(\"m/44'/501'/0'/0'\", seed.toString('hex')).key;
const keypair = Keypair.fromSeed(derivedSeed);
console.log('Wallet address:', keypair.publicKey.toBase58());
"
```

Then check balance at: https://solscan.io/account/YOUR_ADDRESS

---

END OF INSTRUCTIONS
