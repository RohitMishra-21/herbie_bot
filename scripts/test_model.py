#!/usr/bin/env python3
"""
Test script for the fine-tuned Herbie Gemma model
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))

from models.gemma_model import HerbieGemmaModel
import json

def test_model():
    """Test the fine-tuned model with sample inputs"""
    
    model_path = "models/fine_tuned/herbie-gemma-3b"
    
    print("Loading Herbie Gemma model...")
    try:
        model = HerbieGemmaModel(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "input": "Hello Herbie!",
            "context": "greeting"
        },
        {
            "input": "Can you help me?",
            "context": "offering_help"
        },
        {
            "input": "There's danger approaching!",
            "context": "emergency"
        },
        {
            "input": "What can you do?",
            "context": "introduction"
        },
        {
            "input": "System malfunction detected",
            "context": "technical_warning"
        }
    ]
    
    print("\n" + "="*50)
    print("Testing Herbie Gemma Model")
    print("="*50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input: {test_case['input']}")
        print(f"Context: {test_case['context']}")
        print("-" * 30)
        
        try:
            result = model.generate_response(
                user_input=test_case['input'],
                context=test_case['context'],
                temperature=0.7,
                max_length=128
            )
            
            print(f"Response: {result['response']}")
            print(f"Emotion: {result['emotion']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Model: {result['model_used']}")
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
    
    print("\n" + "="*50)
    print("Testing completed!")
    print("="*50)

if __name__ == "__main__":
    test_model()