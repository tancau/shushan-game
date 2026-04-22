#!/bin/bash
# Script to help manage Bing Image Creator generation

EFFECTS_DIR="$HOME/.openclaw/workspace/shushan-game/frontend/public/assets/images/effects"

# Create effects directory
mkdir -p "$EFFECTS_DIR"

# Function to generate and save images
# This script is a helper - the main work is done via browser automation

echo "Effects directory: $EFFECTS_DIR"
echo "Directory created: $(ls -la $EFFECTS_DIR)"

# List of prompts to generate
PROMPTS=(
  "glow_golden:Chinese fantasy game golden light glow effect, cultivation breakthrough aura, bright center radiating outward, transparent background, game effect, 512x512"
  "glow_purple:Chinese fantasy game purple mystical glow effect, cultivation power aura, ethereal light, transparent background, game effect, 512x512"
  "glow_blue:Chinese fantasy game blue energy glow effect, cultivation true essence aura, flowing light, transparent background, game effect, 512x512"
)

echo "Total prompts to process: ${#PROMPTS[@]}"
