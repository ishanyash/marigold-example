# orchestration/chains.py

from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.prompts import PromptTemplate
from typing import Dict, List, Any, Callable

from config.settings import DEMO_MODE
from prompts.email_templates import (
    EMAIL_ANALYSIS_TEMPLATE,
    EMAIL_GENERATION_TEMPLATE,
    EMAIL_REFINEMENT_TEMPLATE
)
from utils.logger import get_logger

logger = get_logger(__name__)

def create_analysis_chain(llm):
    """
    Create a chain for analyzing customer data.
    
    Args:
        llm: Language model to use for analysis
        
    Returns:
        LLMChain: Analysis chain
    """
    analysis_prompt = PromptTemplate(
        template=EMAIL_ANALYSIS_TEMPLATE,
        input_variables=["customer_name", "tariff_type", "energy_usage", 
                       "location", "peak_usage_time", "customer_history"]
    )
    
    return LLMChain(
        llm=llm,
        prompt=analysis_prompt,
        output_key="customer_insights",
        verbose=True
    )

def create_generation_chain(llm):
    """
    Create a chain for generating email drafts.
    
    Args:
        llm: Language model to use for generation
        
    Returns:
        LLMChain: Generation chain
    """
    generation_prompt = PromptTemplate(
        template=EMAIL_GENERATION_TEMPLATE,
        input_variables=["customer_name", "tariff_type", "energy_usage", 
                       "potential_savings", "recommended_plan", 
                       "location", "peak_usage_time", "customer_insights"]
    )
    
    return LLMChain(
        llm=llm,
        prompt=generation_prompt,
        output_key="email_draft",
        verbose=True
    )

def create_refinement_chain(llm):
    """
    Create a chain for refining and optimizing email drafts.
    
    Args:
        llm: Language model to use for refinement
        
    Returns:
        LLMChain: Refinement chain
    """
    refinement_prompt = PromptTemplate(
        template=EMAIL_REFINEMENT_TEMPLATE,
        input_variables=["email_draft", "customer_name", "tariff_type"]
    )
    
    return LLMChain(
        llm=llm,
        prompt=refinement_prompt,
        output_key="final_email",
        verbose=True
    )

def create_subject_extraction_chain():
    """
    Create a chain for extracting the subject line from a generated email.
    
    Returns:
        TransformChain: Subject extraction chain
    """
    def extract_subject(inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Extract subject line from email text"""
        email_text = inputs.get("final_email", "")
        
        if "Subject:" in email_text:
            subject = email_text.split("Subject:")[1].split("\n")[0].strip()
        else:
            # Default subject if none found
            customer_name = inputs.get("customer_name", "Customer")
            subject = f"Special Offer for {customer_name} from Octopus Energy"
        
        return {"email_subject": subject}
    
    return TransformChain(
        input_variables=["final_email", "customer_name"],
        output_variables=["email_subject"],
        transform=extract_subject
    )

def create_email_campaign_chain(llm):
    """
    Create the complete email campaign generation chain.
    
    Args:
        llm: Language model to use for the chain
        
    Returns:
        SequentialChain: Complete email campaign chain
    """
    # Create the individual chains
    analysis_chain = create_analysis_chain(llm)
    generation_chain = create_generation_chain(llm)
    refinement_chain = create_refinement_chain(llm)
    subject_extraction_chain = create_subject_extraction_chain()
    
    # Create the sequential chain
    return SequentialChain(
        chains=[
            analysis_chain,
            generation_chain,
            refinement_chain,
            subject_extraction_chain
        ],
        input_variables=[
            "customer_name",
            "tariff_type",
            "energy_usage",
            "potential_savings",
            "recommended_plan",
            "location",
            "peak_usage_time",
            "customer_history"
        ],
        output_variables=[
            "customer_insights",
            "email_draft",
            "final_email",
            "email_subject"
        ],
        verbose=True
    )

def create_email_analysis_only_chain(llm):
    """
    Create a chain that only performs customer data analysis.
    
    Args:
        llm: Language model to use for analysis
        
    Returns:
        LLMChain: Analysis-only chain
    """
    return create_analysis_chain(llm)

def create_email_refinement_only_chain(llm):
    """
    Create a chain that only performs email refinement.
    
    Args:
        llm: Language model to use for refinement
        
    Returns:
        SequentialChain: Refinement chain with subject extraction
    """
    refinement_chain = create_refinement_chain(llm)
    subject_extraction_chain = create_subject_extraction_chain()
    
    return SequentialChain(
        chains=[refinement_chain, subject_extraction_chain],
        input_variables=["email_draft", "customer_name", "tariff_type"],
        output_variables=["final_email", "email_subject"],
        verbose=True
    )