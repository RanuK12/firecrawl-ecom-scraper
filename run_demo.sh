#!/usr/bin/env bash
set -e

echo "🚀 Firecrawl E-Commerce Scraper - Demo Mode"
echo "=========================================="
echo ""

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env from .env.example"
else
    echo "ℹ️  .env already exists, skipping copy"
fi

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Run the demo
echo ""
echo "🎯 Running scraper in demo mode..."
python3 -m scraper --demo --output output.csv

echo ""
echo "✅ Demo finished! Check output.csv for the generated CSV."