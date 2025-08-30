#!/usr/bin/env python3
"""
Test script for Ollama Herbie model
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))

from models.ollama_model import HerbieOllamaModel
import time

def test_ollama_models():
    """Test both base and fine-tuned Ollama models"""
    
    models_to_test = [
        ("herbie-gemma3:4b", "Fine-tuned Herbie Model"),
        ("gemma3:4b", "Base Gemma3 Model")
    ]
    
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
        }
    ]
    
    print("="*60)
    print("🤖 HERBIE OLLAMA MODEL TESTING")
    print("="*60)
    
    for model_name, model_desc in models_to_test:
        print(f"\n🔥 Testing: {model_desc} ({model_name})")
        print("-" * 50)
        
        try:
            model = HerbieOllamaModel(model_name)
            print(f"✅ Model loaded successfully!")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 Test {i}: {test_case['input']}")
                print(f"📋 Context: {test_case['context']}")
                
                start_time = time.time()
                result = model.generate_response(
                    user_input=test_case['input'],
                    context=test_case['context'],
                    temperature=0.7
                )
                end_time = time.time()
                
                print(f"🤖 Response: {result['response']}")
                print(f"😊 Emotion: {result['emotion']}")
                print(f"📊 Confidence: {result['confidence']}")
                print(f"⚡ Model: {result['model_used']}")
                print(f"⏱️  Time: {end_time - start_time:.2f}s")
                
        except Exception as e:
            print(f"❌ Error testing {model_name}: {e}")
        
        print("\n" + "="*50)
    
    print("\n🎉 Testing completed!")

def test_api_status():
    """Test Ollama API connection"""
    print("🔍 Testing Ollama API connection...")
    
    try:
        model = HerbieOllamaModel("gemma3:4b")
        available_models = model.get_available_models()
        
        print("✅ Ollama API is accessible")
        print(f"📋 Available models: {available_models}")
        
        if "herbie-gemma3:4b" in available_models:
            print("✅ Fine-tuned Herbie model found!")
        else:
            print("⚠️  Fine-tuned Herbie model not found")
            print("💡 You can create it using: ollama create herbie-gemma3:4b -f Modelfile")
            
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("💡 Make sure Ollama is running: ollama serve")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Ollama Herbie models")
    parser.add_argument("--api-only", action="store_true", help="Only test API connection")
    
    args = parser.parse_args()
    
    if args.api_only:
        test_api_status()
    else:
        test_api_status()
        print("\n")
        test_ollama_models()