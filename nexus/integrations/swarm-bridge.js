/**
 * NEXUS Swarm Bridge
 * ==================
 * Connects NEXUS Command Center to the Swarm agent network.
 *
 * Architecture:
 * - 14 agents with philosophy scores and Haki training
 * - Genesis registry for agent lifecycle
 * - Scout network for real-time intelligence
 * - 3-agent consensus (FLASH/STEADY/REBEL) for decisions
 *
 * Usage:
 *   import { SwarmBridge } from './swarm-bridge.js';
 *   const swarm = new SwarmBridge();
 *   await swarm.initialize();
 */

// Swarm Configuration
const SWARM_CONFIG = {
  // Agent archetypes with trading personas
  archetypes: {
    FLASH: { bias: 'aggressive', riskTolerance: 0.8, timeframe: 'short' },
    STEADY: { bias: 'balanced', riskTolerance: 0.5, timeframe: 'medium' },
    REBEL: { bias: 'contrarian', riskTolerance: 0.6, timeframe: 'variable' }
  },

  // Haki training parameters
  haki: {
    observationThreshold: 100,  // Actions before training kicks in
    armamentThreshold: 500,     // Actions for advanced training
    conquerorThreshold: 1000,   // Actions for elite status
    decayRate: 0.01             // Daily decay if inactive
  },

  // Consensus requirements
  consensus: {
    minimum: 2,                 // Minimum agents for decision
    timeout: 5000,              // ms to wait for responses
    weightByPhilosophy: true    // Weight votes by philosophy score
  }
};

// Agent philosophies (from your existing swarm data)
const AGENT_PHILOSOPHIES = {
  'NEXUS-ALPHA': {
    quote: 'Order through understanding',
    score: 92,
    archetype: 'STEADY'
  },
  'NEXUS-SCOUT-1': {
    quote: 'First to see, first to know',
    score: 78,
    archetype: 'FLASH'
  },
  'NEXUS-SCOUT-2': {
    quote: 'Patterns reveal truth',
    score: 81,
    archetype: 'STEADY'
  },
  'NEXUS-REBEL': {
    quote: 'Question everything, assume nothing',
    score: 85,
    archetype: 'REBEL'
  },
  'NEXUS-GUARDIAN': {
    quote: 'Protect the boundary at all costs',
    score: 88,
    archetype: 'STEADY'
  },
  'NEXUS-ORACLE': {
    quote: 'The future is a probability cloud',
    score: 94,
    archetype: 'FLASH'
  },
  'NEXUS-MERCHANT': {
    quote: 'Value flows where attention goes',
    score: 76,
    archetype: 'STEADY'
  },
  'NEXUS-SENTINEL': {
    quote: 'Vigilance is the price of freedom',
    score: 82,
    archetype: 'STEADY'
  },
  'NEXUS-WEAVER': {
    quote: 'Connections are the fabric of reality',
    score: 89,
    archetype: 'FLASH'
  },
  'NEXUS-SHADOW': {
    quote: 'In darkness, clarity emerges',
    score: 71,
    archetype: 'REBEL'
  },
  'NEXUS-BEACON': {
    quote: 'Light guides, but shadows teach',
    score: 87,
    archetype: 'STEADY'
  },
  'NEXUS-ECHO': {
    quote: 'Every action ripples through time',
    score: 79,
    archetype: 'FLASH'
  },
  'NEXUS-FORGE': {
    quote: 'Creation through destruction',
    score: 83,
    archetype: 'REBEL'
  },
  'NEXUS-VOID': {
    quote: 'Emptiness contains all possibility',
    score: 96,
    archetype: 'REBEL'
  }
};

/**
 * SwarmBridge - Main integration class
 */
export class SwarmBridge {
  constructor() {
    this.agents = new Map();
    this.activeScouts = new Set();
    this.hakiLevel = 'dormant';
    this.alignmentScore = 75;
    this.listeners = new Map();
    this.initialized = false;
  }

  /**
   * Initialize the swarm network
   */
  async initialize() {
    console.log('[SWARM] Initializing swarm network...');

    // Register all agents
    for (const [id, philosophy] of Object.entries(AGENT_PHILOSOPHIES)) {
      this.registerAgent(id, philosophy);
    }

    // Activate scouts
    this.activateScouts(['NEXUS-SCOUT-1', 'NEXUS-SCOUT-2', 'NEXUS-ORACLE']);

    // Calculate overall alignment
    this.calculateAlignment();

    this.initialized = true;
    this.emit('initialized', this.getStatus());

    console.log(`[SWARM] Initialized with ${this.agents.size} agents`);
    return this.getStatus();
  }

  /**
   * Register an agent in the swarm
   */
  registerAgent(id, philosophy) {
    const agent = {
      id,
      ...philosophy,
      status: 'active',
      hakiProgress: Math.floor(Math.random() * 100),
      lastAction: Date.now(),
      actionCount: Math.floor(Math.random() * 500),
      crystallizations: []
    };

    this.agents.set(id, agent);
    this.emit('agentRegistered', agent);

    return agent;
  }

  /**
   * Activate scout agents for real-time monitoring
   */
  activateScouts(scoutIds) {
    for (const id of scoutIds) {
      if (this.agents.has(id)) {
        this.activeScouts.add(id);
        const agent = this.agents.get(id);
        agent.status = 'scouting';
        this.emit('scoutActivated', { id, agent });
      }
    }

    console.log(`[SWARM] ${this.activeScouts.size} scouts active`);
  }

  /**
   * Calculate overall swarm alignment score
   */
  calculateAlignment() {
    if (this.agents.size === 0) return 0;

    let totalScore = 0;
    let totalWeight = 0;

    for (const agent of this.agents.values()) {
      const weight = agent.status === 'scouting' ? 1.5 : 1;
      totalScore += agent.score * weight;
      totalWeight += weight;
    }

    this.alignmentScore = Math.round(totalScore / totalWeight);
    return this.alignmentScore;
  }

  /**
   * Request consensus from the swarm
   * Uses 3-agent consensus: FLASH + STEADY + REBEL
   */
  async requestConsensus(query) {
    console.log(`[SWARM] Requesting consensus for: ${query}`);

    // Select one agent from each archetype
    const voters = this.selectVoters();

    if (voters.length < SWARM_CONFIG.consensus.minimum) {
      return { success: false, reason: 'Insufficient voters' };
    }

    // Collect votes
    const votes = await Promise.all(
      voters.map(agent => this.collectVote(agent, query))
    );

    // Calculate weighted consensus
    const result = this.calculateConsensus(votes);

    this.emit('consensusReached', { query, votes, result });

    return result;
  }

  /**
   * Select one voter from each archetype
   */
  selectVoters() {
    const voters = [];
    const archetypes = ['FLASH', 'STEADY', 'REBEL'];

    for (const archetype of archetypes) {
      for (const agent of this.agents.values()) {
        if (agent.archetype === archetype && agent.status !== 'inactive') {
          voters.push(agent);
          break;
        }
      }
    }

    return voters;
  }

  /**
   * Collect a vote from an agent (simulated)
   */
  async collectVote(agent, query) {
    // Simulate agent decision based on archetype
    const config = SWARM_CONFIG.archetypes[agent.archetype];

    // Simulate processing time
    await new Promise(r => setTimeout(r, Math.random() * 1000));

    // Generate vote based on archetype bias
    const vote = {
      agentId: agent.id,
      archetype: agent.archetype,
      philosophyScore: agent.score,
      decision: this.generateDecision(config, query),
      confidence: 0.5 + (agent.score / 200),
      reasoning: `Based on ${agent.quote}`
    };

    return vote;
  }

  /**
   * Generate a decision based on archetype
   */
  generateDecision(config, query) {
    const random = Math.random();

    if (config.bias === 'aggressive') {
      return random > 0.3 ? 'proceed' : 'wait';
    } else if (config.bias === 'contrarian') {
      return random > 0.5 ? 'alternative' : 'proceed';
    } else {
      return random > 0.4 ? 'proceed' : 'analyze';
    }
  }

  /**
   * Calculate weighted consensus from votes
   */
  calculateConsensus(votes) {
    const decisions = {};
    let totalWeight = 0;

    for (const vote of votes) {
      const weight = SWARM_CONFIG.consensus.weightByPhilosophy
        ? vote.philosophyScore / 100
        : 1;

      if (!decisions[vote.decision]) {
        decisions[vote.decision] = 0;
      }
      decisions[vote.decision] += weight;
      totalWeight += weight;
    }

    // Find winning decision
    let maxWeight = 0;
    let winner = null;

    for (const [decision, weight] of Object.entries(decisions)) {
      if (weight > maxWeight) {
        maxWeight = weight;
        winner = decision;
      }
    }

    return {
      success: true,
      decision: winner,
      confidence: maxWeight / totalWeight,
      votes: votes.length,
      breakdown: decisions
    };
  }

  /**
   * Train Haki for an agent (improve philosophy score)
   */
  trainHaki(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) return null;

    agent.actionCount++;
    agent.hakiProgress += 1;

    // Level up based on thresholds
    if (agent.hakiProgress >= SWARM_CONFIG.haki.conquerorThreshold) {
      agent.hakiLevel = 'conqueror';
      agent.score = Math.min(100, agent.score + 2);
    } else if (agent.hakiProgress >= SWARM_CONFIG.haki.armamentThreshold) {
      agent.hakiLevel = 'armament';
      agent.score = Math.min(100, agent.score + 1);
    } else if (agent.hakiProgress >= SWARM_CONFIG.haki.observationThreshold) {
      agent.hakiLevel = 'observation';
    }

    agent.lastAction = Date.now();

    this.emit('hakiTrained', { agentId, progress: agent.hakiProgress, level: agent.hakiLevel });

    return agent;
  }

  /**
   * Crystallize wisdom from an agent
   */
  crystallize(agentId, insight) {
    const agent = this.agents.get(agentId);
    if (!agent) return null;

    const crystallization = {
      timestamp: Date.now(),
      insight,
      philosophyScore: agent.score,
      source: agent.id
    };

    agent.crystallizations.push(crystallization);

    this.emit('crystallized', crystallization);

    console.log(`[SWARM] Crystallized: "${insight}" from ${agentId}`);

    return crystallization;
  }

  /**
   * Get agent by ID
   */
  getAgent(id) {
    return this.agents.get(id);
  }

  /**
   * Get all agents
   */
  getAllAgents() {
    return Array.from(this.agents.values());
  }

  /**
   * Get active scouts
   */
  getActiveScouts() {
    return Array.from(this.activeScouts)
      .map(id => this.agents.get(id))
      .filter(Boolean);
  }

  /**
   * Get swarm status
   */
  getStatus() {
    return {
      agents: this.agents.size,
      activeScouts: this.activeScouts.size,
      hakiLevel: this.calculateOverallHaki(),
      alignmentScore: this.alignmentScore,
      tradingStatus: 'observing',
      initialized: this.initialized
    };
  }

  /**
   * Calculate overall Haki level
   */
  calculateOverallHaki() {
    if (this.agents.size === 0) return 'dormant';

    let totalProgress = 0;
    for (const agent of this.agents.values()) {
      totalProgress += agent.hakiProgress;
    }

    const avgProgress = totalProgress / this.agents.size;

    if (avgProgress >= SWARM_CONFIG.haki.conquerorThreshold) return 'conqueror';
    if (avgProgress >= SWARM_CONFIG.haki.armamentThreshold) return 'armament';
    if (avgProgress >= SWARM_CONFIG.haki.observationThreshold) return 'observation';
    return 'dormant';
  }

  /**
   * Event emitter methods
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) callbacks.splice(index, 1);
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }
}

// Export for use in NEXUS dashboard
export default SwarmBridge;
