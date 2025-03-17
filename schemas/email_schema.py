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
                    "token_count": 320,
                    "prompt_tokens": 520,
                    "completion_tokens": 320
                }
            }
        }

class EmailTemplate(BaseModel):
    """
    Schema for email templates that can be reused.
    """
    template_id: str
    name: str
    description: str
    template_type: str  # e.g., "new_plan", "seasonal", "retention"
    subject_template: str
    body_template: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    tags: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "template_id": "template_001",
                "name": "Winter Energy Savings",
                "description": "Template for winter energy saving campaigns",
                "template_type": "seasonal",
                "subject_template": "{customer_name}, Stay Warm & Save {potential_savings}% This Winter",
                "body_template": "Hi {customer_name},\n\nAs temperatures drop...",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-15T09:30:00",
                "tags": ["winter", "savings", "seasonal"]
            }
        }

class EmailPerformanceMetrics(BaseModel):
    """
    Schema for tracking email performance metrics.
    Would be used in a real implementation to evaluate email effectiveness.
    """
    campaign_id: str
    email_id: str
    customer_id: str
    sent_at: datetime
    opened: bool = False
    opened_at: Optional[datetime] = None
    clicked: bool = False
    clicked_at: Optional[datetime] = None
    converted: bool = False
    converted_at: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "campaign_id": "campaign_winter_2023",
                "email_id": "email_12345",
                "customer_id": "C1234",
                "sent_at": "2023-01-10T09:00:00",
                "opened": True,
                "opened_at": "2023-01-10T10:15:00",
                "clicked": True,
                "clicked_at": "2023-01-10T10:16:30",
                "converted": True,
                "converted_at": "2023-01-10T14:22:15"
            }
        }