#!/bin/bash

echo "🤖 Starting Herbie Data Collection Automation..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install basic requirements
echo "📦 Installing required packages..."
python3 -m pip install --quiet --user requests beautifulsoup4 pandas 2>/dev/null || echo "⚠️  Some packages may not install - continuing..."

# Run the collection
echo "🚀 Running data collection..."
python3 scripts/automation/run_data_collection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Your Herbie dataset is ready!"
    echo ""
    echo "📁 Files created:"
    echo "   - data/processed/herbie_dataset.json"
    echo "   - data/training/herbie_training.jsonl"
    echo "   - data/processed/herbie_quotes_review.txt"
    echo ""
    echo "📋 What to do next:"
    echo "   1. Review: data/processed/herbie_quotes_review.txt"
    echo "   2. Add more quotes manually if desired"
    echo "   3. Proceed to Phase 2: Model Training"
    echo ""
    echo "✨ You now have a complete Herbie dataset!"
else
    echo "❌ Collection failed. Check the output above for errors."
fi
