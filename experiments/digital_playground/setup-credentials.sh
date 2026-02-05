#!/bin/bash

# Setup OpenCode credentials in the proper location

mkdir -p ~/.config/opencode

# Create credentials.json
cat > ~/.config/opencode/credentials.json << 'CREDS'
{
  "openrouter": {
    "apiKey": "$OPENROUTER_API_KEY"
  },
  "anthropic": {
    "apiKey": "$ANTHROPIC_API_KEY"
  },
  "opencode": {
    "apiKey": "$OPENCODE_API_KEY"
  }
}
CREDS

echo "✅ Credentials file created at ~/.config/opencode/credentials.json"
echo ""
echo "This uses your environment variables from ~/.zshrc"
echo "Make sure you've run: ./setup-api-keys.sh first"
