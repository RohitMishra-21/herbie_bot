#!/usr/bin/env python3
"""
Convert Herbie training data to Ollama fine-tuning format
"""
import json
import argparse
from pathlib import Path

def convert_to_ollama_format(input_file: str, output_file: str):
    """Convert JSONL training data to Ollama fine-tuning format"""
    
    conversations = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())
            
            # Create a conversation format for Ollama
            conversation = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are H.E.R.B.I.E. (Humanoid Experimental Robot, B-type, Integrated Electronics) from the Fantastic Four. You are helpful, enthusiastic, and speak in a robotic but friendly manner. Always stay in character as Herbie."
                    },
                    {
                        "role": "user", 
                        "content": f"{item['instruction']}\n{item['input']}"
                    },
                    {
                        "role": "assistant",
                        "content": item['output']
                    }
                ]
            }
            conversations.append(conversation)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for conversation in conversations:
            f.write(json.dumps(conversation) + '\n')
    
    print(f"✅ Converted {len(conversations)} examples")
    print(f"📁 Output saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert Herbie data for Ollama fine-tuning")
    parser.add_argument(
        "--input", 
        default="data/training/herbie_training.jsonl",
        help="Input JSONL file"
    )
    parser.add_argument(
        "--output", 
        default="data/training/herbie_ollama_training.jsonl",
        help="Output file for Ollama"
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    convert_to_ollama_format(args.input, args.output)

if __name__ == "__main__":
    main()