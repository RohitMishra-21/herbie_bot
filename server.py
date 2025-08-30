#!/usr/bin/env python3
"""
Simple Herbie API server for Ollama integration
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
import requests
import json
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Herbie Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://herbie-8d4b4.web.app", 
        "https://herbie-8d4b4.firebaseapp.com",
        "https://actress-programs-commonly-threshold.trycloudflare.com",
        "*"  # Allow all origins for public access
    ],
    allow_credentials=False,  # Disable credentials for better CORS compatibility
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Mx-ReqToken",
        "Keep-Alive",
        "X-Requested-With",
        "If-Modified-Since"
    ],
    expose_headers=["*"],
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
    model_used: Optional[str] = "herbie-gemma3:4b"

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
FINETUNED_MODEL = "herbie-gemma3:4b"
BASE_MODEL = "gemma3:4b"

def get_available_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        return []
    except:
        return []

def classify_emotion(response: str) -> str:
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

def generate_ollama_response(user_input: str, context: str = "", temperature: float = 0.7, model: str = FINETUNED_MODEL):
    """Generate response using Ollama"""
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
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 256,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        # Make request to Ollama
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
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
            emotion = classify_emotion(generated_text)
            
            return {
                "response": generated_text,
                "emotion": emotion,
                "confidence": 0.9,
                "model_used": model
            }
        else:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            raise Exception(f"Ollama API returned status {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error generating response with Ollama: {e}")
        return None

# Fallback responses
FALLBACK_RESPONSES = [
    {"dialogue": "Herbie is online and ready to assist!", "emotion": "helpful"},
    {"dialogue": "Greetings! How may Herbie help you?", "emotion": "friendly"},
    {"dialogue": "Alert! Herbie is processing your request!", "emotion": "thoughtful"}
]

@app.get("/")
async def root():
    return {
        "message": "Herbie is online! 🤖", 
        "model": FINETUNED_MODEL,
        "status": "ready",
        "timestamp": "2025-01-08T12:00:00Z"
    }

# Add CORS preflight handlers
@app.options("/{full_path:path}")
async def options_handler(request: Request):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",
        }
    )

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
    available_models = get_available_models()
    
    if FINETUNED_MODEL in available_models:
        return {
            "status": "ready",
            "current_model": FINETUNED_MODEL,
            "model_type": "ollama",
            "available_models": available_models,
            "ollama_url": OLLAMA_BASE_URL
        }
    elif BASE_MODEL in available_models:
        return {
            "status": "base_available",
            "current_model": BASE_MODEL,
            "model_type": "ollama",
            "available_models": available_models,
            "ollama_url": OLLAMA_BASE_URL
        }
    else:
        return {
            "status": "fallback",
            "current_model": None,
            "model_type": "rule-based",
            "available_models": available_models,
            "ollama_url": OLLAMA_BASE_URL
        }

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: ChatMessage):
    """Generate chat response using Ollama or fallback"""
    try:
        # Try fine-tuned model first
        result = generate_ollama_response(
            user_input=msg.message,
            context=msg.context,
            temperature=msg.temperature,
            model=FINETUNED_MODEL
        )
        
        if result:
            logger.info(f"Using {FINETUNED_MODEL} for: {msg.message[:50]}...")
            return ChatResponse(**result)
        
        # Try base model
        result = generate_ollama_response(
            user_input=msg.message,
            context=msg.context,
            temperature=msg.temperature,
            model=BASE_MODEL
        )
        
        if result:
            logger.info(f"Using {BASE_MODEL} for: {msg.message[:50]}...")
            return ChatResponse(**result)
        
        # Fallback to simple responses
        logger.info("Using fallback responses")
        chosen = random.choice(FALLBACK_RESPONSES)
        return ChatResponse(
            response=chosen['dialogue'],
            emotion=chosen['emotion'],
            confidence=0.5,
            model_used="fallback"
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response="Herbie is experiencing technical difficulties! Please try again!",
            emotion="confused",
            confidence=0.1,
            model_used="error"
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting Herbie Chatbot API Server...")
    print("Backend: http://localhost:8000")
    print("Model Status: http://localhost:8000/model/status")
    print("Chat Endpoint: http://localhost:8000/chat")
    uvicorn.run(app, host="0.0.0.0", port=8000)