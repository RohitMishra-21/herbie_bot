#!/usr/bin/env python3
"""
Create Training Data for Herbie Chatbot

This script processes raw character data and creates structured training datasets
for fine-tuning the chatbot model.
"""

import json
import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HerbieDataProcessor:
    """Process raw Herbie character data into training format."""
    
    def __init__(self, raw_data_path: str = "data/raw", output_path: str = "data/training"):
        self.raw_data_path = Path(raw_data_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def load_raw_data(self) -> Dict[str, Any]:
        """Load raw character data from files."""
        data = {
            'quotes': [],
            'personality_traits': [],
            'response_patterns': []
        }
        
        # Load template file
        template_file = self.raw_data_path / "herbie_quotes_template.txt"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                data['quotes'] = self.extract_quotes(content)
                data['personality_traits'] = self.extract_personality_traits(content)
                data['response_patterns'] = self.extract_response_patterns(content)
        
        return data
    
    def extract_quotes(self, content: str) -> List[str]:
        """Extract quotes from the template content."""
        quotes = []
        lines = content.split('\n')
        
        in_quotes_section = False
        for line in lines:
            line = line.strip()
            if line.startswith('###') or line.startswith('##'):
                in_quotes_section = 'Sample Quotes' in line or 'Greetings' in line or 'Excitement' in line or 'Concern' in line or 'Playful' in line or 'Determination' in line or 'Racing' in line
            elif in_quotes_section and line.startswith('"') and line.endswith('"'):
                quotes.append(line[1:-1])  # Remove quotes
        
        return quotes
    
    def extract_personality_traits(self, content: str) -> List[str]:
        """Extract personality traits from content."""
        traits = []
        lines = content.split('\n')
        
        in_traits_section = False
        for line in lines:
            line = line.strip()
            if '## Personality Traits' in line:
                in_traits_section = True
            elif line.startswith('##') and in_traits_section:
                break
            elif in_traits_section and line.startswith('-'):
                traits.append(line[1:].strip())
        
        return traits
    
    def extract_response_patterns(self, content: str) -> List[str]:
        """Extract response patterns from content."""
        patterns = []
        lines = content.split('\n')
        
        in_patterns_section = False
        for line in lines:
            line = line.strip()
            if '## Response Patterns' in line:
                in_patterns_section = True
            elif line.startswith('##') and in_patterns_section:
                break
            elif in_patterns_section and line.startswith('-'):
                patterns.append(line[1:].strip())
        
        return patterns
    
    def create_conversation_pairs(self, quotes: List[str]) -> List[Dict[str, str]]:
        """Create conversation pairs for training."""
        pairs = []
        
        # Create greeting pairs
        greetings = ["Hello", "Hi", "Hey", "Good morning", "Good afternoon", "Hi Herbie"]
        herbie_greetings = [q for q in quotes if any(word in q.lower() for word in ['hello', 'beep', 'ready'])]
        
        for greeting in greetings:
            for response in herbie_greetings:
                pairs.append({
                    "input": greeting,
                    "output": response,
                    "context": "greeting"
                })
        
        # Create emotion-based pairs
        emotions = {
            "excited": ["I'm so excited!", "This is amazing!", "Wow!"],
            "worried": ["I'm worried", "This doesn't look good", "Are we safe?"],
            "ready_for_adventure": ["Let's go!", "Ready for adventure?", "Want to race?"]
        }
        
        for emotion, inputs in emotions.items():
            relevant_quotes = [q for q in quotes if any(word in q.lower() for word in ['excited', 'fantastic', 'worried', 'adventure', 'race'])]
            for input_text in inputs:
                for quote in relevant_quotes[:2]:  # Limit to avoid too many combinations
                    pairs.append({
                        "input": input_text,
                        "output": quote,
                        "context": emotion
                    })
        
        return pairs
    
    def create_training_dataset(self) -> None:
        """Create the main training dataset."""
        logger.info("Loading raw data...")
        raw_data = self.load_raw_data()
        
        logger.info("Creating conversation pairs...")
        conversation_pairs = self.create_conversation_pairs(raw_data['quotes'])
        
        # Create DataFrame
        df = pd.DataFrame(conversation_pairs)
        
        # Save as JSON for model training
        training_data = []
        for _, row in df.iterrows():
            training_data.append({
                "messages": [
                    {"role": "user", "content": row['input']},
                    {"role": "assistant", "content": row['output']}
                ],
                "context": row['context']
            })
        
        # Save training data
        output_file = self.output_path / "herbie_training_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created {len(training_data)} training examples")
        logger.info(f"Training data saved to {output_file}")
        
        # Save CSV for analysis
        csv_file = self.output_path / "herbie_conversations.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"CSV data saved to {csv_file}")
        
        # Create metadata
        metadata = {
            "total_examples": len(training_data),
            "personality_traits": raw_data['personality_traits'],
            "response_patterns": raw_data['response_patterns'],
            "contexts": list(df['context'].unique())
        }
        
        metadata_file = self.output_path / "dataset_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Metadata saved to {metadata_file}")

def main():
    """Main function to create training data."""
    processor = HerbieDataProcessor()
    processor.create_training_dataset()
    print("Training data creation complete!")

if __name__ == "__main__":
    main()