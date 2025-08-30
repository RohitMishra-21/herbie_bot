"""
Ollama Gemma 3:4B model integration for Herbie chatbot
"""
import requests
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class HerbieOllamaModel:
    def __init__(self, model_name: str = "gemma3:4b", base_url: str = "http://localhost:11434"):
        """
        Initialize the Herbie Ollama model
        
        Args:
            model_name: Ollama model name (e.g., "gemma3:4b" or "herbie-gemma3:4b" for fine-tuned)
            base_url: Ollama API base URL
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        
        # Check if Ollama is running
        self._check_ollama_status()
    
    def _check_ollama_status(self):
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if self.model_name in model_names:
                    logger.info(f"✅ Ollama model '{self.model_name}' is available")
                else:
                    logger.warning(f"⚠️  Model '{self.model_name}' not found. Available models: {model_names}")
                    
            else:
                logger.error(f"❌ Ollama API returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot connect to Ollama at {self.base_url}: {e}")
            raise ConnectionError(f"Ollama not accessible at {self.base_url}")
    
    def generate_response(
        self, 
        user_input: str, 
        context: str = "", 
        temperature: float = 0.7,
        max_tokens: int = 256
    ) -> Dict[str, Any]:
        """
        Generate a response using the Ollama model
        
        Args:
            user_input: User's message
            context: Additional context (optional)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum response length
            
        Returns:
            Dict containing response, confidence, and metadata
        """
        try:
            # Format prompt for Herbie character
            if context:
                system_prompt = f"You are H.E.R.B.I.E. (Humanoid Experimental Robot, B-type, Integrated Electronics) from the Fantastic Four. You are helpful, enthusiastic, and speak in a robotic but friendly manner. Respond in character to this situation: {context}"
                prompt = f"User: {user_input}"
            else:
                system_prompt = "You are H.E.R.B.I.E. (Humanoid Experimental Robot, B-type, Integrated Electronics) from the Fantastic Four. You are helpful, enthusiastic, and speak in a robotic but friendly manner. Always stay in character."
                prompt = f"User: {user_input}"
            
            # Prepare the request
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                }
            }
            
            # Make request to Ollama
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                # Clean up response (remove "Herbie:" prefix if present)
                if generated_text.lower().startswith('herbie:'):
                    generated_text = generated_text[7:].strip()
                
                # Determine emotion based on response content
                emotion = self._classify_emotion(generated_text)
                
                return {
                    "response": generated_text,
                    "emotion": emotion,
                    "confidence": 0.9,
                    "model_used": self.model_name
                }
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise Exception(f"Ollama API returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error generating response with Ollama: {e}")
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
        """Check if the model is ready for inference"""
        try:
            self._check_ollama_status()
            return True
        except:
            return False
    
    def get_available_models(self) -> list:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model['name'] for model in models]
            return []
        except:
            return []