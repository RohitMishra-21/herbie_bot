# Herbie Gemma 3B Fine-tuning Guide

This guide walks you through fine-tuning a Gemma 3B model on Herbie chatbot data and integrating it into your project.

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended) with at least 8GB VRAM
- At least 16GB system RAM

## Setup

### 1. Install Dependencies

```bash
# Install fine-tuning specific requirements
pip install -r requirements_finetuning.txt

# Verify PyTorch CUDA installation
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 2. Prepare Training Data

Your training data is already prepared in `data/training/herbie_training.jsonl`. Each line contains:
```json
{
  "instruction": "You are Herbie from Fantastic Four. Respond in character to this situation: greeting",
  "input": "Core Herbie personality quote",
  "output": "Hello! Herbie is online and ready to assist the Fantastic Four!"
}
```

## Fine-tuning Process

### Option 1: Using the Training Script (Recommended)

```bash
# Make script executable (Linux/Mac)
chmod +x scripts/train.sh

# Run fine-tuning
./scripts/train.sh
```

### Option 2: Manual Fine-tuning

```bash
python scripts/fine_tune_gemma.py \
    --data_path data/training/herbie_training.jsonl \
    --output_dir models/fine_tuned/herbie-gemma-3b \
    --base_model google/gemma-2b-it \
    --epochs 5 \
    --batch_size 2 \
    --learning_rate 2e-4 \
    --max_length 512
```

### Training Parameters Explained

- **epochs**: Number of training cycles (3-5 recommended for small dataset)
- **batch_size**: Adjust based on GPU memory (2 for 8GB VRAM)
- **learning_rate**: 2e-4 is optimal for LoRA fine-tuning
- **max_length**: Maximum sequence length (512 for good context)

## Testing the Model

### 1. Test the Fine-tuned Model

```bash
python scripts/test_model.py
```

### 2. Start the API Server

```bash
# Start the backend server
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Check Model Status

Visit: http://localhost:8000/model/status

Expected response for successful fine-tuning:
```json
{
  "status": "ready",
  "model_path": "models/fine_tuned/herbie-gemma-3b",
  "model_type": "herbie-gemma-3b"
}
```

## API Usage

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello Herbie!",
    "context": "greeting",
    "temperature": 0.7,
    "max_length": 256
  }'
```

Response:
```json
{
  "response": "Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics!",
  "emotion": "friendly",
  "confidence": 0.9,
  "model_used": "herbie-gemma-3b"
}
```

## Project Structure

```
herbie-chatbot/
├── data/
│   └── training/
│       └── herbie_training.jsonl     # Training data
├── models/
│   ├── fine_tuned/
│   │   └── herbie-gemma-3b/         # Fine-tuned model output
│   └── base_models/                 # Base model cache
├── backend/
│   └── app/
│       ├── main.py                  # Updated API server
│       └── models/
│           └── gemma_model.py       # Gemma model wrapper
├── scripts/
│   ├── fine_tune_gemma.py          # Fine-tuning script
│   ├── test_model.py               # Model testing script
│   └── train.sh                    # Training wrapper
└── requirements_finetuning.txt     # Fine-tuning dependencies
```

## Troubleshooting

### GPU Memory Issues
- Reduce `batch_size` to 1
- Enable gradient checkpointing
- Use smaller `max_length`

### CUDA Not Available
- Install PyTorch with CUDA support:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

### Model Loading Fails
- Check if fine-tuned model exists in `models/fine_tuned/herbie-gemma-3b/`
- API will fall back to rule-based responses if model isn't available
- Check logs for detailed error messages

### Low Quality Responses
- Increase training epochs
- Add more diverse training data
- Adjust temperature and top_p parameters

## Performance Optimization

### For Better Responses
1. **Add More Training Data**: Expand `herbie_training.jsonl` with more examples
2. **Balanced Dataset**: Ensure good coverage of different scenarios
3. **Quality Control**: Review and improve existing training examples

### For Faster Inference
1. **Model Quantization**: Already using 4-bit quantization
2. **Batch Processing**: Process multiple requests together
3. **Model Caching**: Keep model in memory between requests

## Adding New Training Data

1. Add entries to `data/training/herbie_training.jsonl`:
   ```json
   {"instruction": "You are Herbie from Fantastic Four. Respond in character to this situation: [scenario]", "input": "[context]", "output": "[herbie_response]"}
   ```

2. Re-run fine-tuning:
   ```bash
   ./scripts/train.sh
   ```

3. Restart the API server to load the new model

## Integration with Frontend

The frontend in `frontend/` is already set up to work with the updated API. The chat interface will automatically use the fine-tuned model when available.

## Next Steps

1. **Expand Training Data**: Add more diverse Herbie scenarios
2. **Implement RAG**: Add retrieval-augmented generation for better context
3. **Add Voice Synthesis**: Integrate text-to-speech for Herbie's voice
4. **Model Monitoring**: Add logging and monitoring for model performance
5. **A/B Testing**: Compare fine-tuned vs. rule-based responses

## Support

For issues with fine-tuning or integration, check:
1. GPU memory and CUDA installation
2. Model file permissions and paths
3. API server logs for detailed error messages
4. Training data format and quality

Quick Start:

  1. Install dependencies:
  cd C:\Users\Administrator\Documents\ML\herbie_project\herbie-chatbot
  pip install -r requirements_finetuning.txt
  2. Run fine-tuning:
  python scripts/fine_tune_gemma.py --data_path data/training/herbie_training.jsonl --output_dir models/fine_tuned/herbie-gemma-3b --epochs 5
  3. Test the model:
  python scripts/test_model.py
  4. Start the API:
  cd backend
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000