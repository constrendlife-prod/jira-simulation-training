#!/bin/bash
# ────────────────────────────────────────────────────────────────────────────
# Git Push Helper Script
# ────────────────────────────────────────────────────────────────────────────
# This script loads your GitHub credentials from .env and pushes to remote
# ────────────────────────────────────────────────────────────────────────────

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN not found in .env file!"
    exit 1
fi

# Get commit message from argument or use default
COMMIT_MSG="${1:-Update: Changes to CORE Engineer Training Portal}"

echo "────────────────────────────────────────────────────────────────"
echo "🚀 Git Push Helper for Jira Simulation Project"
echo "────────────────────────────────────────────────────────────────"
echo ""

# Show current status
echo "📊 Current Git Status:"
git status --short
echo ""

# Ask for confirmation
read -p "Do you want to commit and push these changes? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📦 Adding files..."
    git add .

    echo "💾 Creating commit..."
    git commit -m "$COMMIT_MSG"

    echo "🔐 Pushing to GitHub (using token from .env)..."
    # Use token in URL for authentication
    git push https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/constrendlife-prod/jira-simulation-training.git main

    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 Repository: https://github.com/constrendlife-prod/jira-simulation-training"
else
    echo ""
    echo "❌ Push cancelled."
fi
