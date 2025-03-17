# schemas/email.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class EmailCampaign(BaseModel):
    """
    Schema for email campaign output.
    Contains both the final email and metadata about its generation.
    """
    customer_id: str
    email_subject: str
    email_body: str
    customer_insights: Optional[str] = None
    draft_version: Optional[str] = None
    final_version: str
    model_used: str
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "C1234",
                "email_subject": "John, Save 15% on Your Energy Bills This Winter",
                "email_body": "Hi John,\n\nWe've noticed you're on our Standard Variable tariff...",
                "customer_insights": "John uses most energy in the evenings...",
                "draft_version": "Hi John,\n\nYou could save money by switching...",
                "final_version": "Hi John,\n\nWe've noticed you're on our Standard Variable tariff...",
                "model_used": "gpt-4",
                "created_at": "2023-01-01T12:00:00",
                "metadata": {
                    "generation_time_ms": 2450,
                    "token_count": 320
                }
            }
        }


# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
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
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4")
EVALUATION_MODEL = os.getenv("EVALUATION_MODEL", "gpt-3.5-turbo")

# Available Models
AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-3.5-turbo",
    "claude-3-opus",
    "claude-3-sonnet",
    "bedrock-anthropic.claude-3-sonnet",
    "bedrock-amazon.titan-text-express"
]

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# config/constants.py

"""
Constants used throughout the application.
"""

# Email campaign types
CAMPAIGN_TYPES = {
    "NEW_PLAN": "new_plan",
    "SEASONAL": "seasonal",
    "RETENTION": "retention",
    "WINBACK": "winback",
    "ECO_FOCUS": "eco_focus",
    "SMART_METER": "smart_meter"
}

# Tariff types
TARIFF_TYPES = [
    "Standard Variable",
    "Fixed Rate",
    "Economy 7",
    "Green Energy",
    "Agile",
    "Go",
    "Tracker"
]

# Plans
PLANS = [
    "Agile Octopus",
    "Super Green Octopus",
    "Octopus Go",
    "GreenFlex",
    "Octopus Tracker",
    "Flexible Octopus"
]

# Evaluation metrics
EVALUATION_METRICS = {
    "CONTENT_QUALITY": "content_quality",
    "BRAND_ALIGNMENT": "brand_alignment",
    "PERSONALIZATION": "personalization",
    "CTA_EFFECTIVENESS": "cta_effectiveness",
    "ENGAGEMENT_SCORE": "engagement_score",
    "CONVERSION_POTENTIAL": "conversion_potential"
}

# Target scores
TARGET_SCORES = {
    "overall_score": 8.0,
    "engagement_score": 7.5,
    "conversion_potential": 8.0,
    "brand_alignment_score": 8.5
}

# LangSmith tags
LANGSMITH_TAGS = {
    "PRODUCTION": "production",
    "TESTING": "testing",
    "EVALUATION": "evaluation",
    "PROMPT_TESTING": "prompt_testing",
    "MODEL_COMPARISON": "model_comparison"
}


# utils/logger.py

import logging
import os
from config.settings import LOG_LEVEL

def get_logger(name):
    """
    Configure and return a logger instance.
    
    Args:
        name: Name of the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: Configured logger
    """
    # Set up logging
    logger = logging.getLogger(name)
    
    # Set log level from environment or default to INFO
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler if not already added
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger


# utils/helpers.py

import re
import json
from typing import Dict, List, Any, Optional

def extract_subject_line(email_text: str) -> str:
    """
    Extract the subject line from a generated email.
    
    Args:
        email_text: Full email text including subject line
        
    Returns:
        str: Extracted subject line, or default if not found
    """
    subject_pattern = r"Subject:([^\n]*)"
    match = re.search(subject_pattern, email_text)
    
    if match:
        return match.group(1).strip()
    return "Special Offer from Octopus Energy"  # Default subject

def parse_customer_data(customer_text: str) -> Dict[str, Any]:
    """
    Parse customer data from structured text input.
    
    Args:
        customer_text: Text containing customer information
        
    Returns:
        Dict: Parsed customer data
    """
    patterns = {
        "name": r"Name:?\s*([^\n,]+)",
        "tariff_type": r"Tariff:?\s*([^\n,]+)",
        "energy_usage": r"Usage:?\s*(\d+)\s*kWh",
        "location": r"Location:?\s*([^\n,]+)",
        "peak_usage_time": r"Peak(?:\s*usage)?(?:\s*time)?:?\s*([^\n,]+)"
    }
    
    result = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, customer_text, re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()
    
    # Convert energy usage to int if found
    if "energy_usage" in result:
        try:
            result["energy_usage"] = int(result["energy_usage"])
        except ValueError:
            pass
    
    return result

def format_email_for_display(email_body: str) -> str:
    """
    Format an email body for HTML display.
    
    Args:
        email_body: Raw email body text
        
    Returns:
        str: HTML-formatted email for display
    """
    # Replace newlines with HTML breaks
    formatted = email_body.replace('\n', '<br>')
    
    # Make bullet points into HTML lists
    bullet_pattern = r'(?:^|\n)[\s]*[•\-\*][\s]+(.+)'
    if re.search(bullet_pattern, email_body, re.MULTILINE):
        # Start list
        formatted = re.sub(r'(?:^|\n)[\s]*[•\-\*][\s]+', r'<ul><li>', formatted, count=1, flags=re.MULTILINE)
        # Middle items
        formatted = re.sub(r'(?:\n)[\s]*[•\-\*][\s]+', r'</li><li>', formatted)
        # End list
        bullet_end_pattern = r'</li><li>(.+?)(?=<br>|$)'
        match = re.search(bullet_end_pattern, formatted)
        if match:
            formatted = re.sub(bullet_end_pattern, r'</li><li>\1</li></ul>', formatted, count=1)
    
    # Highlight CTA in button-like style
    cta_patterns = [
        r'\[([^\]]+)\]',  # [Text in brackets]
        r'<\s*([^>]+)\s*>',  # <Text in angle brackets>
    ]
    
    for pattern in cta_patterns:
        formatted = re.sub(
            pattern,
            r'<div style="display:inline-block; background-color:#4c12a1; color:white; padding:8px 15px; border-radius:5px; margin:10px 0;">\1</div>',
            formatted
        )
    
    return formatted


# .env.example

"""
# LangChain Email Marketing Assistant Environment Variables

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here

# AWS Configuration (for Bedrock models)
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# LangSmith Configuration
LANGSMITH_PROJECT=octopus-email-marketing
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Model Settings
DEFAULT_MODEL=gpt-4
EVALUATION_MODEL=gpt-3.5-turbo

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
"""