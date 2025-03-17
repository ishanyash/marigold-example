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