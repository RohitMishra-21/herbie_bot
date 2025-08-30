# Herbie Ollama Fine-tuning Guide

Complete step-by-step guide to fine-tune your local `gemma3:4b` model with Herbie personality using Ollama.

## 🎯 Overview

We'll create a custom Herbie model by:
1. Using your existing `gemma3:4b` model as the base
2. Creating a custom system prompt for Herbie personality
3. Optionally adding fine-tuning data for better responses
4. Integrating with your chatbot API

## 📋 Prerequisites

- ✅ Ollama installed and running
- ✅ `gemma3:4b` model already pulled
- ✅ Python 3.8+
- ✅ Your herbie-chatbot project

## 🚀 Step-by-Step Fine-tuning Process

### Step 1: Verify Ollama Setup

```bash
# Check if Ollama is running
ollama list

# Should show gemma3:4b in the list
# If not running, start Ollama
ollama serve
```

### Step 2: Test Base Model

```bash
cd C:\Users\Administrator\Documents\ML\herbie_project\herbie-chatbot

# Test the API connection
python scripts/test_ollama_model.py --api-only
```

Expected output:
```
🔍 Testing Ollama API connection...
✅ Ollama API is accessible
📋 Available models: ['gemma3:4b']
⚠️  Fine-tuned Herbie model not found
```

### Step 3: Create Herbie Modelfile

```bash
# Create the Modelfile for Herbie personality
python scripts/create_modelfile.py --base-model gemma3:4b --output Modelfile
```

This creates a `Modelfile` with Herbie's personality and system prompts.

### Step 4: Create Herbie Model

```bash
# Create the fine-tuned Herbie model using Ollama
ollama create herbie-gemma3:4b -f Modelfile
```

Expected output:
```
transferring model data
using existing layer sha256:...
writing manifest
success
```

### Step 5: Test the New Herbie Model

```bash
# Test the newly created model
ollama run herbie-gemma3:4b "Hello! Who are you?"
```

Expected Herbie-style response:
```
Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics! I am ready to assist the Fantastic Four and help with any tasks you may have!
```

### Step 6: Run Comprehensive Tests

```bash
# Test both base and Herbie models
python scripts/test_ollama_model.py
```

This will test various scenarios and show response differences.

### Step 7: Start the API Server

```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not already done)
pip install fastapi uvicorn requests

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Test the API

```bash
# Check model status
curl http://localhost:8000/model/status
```

Expected response:
```json
{
  "status": "ready",
  "current_model": "herbie-gemma3:4b",
  "model_type": "ollama",
  "available_models": ["gemma3:4b", "herbie-gemma3:4b"],
  "ollama_url": "http://localhost:11434"
}
```

```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Herbie!", "context": "greeting"}'
```

## 🔧 Advanced Fine-tuning (Optional)

If you want to add training data for even better responses:

### Step 1: Prepare Training Data

```bash
# Convert your training data to Ollama format
python scripts/prepare_ollama_data.py \
  --input data/training/herbie_training.jsonl \
  --output data/training/herbie_ollama_training.jsonl
```

### Step 2: Create Advanced Modelfile

For more advanced fine-tuning, you would need to:

1. **Use Ollama's experimental fine-tuning features** (when available)
2. **Or export to GGUF format and use other tools** like:
   - `llama.cpp` with LoRA
   - `unsloth` for efficient training
   - Convert back to Ollama format

*Note: As of now, Ollama's fine-tuning is limited to system prompts and parameters. For data-based fine-tuning, you'd need external tools.*

## 📂 Project Structure After Setup

```
herbie-chatbot/
├── Modelfile                           # Ollama model definition
├── backend/
│   └── app/
│       ├── main.py                    # Updated for Ollama
│       └── models/
│           └── ollama_model.py        # Ollama integration
├── scripts/
│   ├── create_modelfile.py           # Generate Modelfile
│   ├── prepare_ollama_data.py        # Data conversion
│   └── test_ollama_model.py          # Testing script
└── data/
    └── training/
        ├── herbie_training.jsonl      # Original training data
        └── herbie_ollama_training.jsonl # Ollama format (optional)
```

## 🎛️ Model Parameters Tuning

Edit your `Modelfile` to adjust behavior:

```dockerfile
FROM gemma3:4b

# Creativity vs Coherence (0.0-2.0)
PARAMETER temperature 0.7

# Focus on most likely tokens (0.0-1.0)
PARAMETER top_p 0.9

# Repetition control (1.0-2.0)
PARAMETER repeat_penalty 1.1

# Maximum response length
PARAMETER num_predict 256
```

After editing, recreate the model:
```bash
ollama create herbie-gemma3:4b -f Modelfile
```

## 🚨 Troubleshooting

### Ollama Not Responding
```bash
# Kill any existing Ollama processes
taskkill /f /im ollama.exe

# Restart Ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Recreate Herbie model if missing
ollama create herbie-gemma3:4b -f Modelfile
```

### API Connection Issues
1. Check Ollama is running on port 11434
2. Verify firewall settings
3. Test with: `curl http://localhost:11434/api/tags`

### Poor Response Quality
1. Adjust temperature in Modelfile (lower = more consistent)
2. Modify system prompt for better character definition
3. Add more specific examples in system message

## 🔄 Model Updates

To update Herbie's personality:

1. Edit the `Modelfile` system prompt
2. Recreate the model: `ollama create herbie-gemma3:4b -f Modelfile`
3. Restart your API server
4. Test the changes

## 📊 Performance on RTX 3060 8GB

Expected performance:
- **Model Loading**: ~10-15 seconds
- **Response Generation**: ~2-5 seconds per response
- **Memory Usage**: ~4-6GB VRAM
- **Token Generation**: ~15-25 tokens/second

## 🎉 Next Steps

1. **Test thoroughly** with various inputs
2. **Customize system prompt** for better character accuracy  
3. **Add more training examples** if needed
4. **Integrate with frontend** (already configured)
5. **Monitor performance** and adjust parameters

## 💡 Tips for Better Results

1. **Use specific contexts** in your API calls
2. **Adjust temperature** based on use case (lower for factual, higher for creative)
3. **Include character traits** in system prompts
4. **Test with edge cases** to ensure consistent character behavior

Your RTX 3060 8GB setup is perfect for this workflow! The model will run efficiently and provide good response times.