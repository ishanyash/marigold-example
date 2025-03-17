# evaluation/evaluators.py

from langchain.evaluation import EvaluatorType
from langchain.evaluation.schema import StringEvaluator
from langchain.smith import RunEvaluator
from langchain_core.outputs import LLMResult
from langchain_openai import OpenAI

import json
import re
from typing import Dict, List, Any, Optional, Union

from config.settings import OPENAI_API_KEY, EVALUATION_MODEL
from evaluation.metrics import (
    calculate_engagement_score,
    calculate_conversion_potential_score,
    calculate_brand_alignment_score
)
from utils.logger import get_logger

logger = get_logger(__name__)

class EmailContentEvaluator(RunEvaluator):
    """
    Custom evaluator for assessing email marketing content quality.
    Used with LangSmith to evaluate model outputs systematically.
    """
    
    def __init__(self):
        self.eval_llm = OpenAI(model_name=EVALUATION_MODEL, temperature=0)
    
    def evaluate_run(self, run):
        """Evaluate a LangSmith run containing an email generation"""
        try:
            # Extract the generated email from the run
            if "final_email" in run.outputs:
                email_content = run.outputs["final_email"]
            else:
                # Fall back to the last output if final_email not found
                email_content = list(run.outputs.values())[-1]
            
            # Extract inputs for context
            customer_name = run.inputs.get("customer_name", "Customer")
            tariff_type = run.inputs.get("tariff_type", "Unknown")
            
            # Run all evaluations
            results = {}
            
            # Content quality evaluation
            results["content_quality"] = self._evaluate_content_quality(email_content)
            
            # Brand voice alignment
            results["brand_alignment"] = self._evaluate_brand_alignment(email_content)
            
            # Personalization assessment
            results["personalization"] = self._evaluate_personalization(
                email_content, customer_name, tariff_type
            )
            
            # Call-to-action strength
            results["cta_effectiveness"] = self._evaluate_cta(email_content)
            
            # Calculate aggregate scores
            results["engagement_score"] = calculate_engagement_score(results)
            results["conversion_potential"] = calculate_conversion_potential_score(results)
            results["brand_alignment_score"] = calculate_brand_alignment_score(results)
            
            # Calculate overall score
            results["overall_score"] = (
                results["engagement_score"] * 0.3 +
                results["conversion_potential"] * 0.4 +
                results["brand_alignment_score"] * 0.3
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in email evaluation: {str(e)}")
            return {"error": str(e), "overall_score": 0}
    
    def _evaluate_content_quality(self, email_content):
        """Evaluate the general quality of the email content"""
        prompt = f"""
        Evaluate the following marketing email content for an energy company.
        Rate each aspect on a scale of 1-10:
        
        EMAIL CONTENT:
        {email_content}
        
        EVALUATION CRITERIA:
        1. Clarity: Is the message clear and easy to understand?
        2. Conciseness: Is the content appropriately brief without unnecessary text?
        3. Grammar & Spelling: Is the text free of errors?
        4. Persuasiveness: Does the content make a compelling case?
        5. Readability: Is the content well-structured and easy to scan?
        
        Provide your ratings and brief explanations in JSON format:
        {{
            "clarity": {{score: X, reason: "explanation"}},
            "conciseness": {{score: X, reason: "explanation"}},
            "grammar": {{score: X, reason: "explanation"}},
            "persuasiveness": {{score: X, reason: "explanation"}},
            "readability": {{score: X, reason: "explanation"}},
            "overall_content_quality": X
        }}
        """
        
        result = self.eval_llm.invoke(prompt)
        return self._extract_json(result)
    
    def _evaluate_brand_alignment(self, email_content):
        """Evaluate how well the email aligns with Octopus Energy's brand voice"""
        prompt = f"""
        Evaluate how well this email aligns with Octopus Energy's brand voice guidelines.
        Rate each aspect on a scale of 1-10:
        
        OCTOPUS ENERGY BRAND VOICE:
        - Friendly and conversational
        - Clear and jargon-free
        - Helpful and transparent
        - Eco-conscious
        - Slightly quirky and different from traditional energy companies
        - Never overly formal, corporate, or aggressive
        
        EMAIL CONTENT:
        {email_content}
        
        EVALUATION CRITERIA:
        1. Tone Alignment: How well does the tone match Octopus Energy's friendly, conversational style?
        2. Language Clarity: Is the language clear, accessible, and jargon-free?
        3. Brand Personality: Does it convey helpfulness, transparency, and eco-consciousness?
        4. Distinctiveness: Does it stand out from generic corporate energy messaging?
        
        Provide your ratings and brief explanations in JSON format:
        {{
            "tone_alignment": {{score: X, reason: "explanation"}},
            "language_clarity": {{score: X, reason: "explanation"}},
            "brand_personality": {{score: X, reason: "explanation"}},
            "distinctiveness": {{score: X, reason: "explanation"}},
            "overall_brand_alignment": X
        }}
        """
        
        result = self.eval_llm.invoke(prompt)
        return self._extract_json(result)
    
    def _evaluate_personalization(self, email_content, customer_name, tariff_type):
        """Evaluate how well the email is personalized to the customer"""
        prompt = f"""
        Evaluate how effectively this email is personalized for the specific customer.
        
        CUSTOMER DETAILS:
        - Name: {customer_name}
        - Current Tariff: {tariff_type}
        
        EMAIL CONTENT:
        {email_content}
        
        EVALUATION CRITERIA (rate 1-10):
        1. Name Usage: How effectively is the customer's name incorporated?
        2. Tariff Relevance: How well does the email reference their current tariff?
        3. Specific Needs: Does the email address specific needs implied by their tariff type?
        4. Tailored Benefits: Are benefits framed in terms of this customer's situation?
        5. Personal Connection: Does the email establish a personal connection rather than feeling generic?
        
        Provide your ratings and brief explanations in JSON format:
        {{
            "name_usage": {{score: X, reason: "explanation"}},
            "tariff_relevance": {{score: X, reason: "explanation"}},
            "specific_needs": {{score: X, reason: "explanation"}},
            "tailored_benefits": {{score: X, reason: "explanation"}},
            "personal_connection": {{score: X, reason: "explanation"}},
            "overall_personalization": X
        }}
        """
        
        result = self.eval_llm.invoke(prompt)
        return self._extract_json(result)
    
    def _evaluate_cta(self, email_content):
        """Evaluate the effectiveness of the call-to-action"""
        prompt = f"""
        Evaluate the call-to-action (CTA) in this marketing email.
        
        EMAIL CONTENT:
        {email_content}
        
        EVALUATION CRITERIA (rate 1-10):
        1. Clarity: Is the CTA clear about what action to take?
        2. Prominence: Is the CTA easy to find and visually distinct?
        3. Persuasiveness: Does the CTA give a compelling reason to act?
        4. Urgency: Does the CTA create an appropriate sense of urgency?
        5. Value Proposition: Is the value of taking action clear in the CTA?
        
        Provide your ratings and brief explanations in JSON format:
        {{
            "clarity": {{score: X, reason: "explanation"}},
            "prominence": {{score: X, reason: "explanation"}},
            "persuasiveness": {{score: X, reason: "explanation"}},
            "urgency": {{score: X, reason: "explanation"}},
            "value_proposition": {{score: X, reason: "explanation"}},
            "overall_cta_effectiveness": X
        }}
        """
        
        result = self.eval_llm.invoke(prompt)
        return self._extract_json(result)
    
    def _extract_json(self, text):
        """Extract and parse JSON from LLM output"""
        try:
            # Find JSON object in text
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            return {"error": "No JSON found in response"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in response"}


# evaluation/metrics.py

"""
Metrics and scoring functions for evaluating email marketing content.
"""

def calculate_engagement_score(evaluation_results):
    """
    Calculate an engagement score based on content quality, personalization, and readability.
    
    Args:
        evaluation_results: Dict containing evaluation metrics
        
    Returns:
        float: Engagement score on a scale of 0-10
    """
    try:
        content_quality = evaluation_results["content_quality"]["overall_content_quality"]
        personalization = evaluation_results["personalization"]["overall_personalization"]
        readability = evaluation_results["content_quality"]["readability"]["score"]
        
        # Weighted score calculation
        engagement_score = (
            content_quality * 0.4 +
            personalization * 0.4 +
            readability * 0.2
        )
        
        return round(engagement_score, 1)
    except (KeyError, TypeError):
        return 5.0  # Default value if calculation fails

def calculate_conversion_potential_score(evaluation_results):
    """
    Calculate conversion potential based on persuasiveness, CTA effectiveness, and personalization.
    
    Args:
        evaluation_results: Dict containing evaluation metrics
        
    Returns:
        float: Conversion potential score on a scale of 0-10
    """
    try:
        persuasiveness = evaluation_results["content_quality"]["persuasiveness"]["score"]
        cta_effectiveness = evaluation_results["cta_effectiveness"]["overall_cta_effectiveness"]
        personalization = evaluation_results["personalization"]["overall_personalization"]
        
        # Weighted score calculation
        conversion_score = (
            persuasiveness * 0.3 +
            cta_effectiveness * 0.5 +
            personalization * 0.2
        )
        
        return round(conversion_score, 1)
    except (KeyError, TypeError):
        return 5.0  # Default value if calculation fails

def calculate_brand_alignment_score(evaluation_results):
    """
    Calculate how well the content aligns with Octopus Energy's brand voice.
    
    Args:
        evaluation_results: Dict containing evaluation metrics
        
    Returns:
        float: Brand alignment score on a scale of 0-10
    """
    try:
        tone_alignment = evaluation_results["brand_alignment"]["tone_alignment"]["score"]
        language_clarity = evaluation_results["brand_alignment"]["language_clarity"]["score"]
        brand_personality = evaluation_results["brand_alignment"]["brand_personality"]["score"]
        distinctiveness = evaluation_results["brand_alignment"]["distinctiveness"]["score"]
        
        # Weighted score calculation
        brand_score = (
            tone_alignment * 0.3 +
            language_clarity * 0.2 +
            brand_personality * 0.3 +
            distinctiveness * 0.2
        )
        
        return round(brand_score, 1)
    except (KeyError, TypeError):
        return 5.0  # Default value if calculation fails