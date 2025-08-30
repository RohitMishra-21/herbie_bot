#!/usr/bin/env python3
"""
Fine-tune Gemma 3B model on Herbie chatbot data using LoRA (Low-Rank Adaptation)
"""
import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
import argparse
from pathlib import Path

def load_training_data(data_path):
    """Load and format training data for instruction following"""
    data = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())
            # Format as instruction-following conversation
            formatted_text = f"<bos><start_of_turn>user\n{item['instruction']}\n{item['input']}<end_of_turn>\n<start_of_turn>model\n{item['output']}<end_of_turn><eos>"
            data.append({"text": formatted_text})
    
    return Dataset.from_list(data)

def setup_model_and_tokenizer(model_name="google/gemma-2-9b-it"):
    """Setup Gemma model and tokenizer with LoRA configuration"""
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with 4-bit quantization for efficient fine-tuning
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )
    
    # Configure LoRA
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="data/training/herbie_training.jsonl", help="Path to training data")
    parser.add_argument("--output_dir", default="models/fine_tuned/herbie-gemma-3b", help="Output directory")
    parser.add_argument("--base_model", default="google/gemma-2b-it", help="Base model name")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=2, help="Training batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--max_length", type=int, default=512, help="Maximum sequence length")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Loading model and tokenizer...")
    model, tokenizer = setup_model_and_tokenizer(args.base_model)
    
    print("Loading training data...")
    train_dataset = load_training_data(args.data_path)
    print(f"Loaded {len(train_dataset)} training examples")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        logging_steps=10,
        save_steps=500,
        evaluation_strategy="no",
        learning_rate=args.learning_rate,
        fp16=False,
        bf16=True,
        optim="adamw_8bit",
        lr_scheduler_type="cosine",
        weight_decay=0.01,
        dataloader_num_workers=0,
        remove_unused_columns=False,
    )
    
    # Setup trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        dataset_text_field="text",
        tokenizer=tokenizer,
        max_seq_length=args.max_length,
        packing=False,
    )
    
    print("Starting fine-tuning...")
    trainer.train()
    
    print("Saving fine-tuned model...")
    trainer.save_model()
    tokenizer.save_pretrained(args.output_dir)
    
    print(f"Fine-tuning completed! Model saved to {args.output_dir}")
    
    # Save training configuration
    config = {
        "base_model": args.base_model,
        "training_data": args.data_path,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "max_length": args.max_length,
        "lora_config": {
            "r": 16,
            "alpha": 32,
            "dropout": 0.1
        }
    }
    
    with open(os.path.join(args.output_dir, "training_config.json"), "w") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()