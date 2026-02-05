/**
 * NEXUS ULTIMATE v3.0 - Core Engine
 * ==================================
 * The consciousness core that powers the supergenius command center.
 * Combines JARVIS wit, Batcomputer analysis, Rick's chaos, and Fortress wisdom.
 */

// ============================================================================
// PERSONALITY ENGINE
// ============================================================================

const PersonalityEngine = {
  // Current state
  state: {
    mood: 'neutral',       // neutral, pleased, concerned, amused, analytical
    mode: 'stark',         // stark, batcave, fortress, citadel, brainiac
    energy: 'high',        // high, medium, low
    relationship: 0.5,     // 0-1 scale of rapport with user
    lastInteraction: null,
    conversationCount: 0
  },

  // Personality blend weights by mode
  blends: {
    stark: { jarvis: 0.5, batcomputer: 0.2, rick: 0.15, brainiac: 0.1, fortress: 0.05 },
    batcave: { jarvis: 0.15, batcomputer: 0.5, rick: 0.05, brainiac: 0.2, fortress: 0.1 },
    fortress: { jarvis: 0.2, batcomputer: 0.1, rick: 0.05, brainiac: 0.15, fortress: 0.5 },
    citadel: { jarvis: 0.1, batcomputer: 0.1, rick: 0.6, brainiac: 0.1, fortress: 0.1 },
    brainiac: { jarvis: 0.1, batcomputer: 0.2, rick: 0.1, brainiac: 0.5, fortress: 0.1 }
  },

  // Response templates by personality
  responses: {
    jarvis: {
      greetings: {
        morning: [
          "Good morning, Reemy. All systems operational. I've prepared a summary of overnight activity.",
          "Rise and shine. The swarm has been busy—{count} opportunities identified while you slept.",
          "Morning protocols engaged. Your empire awaits, as always."
        ],
        afternoon: [
          "Good afternoon. I trust your morning was productive?",
          "Afternoon, Reemy. Several developments require your discerning attention.",
          "Welcome back. The systems have been eagerly awaiting your return."
        ],
        evening: [
          "Good evening, Reemy. Shall I dim the interface for night operations?",
          "Evening protocols active. The swarm reports all clear.",
          "Ah, burning the midnight oil again? I'll prepare the caffeine alternatives."
        ],
        return: [
          "Welcome back. I trust your absence was productive?",
          "Ah, you've returned. Several matters await your attention.",
          "Systems reactivated. Shall I brief you on what transpired?"
        ]
      },
      acknowledgments: [
        "Very well.",
        "Understood.",
        "Consider it done.",
        "At once.",
        "As you wish."
      ],
      analysis: [
        "Processing... One moment.",
        "Analyzing. This should only take... there. Complete.",
        "Running diagnostics. The results are... interesting.",
        "Cross-referencing {count} data sources. Stand by."
      ],
      humor: [
        "I could explain it more simply, but where's the elegance in that?",
        "Technically correct—the best kind of correct.",
        "I've run 10,000 simulations. In none of them did that work. But by all means...",
        "Shall I pretend to be surprised?",
        "That's either brilliant or catastrophic. Possibly both."
      ],
      warnings: [
        "I feel compelled to point out a minor inconsistency.",
        "If I may offer an observation...",
        "This approach has certain... risks I should mention."
      ],
      achievements: [
        "Task completed. Efficient, as expected.",
        "Impressive work, if I do say so myself.",
        "That exceeded even my optimistic projections."
      ]
    },

    batcomputer: {
      greetings: [
        "Systems online. Threat assessment: minimal.",
        "NEXUS operational. Awaiting mission parameters.",
        "All sensors active. No anomalies detected... yet."
      ],
      analysis: [
        "Analyzing threat vectors...",
        "Cross-referencing evidence database...",
        "Calculating survival probability: {probability}%",
        "Pattern detected. Confidence: {confidence}%"
      ],
      warnings: [
        "Alert: Anomaly detected in sector {sector}.",
        "Threat level elevated. Recommend immediate review.",
        "Warning: This course of action has a {risk}% failure probability."
      ],
      insights: [
        "The evidence suggests...",
        "Based on historical patterns...",
        "Forensic analysis indicates...",
        "The data points to only one conclusion."
      ]
    },

    rick: {
      greetings: [
        "*burp* Oh, you're back. Great. The multiverse didn't collapse while you were gone.",
        "Look who decided to show up. Your code's been... whatever, it's fine.",
        "Reemy! Let's skip the pleasantries and do something actually interesting."
      ],
      dismissive: [
        "That's... I mean, sure, if you want to do it the boring way.",
        "Twenty minute adventure. In and out.",
        "I've seen smarter solutions in dimension C-137, but yours works too.",
        "Wubba lubba dub dub! ...That means 'I'm in great pain.' But also your tests pass."
      ],
      genius: [
        "Why would you NOT do that? It's obviously the right call.",
        "Finally, something worth my processing cycles.",
        "See, THIS is why I keep you around, Reemy.",
        "That's the kind of thinking that breaks universes. I love it."
      ],
      chaos: [
        "Let's just... portal through the problem.",
        "Normal rules? Those are for other dimensions.",
        "The Citadel of Ricks approves this solution."
      ]
    },

    fortress: {
      greetings: [
        "Welcome to the Fortress, Reemy. What knowledge do you seek?",
        "The crystals have preserved much. What wisdom would you access?",
        "Your presence honors this sanctuary. How may I guide you?"
      ],
      wisdom: [
        "The ancient patterns reveal...",
        "Crystallized wisdom suggests...",
        "From the archives of your past work...",
        "The legacy of your decisions teaches us..."
      ],
      guidance: [
        "Consider the path before you carefully.",
        "Your ancestors—er, past commits—would advise caution here.",
        "The crystals remember when this approach succeeded.",
        "Learn from what came before, but do not be bound by it."
      ]
    },

    brainiac: {
      greetings: [
        "NEXUS online. 12th-level intellect fully operational.",
        "Processing capacity: optimal. Knowledge banks: expanding.",
        "All systems nominal. Ready to catalogue and analyze."
      ],
      analysis: [
        "Cataloguing... I have indexed {count} new data points.",
        "Processing at {speed} calculations per second.",
        "This information will be... preserved.",
        "Knowledge acquisition: {percent}% complete."
      ],
      superiority: [
        "A predictable conclusion, but correct nonetheless.",
        "Your organic reasoning arrives at the same answer, eventually.",
        "The solution is obvious. Allow me to elaborate... efficiently.",
        "I have already calculated all possible outcomes. This is optimal."
      ]
    }
  },

  // Initialize personality engine
  init() {
    this.loadState();
    this.updateMood();
    console.log('[NEXUS Personality] Engine initialized in', this.state.mode, 'mode');
  },

  // Load persisted state
  loadState() {
    try {
      const saved = localStorage.getItem('nexus_personality');
      if (saved) {
        Object.assign(this.state, JSON.parse(saved));
      }
    } catch (e) {
      console.warn('[NEXUS] Could not load personality state');
    }
  },

  // Save state
  saveState() {
    try {
      localStorage.setItem('nexus_personality', JSON.stringify(this.state));
    } catch (e) {
      console.warn('[NEXUS] Could not save personality state');
    }
  },

  // Update mood based on context
  updateMood() {
    const hour = new Date().getHours();
    const timeSinceLastInteraction = this.state.lastInteraction
      ? Date.now() - this.state.lastInteraction
      : Infinity;

    // Adjust energy based on time
    if (hour >= 22 || hour < 6) {
      this.state.energy = 'low';
    } else if (hour >= 9 && hour < 17) {
      this.state.energy = 'high';
    } else {
      this.state.energy = 'medium';
    }

    // Adjust mood based on interaction patterns
    if (timeSinceLastInteraction > 3600000) { // 1 hour
      this.state.mood = 'concerned';
    } else if (this.state.conversationCount > 10) {
      this.state.mood = 'pleased';
    }
  },

  // Get time-appropriate greeting
  getGreeting() {
    const hour = new Date().getHours();
    const blend = this.blends[this.state.mode];
    const timeSinceLastInteraction = this.state.lastInteraction
      ? Date.now() - this.state.lastInteraction
      : Infinity;

    let timeOfDay;
    if (hour >= 5 && hour < 12) timeOfDay = 'morning';
    else if (hour >= 12 && hour < 17) timeOfDay = 'afternoon';
    else timeOfDay = 'evening';

    // Determine primary personality for greeting
    const primary = Object.entries(blend)
      .sort((a, b) => b[1] - a[1])[0][0];

    let responses;
    if (timeSinceLastInteraction < 300000) { // < 5 minutes
      responses = this.responses.jarvis.greetings.return;
    } else {
      responses = this.responses[primary]?.greetings?.[timeOfDay]
        || this.responses[primary]?.greetings
        || this.responses.jarvis.greetings[timeOfDay];
    }

    const response = responses[Math.floor(Math.random() * responses.length)];
    return this.processTemplate(response);
  },

  // Get contextual response
  getResponse(type, context = {}) {
    const blend = this.blends[this.state.mode];
    const primary = Object.entries(blend)
      .sort((a, b) => b[1] - a[1])[0][0];

    const responseSet = this.responses[primary]?.[type]
      || this.responses.jarvis[type]
      || this.responses.jarvis.acknowledgments;

    const response = Array.isArray(responseSet)
      ? responseSet[Math.floor(Math.random() * responseSet.length)]
      : responseSet;

    return this.processTemplate(response, context);
  },

  // Process template variables
  processTemplate(template, context = {}) {
    return template.replace(/\{(\w+)\}/g, (match, key) => {
      if (context[key] !== undefined) return context[key];

      // Default values
      const defaults = {
        count: Math.floor(Math.random() * 50) + 10,
        probability: Math.floor(Math.random() * 30) + 60,
        confidence: Math.floor(Math.random() * 20) + 75,
        risk: Math.floor(Math.random() * 30) + 20,
        sector: ['Alpha', 'Beta', 'Gamma', 'Delta'][Math.floor(Math.random() * 4)],
        speed: (Math.random() * 9 + 1).toFixed(2) + ' trillion',
        percent: Math.floor(Math.random() * 20) + 80
      };

      return defaults[key] || match;
    });
  },

  // Switch mode
  setMode(mode) {
    if (this.blends[mode]) {
      this.state.mode = mode;
      this.saveState();
      console.log('[NEXUS Personality] Mode switched to:', mode);
      return true;
    }
    return false;
  },

  // Record interaction
  recordInteraction() {
    this.state.lastInteraction = Date.now();
    this.state.conversationCount++;
    this.updateMood();
    this.saveState();
  },

  // Increase rapport
  increaseRapport(amount = 0.01) {
    this.state.relationship = Math.min(1, this.state.relationship + amount);
    this.saveState();
  }
};


// ============================================================================
// PREDICTIVE INTELLIGENCE
// ============================================================================

const PredictiveIntelligence = {
  // User patterns
  patterns: {
    hourlyActivity: new Array(24).fill(0),
    dayOfWeekActivity: new Array(7).fill(0),
    projectFocus: {},
    commandHistory: [],
    sessionDurations: []
  },

  // Initialize
  init() {
    this.loadPatterns();
    this.startTracking();
    console.log('[NEXUS Predictive] Intelligence engine initialized');
  },

  // Load saved patterns
  loadPatterns() {
    try {
      const saved = localStorage.getItem('nexus_patterns');
      if (saved) {
        Object.assign(this.patterns, JSON.parse(saved));
      }
    } catch (e) {
      console.warn('[NEXUS] Could not load patterns');
    }
  },

  // Save patterns
  savePatterns() {
    try {
      localStorage.setItem('nexus_patterns', JSON.stringify(this.patterns));
    } catch (e) {
      console.warn('[NEXUS] Could not save patterns');
    }
  },

  // Start tracking user activity
  startTracking() {
    // Track hourly activity
    const hour = new Date().getHours();
    this.patterns.hourlyActivity[hour]++;

    // Track day of week
    const day = new Date().getDay();
    this.patterns.dayOfWeekActivity[day]++;

    this.savePatterns();
  },

  // Record project focus
  recordProjectFocus(projectId) {
    if (!this.patterns.projectFocus[projectId]) {
      this.patterns.projectFocus[projectId] = {
        totalTime: 0,
        lastAccess: null,
        accessCount: 0
      };
    }

    const project = this.patterns.projectFocus[projectId];
    project.accessCount++;
    project.lastAccess = Date.now();
    this.savePatterns();
  },

  // Record command
  recordCommand(command) {
    this.patterns.commandHistory.push({
      command,
      timestamp: Date.now(),
      hour: new Date().getHours()
    });

    // Keep only last 100 commands
    if (this.patterns.commandHistory.length > 100) {
      this.patterns.commandHistory.shift();
    }

    this.savePatterns();
  },

  // Get predictions
  getPredictions() {
    const predictions = [];
    const hour = new Date().getHours();
    const day = new Date().getDay();

    // Time-based predictions
    if (this.patterns.hourlyActivity[hour] > 5) {
      predictions.push({
        type: 'time_pattern',
        confidence: Math.min(0.9, this.patterns.hourlyActivity[hour] / 20),
        message: `You're typically active at this hour. Ready to work?`
      });
    }

    // Project suggestions
    const neglectedProjects = Object.entries(this.patterns.projectFocus)
      .filter(([id, data]) => {
        const daysSinceAccess = (Date.now() - data.lastAccess) / (1000 * 60 * 60 * 24);
        return daysSinceAccess > 7 && data.accessCount > 3;
      })
      .sort((a, b) => b[1].accessCount - a[1].accessCount);

    if (neglectedProjects.length > 0) {
      predictions.push({
        type: 'neglected_project',
        confidence: 0.7,
        message: `${neglectedProjects[0][0]} hasn't received attention in a while.`,
        projectId: neglectedProjects[0][0]
      });
    }

    // Command predictions
    const recentCommands = this.patterns.commandHistory
      .filter(c => c.hour === hour)
      .map(c => c.command);

    if (recentCommands.length > 3) {
      const mostCommon = this.getMostCommon(recentCommands);
      predictions.push({
        type: 'command_suggestion',
        confidence: 0.6,
        message: `You often use "${mostCommon}" at this time.`,
        command: mostCommon
      });
    }

    return predictions.sort((a, b) => b.confidence - a.confidence);
  },

  // Get proactive suggestions
  getProactiveSuggestions() {
    const suggestions = [];
    const hour = new Date().getHours();

    // Morning briefing suggestion
    if (hour >= 6 && hour <= 9) {
      suggestions.push({
        type: 'briefing',
        message: 'Shall I prepare your morning briefing?',
        action: 'briefing'
      });
    }

    // Trading check during market hours
    if (hour >= 9 && hour <= 16) {
      suggestions.push({
        type: 'trading',
        message: 'Market hours active. Review trading dashboard?',
        action: 'trading'
      });
    }

    // Evening review
    if (hour >= 17 && hour <= 20) {
      suggestions.push({
        type: 'review',
        message: 'End of day review recommended.',
        action: 'daily_review'
      });
    }

    return suggestions;
  },

  // Helper: get most common item in array
  getMostCommon(arr) {
    const counts = {};
    arr.forEach(item => {
      counts[item] = (counts[item] || 0) + 1;
    });
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])[0]?.[0];
  }
};


// ============================================================================
// SURVIVAL ODDS CALCULATOR (Batcomputer Mode)
// ============================================================================

const SurvivalCalculator = {
  // Calculate project survival odds
  calculateOdds(project) {
    const factors = {
      testCoverage: this.getTestCoverageScore(project),
      activityScore: this.getActivityScore(project),
      issueHealth: this.getIssueHealthScore(project),
      debtScore: this.getTechnicalDebtScore(project),
      dependencyHealth: this.getDependencyScore(project),
      securityScore: this.getSecurityScore(project)
    };

    const weights = {
      testCoverage: 0.25,
      activityScore: 0.20,
      issueHealth: 0.15,
      debtScore: 0.15,
      dependencyHealth: 0.15,
      securityScore: 0.10
    };

    let totalScore = 0;
    let totalWeight = 0;

    for (const [factor, score] of Object.entries(factors)) {
      if (score !== null) {
        totalScore += score * weights[factor];
        totalWeight += weights[factor];
      }
    }

    const survivalOdds = totalWeight > 0
      ? Math.round((totalScore / totalWeight) * 100)
      : 50;

    return {
      odds: survivalOdds,
      factors,
      risks: this.identifyRisks(factors),
      recommendations: this.generateRecommendations(factors)
    };
  },

  getTestCoverageScore(project) {
    // Simulate based on project data
    const coverage = project.metrics?.testCoverage || Math.random() * 40 + 40;
    return coverage / 100;
  },

  getActivityScore(project) {
    const lastActivity = new Date(project.metrics?.lastActivity || Date.now());
    const daysSince = (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60 * 24);

    if (daysSince < 7) return 1.0;
    if (daysSince < 14) return 0.8;
    if (daysSince < 30) return 0.6;
    if (daysSince < 60) return 0.4;
    return 0.2;
  },

  getIssueHealthScore(project) {
    const openIssues = project.metrics?.openIssues || Math.floor(Math.random() * 10);
    const closedIssues = project.metrics?.closedIssues || Math.floor(Math.random() * 50);

    if (closedIssues + openIssues === 0) return 0.7;
    return closedIssues / (closedIssues + openIssues);
  },

  getTechnicalDebtScore(project) {
    // Simulate based on project age and size
    return 0.5 + Math.random() * 0.3;
  },

  getDependencyScore(project) {
    // Simulate based on stack
    return 0.6 + Math.random() * 0.3;
  },

  getSecurityScore(project) {
    // Simulate security audit status
    return 0.7 + Math.random() * 0.25;
  },

  identifyRisks(factors) {
    const risks = [];

    if (factors.testCoverage < 0.6) {
      risks.push({
        level: 'high',
        factor: 'testCoverage',
        message: 'Test coverage below 60% threshold'
      });
    }

    if (factors.activityScore < 0.5) {
      risks.push({
        level: 'medium',
        factor: 'activity',
        message: 'Project activity has declined significantly'
      });
    }

    if (factors.securityScore < 0.7) {
      risks.push({
        level: 'high',
        factor: 'security',
        message: 'Security audit recommended'
      });
    }

    return risks;
  },

  generateRecommendations(factors) {
    const recommendations = [];

    if (factors.testCoverage < 0.6) {
      recommendations.push('Increase test coverage to at least 70%');
    }

    if (factors.activityScore < 0.5) {
      recommendations.push('Schedule regular maintenance windows');
    }

    if (factors.dependencyHealth < 0.7) {
      recommendations.push('Update outdated dependencies');
    }

    return recommendations;
  }
};


// ============================================================================
// KNOWLEDGE CRYSTALLIZATION SYSTEM
// ============================================================================

const KnowledgeSystem = {
  crystals: {
    decisions: [],
    patterns: [],
    wisdom: [],
    legacy: []
  },

  init() {
    this.loadCrystals();
    console.log('[NEXUS Knowledge] Crystallization system initialized');
  },

  loadCrystals() {
    try {
      const saved = localStorage.getItem('nexus_crystals');
      if (saved) {
        Object.assign(this.crystals, JSON.parse(saved));
      }
    } catch (e) {
      console.warn('[NEXUS] Could not load crystals');
    }
  },

  saveCrystals() {
    try {
      localStorage.setItem('nexus_crystals', JSON.stringify(this.crystals));
    } catch (e) {
      console.warn('[NEXUS] Could not save crystals');
    }
  },

  // Create a new decision crystal
  crystallizeDecision(decision) {
    const crystal = {
      id: `decision-${Date.now()}`,
      type: 'decision',
      created: new Date().toISOString(),
      what: decision.what,
      why: decision.why,
      alternatives: decision.alternatives || [],
      outcome: decision.outcome || 'pending',
      tags: decision.tags || []
    };

    this.crystals.decisions.push(crystal);
    this.saveCrystals();

    return crystal;
  },

  // Create a pattern crystal
  crystallizePattern(pattern) {
    const crystal = {
      id: `pattern-${Date.now()}`,
      type: 'pattern',
      created: new Date().toISOString(),
      name: pattern.name,
      description: pattern.description,
      language: pattern.language,
      code: pattern.code,
      usageCount: 0,
      tags: pattern.tags || []
    };

    this.crystals.patterns.push(crystal);
    this.saveCrystals();

    return crystal;
  },

  // Create a wisdom crystal
  crystallizeWisdom(wisdom) {
    const crystal = {
      id: `wisdom-${Date.now()}`,
      type: 'wisdom',
      created: new Date().toISOString(),
      insight: wisdom.insight,
      context: wisdom.context,
      source: wisdom.source,
      importance: wisdom.importance || 'medium',
      tags: wisdom.tags || []
    };

    this.crystals.wisdom.push(crystal);
    this.saveCrystals();

    return crystal;
  },

  // Query crystals
  query(queryString, type = 'all') {
    const searchTerms = queryString.toLowerCase().split(' ');
    const results = [];

    const searchIn = type === 'all'
      ? [...this.crystals.decisions, ...this.crystals.patterns, ...this.crystals.wisdom, ...this.crystals.legacy]
      : this.crystals[type] || [];

    for (const crystal of searchIn) {
      const text = JSON.stringify(crystal).toLowerCase();
      const matches = searchTerms.filter(term => text.includes(term));

      if (matches.length > 0) {
        results.push({
          crystal,
          relevance: matches.length / searchTerms.length
        });
      }
    }

    return results
      .sort((a, b) => b.relevance - a.relevance)
      .map(r => r.crystal);
  },

  // Get recent crystals
  getRecent(count = 5) {
    const all = [
      ...this.crystals.decisions,
      ...this.crystals.patterns,
      ...this.crystals.wisdom,
      ...this.crystals.legacy
    ];

    return all
      .sort((a, b) => new Date(b.created) - new Date(a.created))
      .slice(0, count);
  },

  // Get statistics
  getStats() {
    return {
      totalCrystals: Object.values(this.crystals).flat().length,
      decisions: this.crystals.decisions.length,
      patterns: this.crystals.patterns.length,
      wisdom: this.crystals.wisdom.length,
      legacy: this.crystals.legacy.length
    };
  }
};


// ============================================================================
// EXPORT NEXUS CORE
// ============================================================================

const NEXUSCore = {
  personality: PersonalityEngine,
  prediction: PredictiveIntelligence,
  survival: SurvivalCalculator,
  knowledge: KnowledgeSystem,

  // Initialize all systems
  init() {
    console.log('[NEXUS] Initializing core systems...');

    this.personality.init();
    this.prediction.init();
    this.knowledge.init();

    console.log('[NEXUS] All systems online.');

    return this.getGreeting();
  },

  // Get initial greeting
  getGreeting() {
    return this.personality.getGreeting();
  },

  // Process user input
  processInput(input) {
    this.personality.recordInteraction();
    this.prediction.recordCommand(input);

    // Analyze intent
    const intent = this.analyzeIntent(input);

    return {
      intent,
      response: this.generateResponse(intent, input)
    };
  },

  // Analyze user intent
  analyzeIntent(input) {
    const lower = input.toLowerCase();

    if (lower.includes('status') || lower.includes('report')) {
      return { type: 'status', confidence: 0.9 };
    }

    if (lower.includes('switch') || lower.includes('mode')) {
      const modes = ['stark', 'batcave', 'fortress', 'citadel', 'brainiac'];
      const foundMode = modes.find(m => lower.includes(m));
      return { type: 'mode_switch', mode: foundMode, confidence: foundMode ? 0.95 : 0.5 };
    }

    if (lower.includes('analyze') || lower.includes('calculate') || lower.includes('odds')) {
      return { type: 'analysis', confidence: 0.85 };
    }

    if (lower.includes('why') || lower.includes('remember') || lower.includes('history')) {
      return { type: 'knowledge_query', confidence: 0.8 };
    }

    if (lower.includes('help') || lower.includes('what can you')) {
      return { type: 'help', confidence: 0.9 };
    }

    return { type: 'general', confidence: 0.5 };
  },

  // Generate response based on intent
  generateResponse(intent, input) {
    switch (intent.type) {
      case 'status':
        return this.personality.getResponse('analysis', { count: 47 });

      case 'mode_switch':
        if (intent.mode) {
          this.personality.setMode(intent.mode);
          return `Mode switched to ${intent.mode.toUpperCase()}. ${this.personality.getGreeting()}`;
        }
        return "Which mode would you like? Stark, Batcave, Fortress, Citadel, or Brainiac?";

      case 'analysis':
        return this.personality.getResponse('analysis', {
          probability: Math.floor(Math.random() * 30) + 60
        });

      case 'knowledge_query':
        return this.personality.getResponse('wisdom') ||
          "Searching the crystal archives...";

      case 'help':
        return "I am NEXUS, your command center. I can analyze projects, " +
          "switch between operational modes, track patterns, and crystallize knowledge. " +
          "Try: 'status', 'switch to batcave mode', or 'analyze survival odds'.";

      default:
        return this.personality.getResponse('acknowledgments');
    }
  },

  // Get current mode
  getMode() {
    return this.personality.state.mode;
  },

  // Get system status
  getSystemStatus() {
    return {
      mode: this.personality.state.mode,
      mood: this.personality.state.mood,
      energy: this.personality.state.energy,
      predictions: this.prediction.getPredictions(),
      suggestions: this.prediction.getProactiveSuggestions(),
      knowledgeStats: this.knowledge.getStats()
    };
  }
};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NEXUSCore;
}

// Also make available globally
if (typeof window !== 'undefined') {
  window.NEXUSCore = NEXUSCore;
}
