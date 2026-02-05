#!/bin/bash

# OpenCode API Key Setup Script
# Adds API keys to ~/.zshrc for persistent storage

echo "🔑 OpenCode API Key Setup"
echo "=========================="
echo ""
echo "Enter your API keys below. They will be saved to ~/.zshrc"
echo "You only need to do this ONCE."
echo ""

# Read API keys
read -p "OpenRouter API Key (or press Enter to skip): " OPENROUTER_KEY
read -p "Anthropic API Key (for Claude Haiku vision, or press Enter to skip): " ANTHROPIC_KEY
read -p "OpenCode Zen API Key (or press Enter to skip): " OPENCODE_KEY

# Backup .zshrc
cp ~/.zshrc ~/.zshrc.backup
echo "✅ Backed up ~/.zshrc to ~/.zshrc.backup"

# Append to .zshrc
{
  echo ""
  echo "# OpenCode API Keys (added $(date))"
  [ -n "$OPENROUTER_KEY" ] && echo "export OPENROUTER_API_KEY=\"$OPENROUTER_KEY\""
  [ -n "$ANTHROPIC_KEY" ] && echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_KEY\""
  [ -n "$OPENCODE_KEY" ] && echo "export OPENCODE_API_KEY=\"$OPENCODE_KEY\""
} >> ~/.zshrc

echo ""
echo "✅ API keys saved to ~/.zshrc"
echo ""
echo "Reloading shell config..."
source ~/.zshrc

echo "✅ Done! Try running: ./opencode-dual-agent.sh"
