#!/usr/bin/env python3
"""
Data Quality Validation for Herbie Chatbot

This script validates the quality and consistency of training data
to ensure optimal model performance.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
import re
from collections import Counter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityChecker:
    """Validate training data quality for Herbie chatbot."""
    
    def __init__(self, training_data_path: str = "data/training"):
        self.training_data_path = Path(training_data_path)
        self.issues = []
        self.stats = {}
    
    def load_training_data(self) -> List[Dict[str, Any]]:
        """Load training data from JSON file."""
        training_file = self.training_data_path / "herbie_training_data.json"
        
        if not training_file.exists():
            logger.error(f"Training data file not found: {training_file}")
            return []
        
        with open(training_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_basic_structure(self, data: List[Dict[str, Any]]) -> None:
        """Check basic data structure and format."""
        logger.info("Checking basic data structure...")
        
        if not data:
            self.issues.append("No training data found")
            return
        
        required_fields = ['messages', 'context']
        for i, example in enumerate(data):
            # Check top-level structure
            for field in required_fields:
                if field not in example:
                    self.issues.append(f"Example {i}: Missing required field '{field}'")
            
            # Check messages structure
            if 'messages' in example:
                messages = example['messages']
                if not isinstance(messages, list) or len(messages) != 2:
                    self.issues.append(f"Example {i}: Messages should be a list of 2 items")
                    continue
                
                for j, message in enumerate(messages):
                    if not isinstance(message, dict):
                        self.issues.append(f"Example {i}, Message {j}: Should be a dictionary")
                        continue
                    
                    if 'role' not in message or 'content' not in message:
                        self.issues.append(f"Example {i}, Message {j}: Missing 'role' or 'content'")
                    
                    if message.get('role') not in ['user', 'assistant']:
                        self.issues.append(f"Example {i}, Message {j}: Invalid role '{message.get('role')}'")
        
        self.stats['total_examples'] = len(data)
        logger.info(f"Total examples: {len(data)}")
    
    def check_content_quality(self, data: List[Dict[str, Any]]) -> None:
        """Check quality and consistency of content."""
        logger.info("Checking content quality...")
        
        user_inputs = []
        assistant_responses = []
        contexts = []
        
        for example in data:
            if 'messages' not in example or len(example['messages']) != 2:
                continue
            
            user_msg = example['messages'][0]['content']
            assistant_msg = example['messages'][1]['content']
            context = example.get('context', 'unknown')
            
            user_inputs.append(user_msg)
            assistant_responses.append(assistant_msg)
            contexts.append(context)
            
            # Check for empty content
            if not user_msg.strip():
                self.issues.append(f"Empty user input found")
            if not assistant_msg.strip():
                self.issues.append(f"Empty assistant response found")
            
            # Check response length
            if len(assistant_msg) < 5:
                self.issues.append(f"Very short response: '{assistant_msg}'")
            if len(assistant_msg) > 500:
                self.issues.append(f"Very long response (>500 chars): '{assistant_msg[:50]}...'")
        
        # Check for duplicates
        user_duplicates = [item for item, count in Counter(user_inputs).items() if count > 1]
        if user_duplicates:
            self.issues.append(f"Duplicate user inputs found: {len(user_duplicates)} items")
        
        response_duplicates = [item for item, count in Counter(assistant_responses).items() if count > 1]
        if response_duplicates:
            self.issues.append(f"Duplicate assistant responses found: {len(response_duplicates)} items")
        
        self.stats['unique_contexts'] = len(set(contexts))
        self.stats['context_distribution'] = Counter(contexts)
        self.stats['avg_user_input_length'] = sum(len(inp) for inp in user_inputs) / len(user_inputs) if user_inputs else 0
        self.stats['avg_response_length'] = sum(len(resp) for resp in assistant_responses) / len(assistant_responses) if assistant_responses else 0
    
    def check_herbie_characteristics(self, data: List[Dict[str, Any]]) -> None:
        """Check if responses maintain Herbie's character traits."""
        logger.info("Checking Herbie character consistency...")
        
        herbie_indicators = [
            'beep', 'honk', 'engine', 'friend', 'buddy', 'race', 'racing',
            'adventure', 'wheelie', 'yahoo', '*', 'revs', 'purr'
        ]
        
        responses_with_indicators = 0
        total_responses = 0
        
        for example in data:
            if 'messages' not in example or len(example['messages']) != 2:
                continue
            
            assistant_msg = example['messages'][1]['content'].lower()
            total_responses += 1
            
            if any(indicator in assistant_msg for indicator in herbie_indicators):
                responses_with_indicators += 1
        
        if total_responses > 0:
            character_consistency = (responses_with_indicators / total_responses) * 100
            self.stats['character_consistency_percent'] = character_consistency
            
            if character_consistency < 50:
                self.issues.append(f"Low character consistency: only {character_consistency:.1f}% of responses have Herbie characteristics")
    
    def check_conversation_flow(self, data: List[Dict[str, Any]]) -> None:
        """Check if conversations flow naturally."""
        logger.info("Checking conversation flow...")
        
        context_mismatches = 0
        
        for example in data:
            if 'messages' not in example or len(example['messages']) != 2:
                continue
            
            user_input = example['messages'][0]['content'].lower()
            assistant_response = example['messages'][1]['content'].lower()
            context = example.get('context', '')
            
            # Check context relevance
            if context == 'greeting':
                if not any(word in user_input for word in ['hello', 'hi', 'hey', 'morning', 'afternoon']):
                    context_mismatches += 1
            elif context == 'excited':
                if not any(word in user_input for word in ['excited', 'amazing', 'wow']):
                    context_mismatches += 1
        
        if context_mismatches > 0:
            self.issues.append(f"Context mismatches found: {context_mismatches} examples")
        
        self.stats['context_mismatches'] = context_mismatches
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report."""
        report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'statistics': self.stats,
            'issues': self.issues,
            'quality_score': self.calculate_quality_score(),
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def calculate_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        score = 100.0
        
        # Deduct points for issues
        critical_issues = len([issue for issue in self.issues if any(word in issue.lower() for word in ['missing', 'empty', 'error'])])
        warning_issues = len(self.issues) - critical_issues
        
        score -= critical_issues * 10  # 10 points per critical issue
        score -= warning_issues * 2   # 2 points per warning
        
        # Bonus for character consistency
        if 'character_consistency_percent' in self.stats:
            if self.stats['character_consistency_percent'] > 80:
                score += 5
        
        return max(0, min(100, score))
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on findings."""
        recommendations = []
        
        if any('duplicate' in issue.lower() for issue in self.issues):
            recommendations.append("Remove duplicate entries to improve training efficiency")
        
        if any('empty' in issue.lower() for issue in self.issues):
            recommendations.append("Add content to empty fields")
        
        if self.stats.get('character_consistency_percent', 100) < 70:
            recommendations.append("Increase character-specific language and mannerisms in responses")
        
        if self.stats.get('total_examples', 0) < 100:
            recommendations.append("Consider adding more training examples for better model performance")
        
        context_dist = self.stats.get('context_distribution', {})
        if context_dist:
            min_context_count = min(context_dist.values())
            if min_context_count < 5:
                recommendations.append("Balance context distribution - some contexts have very few examples")
        
        return recommendations
    
    def run_validation(self) -> Dict[str, Any]:
        """Run complete validation process."""
        logger.info("Starting data quality validation...")
        
        data = self.load_training_data()
        
        if not data:
            return self.generate_report()
        
        self.check_basic_structure(data)
        self.check_content_quality(data)
        self.check_herbie_characteristics(data)
        self.check_conversation_flow(data)
        
        report = self.generate_report()
        
        # Save report
        report_file = self.training_data_path / "quality_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Quality report saved to {report_file}")
        logger.info(f"Quality score: {report['quality_score']:.1f}/100")
        
        return report

def main():
    """Main function to run data quality checks."""
    checker = DataQualityChecker()
    report = checker.run_validation()
    
    print(f"\nData Quality Report")
    print("=" * 50)
    print(f"Quality Score: {report['quality_score']:.1f}/100")
    print(f"Total Examples: {report['statistics'].get('total_examples', 0)}")
    print(f"Issues Found: {len(report['issues'])}")
    
    if report['issues']:
        print("\nIssues:")
        for issue in report['issues'][:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(report['issues']) > 10:
            print(f"  ... and {len(report['issues']) - 10} more")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    main()