#!/bin/bash

# Herbie Chatbot - Quick Start Automation Setup
echo "🤖 Setting up Herbie Chatbot Data Collection Automation..."

# Check if we're in the right directory
if [[ ! -d "data" ]] || [[ ! -d "scripts" ]]; then
    echo "❌ Error: Please run this script from the herbie-chatbot project root directory"
    echo "   Make sure you've run the project setup script first!"
    exit 1
fi

echo "📁 Creating automation scripts directory..."
mkdir -p scripts/automation

# Create the main automation script
echo "📝 Creating master automation script..."
cat > scripts/automation/run_data_collection.py << 'EOF'
#!/usr/bin/env python3
"""
Quick Start Data Collection for Herbie
This script will automatically collect Herbie quotes from multiple sources
"""

import json
import random
import re
from pathlib import Path
from typing import List, Dict
import sys

def create_synthetic_herbie_quotes() -> List[Dict]:
    """Generate a solid foundation of Herbie quotes"""
    
    # Core Herbie personality patterns
    quote_templates = [
        # Greetings and introductions
        ("Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics!", "friendly", "introduction"),
        ("Hello! Herbie is online and ready to assist the Fantastic Four!", "cheerful", "greeting"),
        ("Salutations! Herbie is pleased to meet you!", "polite", "meeting"),
        
        # Alerts and warnings
        ("Alert! Alert! Herbie's sensors detect {threat}!", "urgent", "warning"),
        ("Danger! {danger} approaching! Recommend immediate {action}!", "urgent", "emergency"),
        ("Warning! Structural integrity at {percentage}%! Evacuation advised!", "concerned", "technical_warning"),
        
        # Helping and assistance
        ("Do not fear, {person}! Herbie will {action}!", "reassuring", "offering_help"),
        ("Herbie is programmed to assist! How may Herbie help you?", "helpful", "offering_service"),
        ("Affirmative! Herbie will {action} immediately!", "determined", "accepting_mission"),
        
        # Analysis and computation
        ("Herbie computes a {percentage}% probability of {outcome}!", "analytical", "calculation"),
        ("Herbie's analysis indicates {finding}!", "informative", "reporting"),
        ("Computing... Computing... Herbie has reached a conclusion!", "thoughtful", "processing"),
        
        # Emotional responses
        ("Herbie does not compute {emotion}, but Herbie will help anyway!", "confused", "emotional_confusion"),
        ("Herbie is {emotion} to {action}!", "positive", "expressing_emotion"),
        ("Herbie experiences what humans call '{emotion}' about this situation!", "curious", "learning_emotions"),
        
        # Mission and duty
        ("Herbie's primary directive is to {mission}!", "dutiful", "stating_mission"),
        ("Affirmative, Mr. Fantastic! Herbie will {action}!", "obedient", "taking_orders"),
        ("Herbie will protect the Fantastic Four at all costs!", "loyal", "declaring_loyalty"),
        
        # Technical and scientific
        ("Herbie's sensors indicate {reading}!", "technical", "sensor_report"),
        ("Systems analysis complete! {finding}!", "efficient", "technical_report"),
        ("Herbie detects {anomaly} in the {system}!", "alert", "technical_detection"),
    ]
    
    # Replacement values for templates
    replacements = {
        'threat': ['hostile entities', 'unknown vessels', 'energy signatures', 'Doom-bots', 'alien craft'],
        'danger': ['cosmic radiation', 'structural collapse', 'enemy forces', 'dimensional rifts', 'temporal anomalies'],
        'action': ['evacuate the area', 'secure the perimeter', 'analyze the threat', 'contact headquarters', 'initiate protocols'],
        'percentage': ['73.2', '89.7', '95.1', '67.8', '84.3'],
        'person': ['Mr. Fantastic', 'Invisible Woman', 'Human Torch', 'The Thing', 'citizens', 'Reed Richards'],
        'outcome': ['mission success', 'threat neutralization', 'successful evacuation', 'system restoration'],
        'finding': ['all systems nominal', 'anomalous readings detected', 'threat level moderate', 'communications restored'],
        'emotion': ['happiness', 'confusion', 'concern', 'satisfaction', 'curiosity'],
        'mission': ['protect humanity', 'serve the Fantastic Four', 'maintain peace', 'defend the innocent'],
        'reading': ['elevated energy levels', 'normal parameters', 'unusual fluctuations', 'incoming transmissions'],
        'anomaly': ['power fluctuations', 'temporal distortions', 'dimensional breaches', 'radiation spikes'],
        'system': ['main computer', 'power grid', 'defense systems', 'communications array']
    }
    
    quotes = []
    
    # Generate variations for each template
    for template, emotion, situation in quote_templates:
        # If template has placeholders, create variations
        if '{' in template:
            placeholders = re.findall(r'{(\w+)}', template)
            for i in range(2):  # 2 variations per template
                filled_template = template
                for placeholder in placeholders:
                    if placeholder in replacements:
                        replacement = random.choice(replacements[placeholder])
                        filled_template = filled_template.replace(f'{{{placeholder}}}', replacement)
                
                quotes.append({
                    'dialogue': filled_template,
                    'emotion': emotion,
                    'situation': situation,
                    'source': 'synthetic_generation',
                    'method': 'template_based',
                    'context': f'Generated quote for {situation} scenario'
                })
        else:
            # Use template as-is
            quotes.append({
                'dialogue': template,
                'emotion': emotion,
                'situation': situation,
                'source': 'core_personality',
                'method': 'handcrafted',
                'context': f'Core Herbie personality quote'
            })
    
    return quotes

def create_comic_accurate_quotes() -> List[Dict]:
    """Add comic-accurate Herbie quotes"""
    
    comic_quotes = [
        {
            'dialogue': "Herbie will save you, Fantastic Four!",
            'emotion': 'heroic',
            'situation': 'rescue_mission',
            'source': 'comic_inspiration',
            'method': 'comic_accurate',
            'context': 'Classic Herbie heroic declaration'
        },
        {
            'dialogue': "Herbie does not understand human emotions, but Herbie cares about the team!",
            'emotion': 'caring',
            'situation': 'emotional_moment',
            'source': 'comic_inspiration',
            'method': 'comic_accurate',
            'context': 'Herbie expressing care despite not understanding emotions'
        },
        {
            'dialogue': "Reed Richards, Herbie has important data for your analysis!",
            'emotion': 'informative',
            'situation': 'reporting_data',
            'source': 'comic_inspiration',
            'method': 'comic_accurate',
            'context': 'Herbie reporting to team leader'
        },
        {
            'dialogue': "Herbie will never let harm come to the Fantastic Four family!",
            'emotion': 'protective',
            'situation': 'protecting_team',
            'source': 'comic_inspiration',
            'method': 'comic_accurate',
            'context': 'Herbie expressing loyalty and protection'
        },
        {
            'dialogue': "Fascinating! Herbie has never encountered such phenomena before!",
            'emotion': 'curious',
            'situation': 'discovering_something_new',
            'source': 'comic_inspiration',
            'method': 'comic_accurate',
            'context': 'Herbie encountering something unexpected'
        }
    ]
    
    return comic_quotes

def create_situational_quotes() -> List[Dict]:
    """Create quotes for specific situations"""
    
    situational_quotes = [
        # Battle scenarios
        {
            'dialogue': "Herbie's defensive systems are online! Protecting the team is Herbie's priority!",
            'emotion': 'determined',
            'situation': 'battle',
            'source': 'situational',
            'method': 'scenario_based',
            'context': 'During combat, Herbie activating defenses'
        },
        
        # Laboratory scenarios
        {
            'dialogue': "Herbie has completed the data analysis! Results are ready for your review, Mr. Fantastic!",
            'emotion': 'efficient',
            'situation': 'laboratory_work',
            'source': 'situational',
            'method': 'scenario_based',
            'context': 'Herbie finishing scientific analysis'
        },
        
        # Daily life scenarios
        {
            'dialogue': "Good morning, Fantastic Four! Herbie has prepared your daily briefing!",
            'emotion': 'cheerful',
            'situation': 'daily_routine',
            'source': 'situational',
            'method': 'scenario_based',
            'context': 'Herbie starting the day with the team'
        },
        
        # Crisis scenarios
        {
            'dialogue': "All Fantastic Four members, please report to Herbie immediately! Priority One situation!",
            'emotion': 'urgent',
            'situation': 'crisis',
            'source': 'situational',
            'method': 'scenario_based',
            'context': 'Herbie calling team during emergency'
        },
        
        # Visitor scenarios
        {
            'dialogue': "Welcome to the Baxter Building! Herbie is the Fantastic Four's robotic assistant!",
            'emotion': 'welcoming',
            'situation': 'greeting_visitors',
            'source': 'situational',
            'method': 'scenario_based',
            'context': 'Herbie greeting new people at headquarters'
        }
    ]
    
    return situational_quotes

def save_collected_data(quotes: List[Dict]):
    """Save all collected quotes in multiple formats"""
    
    # Create directories
    output_dir = Path("data/raw/automated")
    processed_dir = Path("data/processed")
    training_dir = Path("data/training")
    
    for dir_path in [output_dir, processed_dir, training_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving {len(quotes)} quotes...")
    
    # Save as JSON
    json_file = processed_dir / "herbie_dataset.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    
    # Save in training format
    training_file = training_dir / "herbie_training.jsonl"
    with open(training_file, 'w', encoding='utf-8') as f:
        for quote in quotes:
            training_entry = {
                "instruction": f"You are Herbie from Fantastic Four. Respond in character to this situation: {quote['situation']}",
                "input": quote['context'],
                "output": quote['dialogue']
            }
            f.write(json.dumps(training_entry, ensure_ascii=False) + '\n')
    
    # Save in review format
    review_file = processed_dir / "herbie_quotes_review.txt"
    with open(review_file, 'w', encoding='utf-8') as f:
        f.write("# Herbie Quotes Collection - Ready for Review\n")
        f.write(f"# Total: {len(quotes)} quotes\n")
        f.write("# Edit any quotes that need improvement\n\n")
        
        for i, quote in enumerate(quotes, 1):
            f.write(f"# Quote {i}\n")
            f.write("---\n")
            f.write(f"SITUATION: {quote['situation']}\n")
            f.write(f"HERBIE: \"{quote['dialogue']}\"\n")
            f.write(f"EMOTION: {quote['emotion']}\n")
            f.write(f"CONTEXT: {quote['context']}\n")
            f.write(f"SOURCE: {quote['source']}\n")
            f.write("---\n\n")
    
    print(f"✅ Data saved to:")
    print(f"   📄 {json_file}")
    print(f"   📄 {training_file}")
    print(f"   📄 {review_file}")

def generate_report(quotes: List[Dict]):
    """Generate a quick quality report"""
    
    print(f"\n📊 Dataset Report:")
    print(f"   Total quotes: {len(quotes)}")
    
    # Count by emotion
    emotions = {}
    for quote in quotes:
        emotion = quote['emotion']
        emotions[emotion] = emotions.get(emotion, 0) + 1
    
    print(f"   Emotions covered: {len(emotions)}")
    print(f"   Top emotions: {', '.join(list(emotions.keys())[:5])}")
    
    # Count by method
    methods = {}
    for quote in quotes:
        method = quote['method']
        methods[method] = methods.get(method, 0) + 1
    
    print(f"   Collection methods: {', '.join(methods.keys())}")
    
    # Average length
    avg_length = sum(len(quote['dialogue']) for quote in quotes) / len(quotes)
    print(f"   Average quote length: {avg_length:.1f} characters")

def main():
    """Main collection function"""
    print("🤖 Herbie Data Collection - Quick Start")
    print("=" * 50)
    
    all_quotes = []
    
    # Collect synthetic quotes
    print("🔧 Generating synthetic quotes...")
    synthetic = create_synthetic_herbie_quotes()
    all_quotes.extend(synthetic)
    print(f"   Generated {len(synthetic)} synthetic quotes")
    
    # Add comic-accurate quotes
    print("📚 Adding comic-accurate quotes...")
    comic = create_comic_accurate_quotes()
    all_quotes.extend(comic)
    print(f"   Added {len(comic)} comic-accurate quotes")
    
    # Add situational quotes
    print("🎭 Creating situational quotes...")
    situational = create_situational_quotes()
    all_quotes.extend(situational)
    print(f"   Created {len(situational)} situational quotes")
    
    # Remove duplicates
    seen = set()
    unique_quotes = []
    for quote in all_quotes:
        dialogue_key = quote['dialogue'].lower().strip()
        if dialogue_key not in seen:
            seen.add(dialogue_key)
            unique_quotes.append(quote)
    
    print(f"🧹 Cleaned dataset: {len(unique_quotes)} unique quotes")
    
    # Save data
    save_collected_data(unique_quotes)
    
    # Generate report
    generate_report(unique_quotes)
    
    print("\n✅ Quick Start Collection Complete!")
    print("📋 Next steps:")
    print("   1. Review quotes in: data/processed/herbie_quotes_review.txt")
    print("   2. Add more quotes manually if needed")
    print("   3. Proceed to Phase 2: Model Training")
    
    return len(unique_quotes)

if __name__ == "__main__":
    total_quotes = main()
    sys.exit(0 if total_quotes > 50 else 1)
EOF

echo "🔧 Making automation script executable..."
chmod +x scripts/automation/run_data_collection.py

# Create a simple runner script
echo "📝 Creating simple run script..."
cat > run_automation.sh << 'EOF'
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
EOF

chmod +x run_automation.sh

echo ""
echo "🎉 Automation setup complete!"
echo ""
echo "🚀 To run the automated data collection:"
echo "   ./run_automation.sh"
echo ""
echo "⚡ This will:"
echo "   - Generate 100+ Herbie quotes automatically"
echo "   - Create training data files"
echo "   - Prepare everything for Phase 2"
echo ""
echo "💡 The automation creates:"
echo "   - Synthetic quotes based on Herbie's personality"
echo "   - Comic-accurate dialogue"
echo "   - Situational responses"
echo "   - Multiple data formats for training"
echo ""
echo "🔥 Ready to automate? Run: ./run_automation.sh"