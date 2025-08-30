# Herbie Chatbot

A conversational AI chatbot inspired by Herbie the Love Bug, bringing the beloved character's personality to life through modern AI technology.

## Project Structure

```
herbie-chatbot/
├── data/
│   ├── raw/                # Original character data and quotes
│   ├── processed/          # Cleaned and formatted training data
│   ├── training/           # Training datasets
│   └── embeddings/         # Vector embeddings
├── scripts/
│   ├── data_collection/    # Data gathering scripts
│   ├── data_processing/    # Data cleaning and preparation
│   └── validation/         # Data quality checks
├── models/
│   ├── base_models/        # Pre-trained model downloads
│   ├── fine_tuned/         # Custom trained models
│   ├── configs/            # Model configurations
│   └── checkpoints/        # Training checkpoints
├── backend/
│   ├── app/
│   │   ├── models/         # Data models
│   │   ├── api/            # API endpoints
│   │   └── utils/          # Utility functions
│   └── tests/              # Backend tests
├── frontend/
│   ├── public/
│   │   └── sounds/         # Herbie sound effects
│   └── src/
│       ├── components/     # React components
│       ├── styles/         # CSS/styling
│       └── utils/          # Frontend utilities
├── deployment/
│   ├── firebase/
│   │   └── functions/      # Cloud functions
│   ├── docker/             # Docker configurations
│   └── scripts/            # Deployment scripts
└── docs/                   # Documentation
```

## Features

- **Character-accurate responses** based on Herbie's personality
- **Interactive chat interface** with sound effects
- **Voice interaction** capabilities
- **Responsive design** for multiple devices
- **Real-time conversation** with context awareness

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
cd frontend && npm install
```

2. Set up the backend:
```bash
cd backend && python app/main.py
```

3. Start the frontend:
```bash
cd frontend && npm start
```

## Development

- Backend: Python/FastAPI
- Frontend: React/JavaScript
- AI: Fine-tuned language model
- Deployment: Firebase/Docker

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request