"""
Gemma 3B model integration for Herbie chatbot
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class HerbieGemmaModel:
    def __init__(self, model_path: str, base_model: str = "google/gemma-2b-it"):
        """
        Initialize the fine-tuned Herbie Gemma model
        
        Args:
            model_path: Path to the fine-tuned LoRA adapter
            base_model: Base Gemma model name
        """
        self.model_path = Path(model_path)
        self.base_model = base_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the fine-tuned model and tokenizer"""
        try:
            logger.info(f"Loading tokenizer from {self.base_model}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Loading base model {self.base_model}")
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                load_in_4bit=True
            )
            
            # Load fine-tuned LoRA adapter if it exists
            if self.model_path.exists():
                logger.info(f"Loading fine-tuned adapter from {self.model_path}")
                self.model = PeftModel.from_pretrained(base_model, self.model_path)
            else:
                logger.warning(f"Fine-tuned model not found at {self.model_path}, using base model")
                self.model = base_model
            
            self.model.eval()
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate_response(
        self, 
        user_input: str, 
        context: str = "", 
        max_length: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a response using the fine-tuned Herbie model
        
        Args:
            user_input: User's message
            context: Additional context (optional)
            max_length: Maximum response length
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            do_sample: Whether to use sampling
            
        Returns:
            Dict containing response, confidence, and metadata
        """
        try:
            # Format input as instruction following
            if context:
                prompt = f"<bos><start_of_turn>user\nYou are Herbie from Fantastic Four. Respond in character to this situation: {context}\n{user_input}<end_of_turn>\n<start_of_turn>model\n"
            else:
                prompt = f"<bos><start_of_turn>user\nYou are Herbie from Fantastic Four. Respond in character to: {user_input}<end_of_turn>\n<start_of_turn>model\n"
            
            # Tokenize input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=len(inputs[0]) + max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=do_sample,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            # Decode response
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            
            # Extract just the model's response
            response_start = full_response.find("<start_of_turn>model\n") + len("<start_of_turn>model\n")
            response_end = full_response.find("<end_of_turn>", response_start)
            
            if response_end == -1:
                response = full_response[response_start:].strip()
            else:
                response = full_response[response_start:response_end].strip()
            
            # Determine emotion based on response content
            emotion = self._classify_emotion(response)
            
            return {
                "response": response,
                "emotion": emotion,
                "confidence": 0.9,  # High confidence for fine-tuned model
                "model_used": "herbie-gemma-3b"
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "Herbie is experiencing technical difficulties! Please try again!",
                "emotion": "confused",
                "confidence": 0.1,
                "model_used": "fallback"
            }
    
    def _classify_emotion(self, response: str) -> str:
        """Simple emotion classification based on response content"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ["alert", "danger", "warning", "emergency"]):
            return "urgent"
        elif any(word in response_lower for word in ["greetings", "hello", "pleased", "salutations"]):
            return "friendly"
        elif any(word in response_lower for word in ["help", "assist", "ready", "available"]):
            return "helpful"
        elif any(word in response_lower for word in ["fear", "worry", "concern"]):
            return "concerned"
        elif any(word in response_lower for word in ["processing", "analyzing", "computing"]):
            return "thoughtful"
        else:
            return "neutral"
    
    def is_model_ready(self) -> bool:
        """Check if the model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None