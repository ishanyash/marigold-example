
# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (will be empty in demo mode)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# LangSmith Configuration
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "octopus-email-marketing")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# Model Settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mock-gpt-4")
EVALUATION_MODEL = os.getenv("EVALUATION_MODEL", "mock-gpt-3.5-turbo")

# Available Models
AVAILABLE_MODELS = [
    "mock-gpt-4",
    "mock-gpt-3.5-turbo",
    "mock-claude-3-opus",
    "mock-claude-3-sonnet",
    "mock-bedrock-anthropic.claude-3-sonnet",
    "mock-bedrock-amazon.titan-text-express"
]

# Flag to determine if we're running in demo mode without APIs
DEMO_MODE = True

# Application Settings
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Automatically select the best model based on performance data
# In demo mode, this always returns mock-gpt-4
def select_production_model():
    """
    Select the best model for production use based on comparison data.
    In demo mode, returns the default mock model.
    """
    if DEMO_MODE:
        return "mock-gpt-4"
    
    try:
        # Try to load saved comparison results
        with open('./data/model_comparison_results.json', 'r') as f:
            import json
            comparison_data = json.load(f)
        
        if 'best_model' in comparison_data:
            return comparison_data['best_model']
        else:
            return DEFAULT_MODEL
    except:
        # Fallback if file doesn't exist or can't be read
        return DEFAULT_MODEL