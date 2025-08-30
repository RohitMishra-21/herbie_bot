#!/bin/bash
# Fine-tune Herbie Gemma 3B model

echo "Starting Herbie Gemma 3B fine-tuning..."

# Create necessary directories
mkdir -p models/fine_tuned
mkdir -p logs

# Install requirements
echo "Installing fine-tuning requirements..."
pip install -r requirements_finetuning.txt

# Run fine-tuning
echo "Running fine-tuning script..."
python scripts/fine_tune_gemma.py \
    --data_path data/training/herbie_training.jsonl \
    --output_dir models/fine_tuned/herbie-gemma-3b \
    --base_model google/gemma-2b-it \
    --epochs 5 \
    --batch_size 2 \
    --learning_rate 2e-4 \
    --max_length 512

echo "Fine-tuning completed!"
echo "Model saved to: models/fine_tuned/herbie-gemma-3b"
echo ""
echo "To test the model, run:"
echo "python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"