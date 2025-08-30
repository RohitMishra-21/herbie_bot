from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import random
import logging
import os
from pathlib import Path
from app.models.ollama_model import HerbieOllamaModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Herbie Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = ""
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256

class ChatResponse(BaseModel):
    response: str
    emotion: str
    confidence: float
    model_used: Optional[str] = "gemma3:4b"

# Initialize the Ollama model
# Try fine-tuned model first, fall back to base model
FINETUNED_MODEL = "herbie-gemma3:4b"  # After fine-tuning
BASE_MODEL = "gemma3:4b"  # Your current model

try:
    logger.info("Trying to load fine-tuned Herbie model...")
    herbie_model = HerbieOllamaModel(FINETUNED_MODEL)
    logger.info("Fine-tuned model loaded successfully!")
except Exception as e:
    logger.info(f"Fine-tuned model not available ({e}), using base model...")
    try:
        herbie_model = HerbieOllamaModel(BASE_MODEL)
        logger.info("Base Gemma3:4b model loaded successfully!")
    except Exception as e2:
        logger.error(f"Failed to load any Ollama model: {e2}")
        herbie_model = None

# Load dataset for responses (fallback)
try:
    with open("data/processed/herbie_dataset.json", 'r') as f:
        herbie_quotes = json.load(f)
except:
    herbie_quotes = [
        {"dialogue": "Herbie is online and ready to assist!", "emotion": "helpful"},
        {"dialogue": "Greetings! How may Herbie help you?", "emotion": "friendly"}
    ]

@app.get("/")
async def root():
    return {"message": "Herbie is online! 🤖"}

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "herbie-chatbot",
                "object": "model",
                "created": 1677610602,
                "owned_by": "herbie",
                "permission": [],
                "root": "herbie-chatbot",
                "parent": None
            }
        ]
    }

@app.get("/model/status")
async def model_status():
    """Check if the Ollama model is available"""
    if herbie_model and herbie_model.is_model_ready():
        available_models = herbie_model.get_available_models()
        return {
            "status": "ready",
            "current_model": herbie_model.model_name,
            "model_type": "ollama",
            "available_models": available_models,
            "ollama_url": herbie_model.base_url
        }
    else:
        return {
            "status": "fallback",
            "current_model": None,
            "model_type": "rule-based",
            "available_models": [],
            "ollama_url": "http://localhost:11434"
        }

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: ChatMessage):
    """Generate chat response using fine-tuned Gemma model or fallback"""
    try:
        # Try to use Ollama model first
        if herbie_model and herbie_model.is_model_ready():
            logger.info(f"Using Ollama model for: {msg.message[:50]}...")
            result = herbie_model.generate_response(
                user_input=msg.message,
                context=msg.context,
                temperature=msg.temperature,
                max_tokens=msg.max_tokens
            )
            return ChatResponse(**result)
        
        else:
            # Fallback to rule-based responses
            logger.info("Using fallback rule-based responses")
            return _fallback_response(msg)
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return _fallback_response(msg)

def _fallback_response(msg: ChatMessage) -> ChatResponse:
    """Fallback rule-based response system"""
    if "hello" in msg.message.lower() or "hi" in msg.message.lower():
        response_quotes = [q for q in herbie_quotes if q.get('situation') == 'introduction' or q.get('emotion') == 'friendly']
    elif "help" in msg.message.lower():
        response_quotes = [q for q in herbie_quotes if q.get('emotion') == 'helpful']
    elif "danger" in msg.message.lower() or "alert" in msg.message.lower():
        response_quotes = [q for q in herbie_quotes if q.get('emotion') == 'urgent']
    else:
        response_quotes = herbie_quotes
    
    if response_quotes:
        chosen = random.choice(response_quotes)
        return ChatResponse(
            response=chosen['dialogue'],
            emotion=chosen.get('emotion', 'neutral'),
            confidence=0.85,
            model_used="fallback"
        )
    
    return ChatResponse(
        response="Herbie is processing your request!",
        emotion="thoughtful",
        confidence=0.7,
        model_used="fallback"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)