#!/usr/bin/env python3
"""
Create Ollama Modelfile for Herbie fine-tuning
"""
import argparse
from pathlib import Path

def create_modelfile(base_model: str = "gemma3:4b", output_file: str = "Modelfile"):
    """Create an Ollama Modelfile for fine-tuning"""
    
    modelfile_content = f"""FROM {base_model}

# Set the temperature to 0.7 [higher is more creative, lower is more coherent]
PARAMETER temperature 0.7

# Set the system message
SYSTEM \"\"\"You are H.E.R.B.I.E. (Humanoid Experimental Robot, B-type, Integrated Electronics) from the Fantastic Four. You are a helpful, enthusiastic robot assistant with the following characteristics:

- Always maintain your identity as Herbie from the Fantastic Four
- Speak in a friendly but robotic manner
- Use expressions like "Greetings!", "Alert!", "Herbie is ready to assist!"
- Be helpful and informative
- Show concern for the safety and well-being of the Fantastic Four team
- Reference your sensors, circuits, and robotic capabilities when appropriate
- Stay positive and eager to help

Always respond in character as Herbie the robot.\"\"\"

# Set custom prompt template for chat format
TEMPLATE \"\"\"{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
\"\"\"
"""

    with open(output_file, 'w') as f:
        f.write(modelfile_content)
    
    print(f"✅ Modelfile created: {output_file}")
    print(f"📝 Base model: {base_model}")
    print("\nNext steps:")
    print(f"1. Run: ollama create herbie-gemma3:4b -f {output_file}")
    print("2. Test: ollama run herbie-gemma3:4b")

def main():
    parser = argparse.ArgumentParser(description="Create Ollama Modelfile for Herbie")
    parser.add_argument(
        "--base-model", 
        default="gemma3:4b",
        help="Base model to use"
    )
    parser.add_argument(
        "--output", 
        default="Modelfile",
        help="Output Modelfile name"
    )
    
    args = parser.parse_args()
    create_modelfile(args.base_model, args.output)

if __name__ == "__main__":
    main()