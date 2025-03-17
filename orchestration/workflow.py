# orchestration/workflow.py

from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain_core.tracers import LangChainTracer
from langchain.prompts import PromptTemplate
import langsmith
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import BedrockChat

from config.settings import LANGSMITH_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, AWS_REGION
from prompts.email_templates import (
    EMAIL_ANALYSIS_TEMPLATE,
    EMAIL_GENERATION_TEMPLATE,
    EMAIL_REFINEMENT_TEMPLATE
)
from schemas.customer import CustomerProfile
from schemas.email import EmailCampaign
from utils.logger import get_logger

logger = get_logger(__name__)

class EmailCampaignWorkflow:
    """
    Orchestrates the entire email campaign generation workflow using LangChain.
    The workflow consists of three main stages:
    1. Customer Data Analysis
    2. Email Draft Generation
    3. Email Refinement and Optimization
    """
    
    def __init__(self, model_name="gpt-4", trace_name="octopus-email-campaign"):
        self.trace_name = trace_name
        self.model_name = model_name
        self.tracer = LangChainTracer(project_name=trace_name)
        
        # Initialize the appropriate LLM based on model_name
        self.llm = self._initialize_llm(model_name)
        
        # Set up conversation memory
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Build the individual chains
        self.analysis_chain = self._build_analysis_chain()
        self.generation_chain = self._build_generation_chain()
        self.refinement_chain = self._build_refinement_chain()
        
        # Build the sequential workflow
        self.workflow = self._build_workflow()
    
    def _initialize_llm(self, model_name):
        """Initialize the appropriate LLM based on model_name"""
        # DEMO MODE: Use mock LLM instead of actual API calls
        from utils.mock_llm import MockLLM
        return MockLLM(model_name=model_name)
        
        # PRODUCTION MODE (commented out for demo)
        """
        if model_name.startswith("gpt"):
            return ChatOpenAI(
                model_name=model_name,
                temperature=0.7,
                openai_api_key=OPENAI_API_KEY
            )
        elif model_name.startswith("claude"):
            return ChatAnthropic(
                model=model_name,
                temperature=0.7,
                anthropic_api_key=ANTHROPIC_API_KEY
            )
        elif model_name.startswith("bedrock"):
            # For AWS Bedrock models
            model_id = model_name.split("-", 1)[1]  # Extract model ID after "bedrock-"
            return BedrockChat(
                model_id=model_id,
                region_name=AWS_REGION,
                model_kwargs={"temperature": 0.7}
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        """
    
    def _build_analysis_chain(self):
        """Build the customer data analysis chain"""
        analysis_prompt = PromptTemplate(
            template=EMAIL_ANALYSIS_TEMPLATE,
            input_variables=["customer_name", "tariff_type", "energy_usage", 
                            "location", "peak_usage_time", "customer_history"]
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=analysis_prompt,
            output_key="customer_insights",
            verbose=True
        )
    
    def _build_generation_chain(self):
        """Build the email generation chain"""
        generation_prompt = PromptTemplate(
            template=EMAIL_GENERATION_TEMPLATE,
            input_variables=["customer_name", "tariff_type", "energy_usage", 
                           "potential_savings", "recommended_plan", 
                           "location", "peak_usage_time", "customer_insights"]
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=generation_prompt,
            output_key="email_draft",
            verbose=True
        )
    
    def _build_refinement_chain(self):
        """Build the email refinement and optimization chain"""
        refinement_prompt = PromptTemplate(
            template=EMAIL_REFINEMENT_TEMPLATE,
            input_variables=["email_draft", "customer_name", "tariff_type"]
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=refinement_prompt,
            output_key="final_email",
            verbose=True
        )
    
    def _build_workflow(self):
        """Build the complete sequential workflow"""
        return SequentialChain(
            chains=[self.analysis_chain, self.generation_chain, self.refinement_chain],
            input_variables=["customer_name", "tariff_type", "energy_usage", 
                           "potential_savings", "recommended_plan", 
                           "location", "peak_usage_time", "customer_history"],
            output_variables=["customer_insights", "email_draft", "final_email"],
            verbose=True
        )
    
    def generate_campaign(self, customer_profile: CustomerProfile) -> EmailCampaign:
        """
        Generate an email campaign for a specific customer
        
        Args:
            customer_profile: Customer data including usage patterns
            
        Returns:
            EmailCampaign object containing the generated campaign
        """
        try:
            # Start tracing with LangSmith
            with langsmith.trace(
                project_name=self.trace_name,
                tags=["production", f"model:{self.model_name}"]
            ):
                # Prepare inputs
                inputs = {
                    "customer_name": customer_profile.name,
                    "tariff_type": customer_profile.tariff_type,
                    "energy_usage": customer_profile.energy_usage,
                    "potential_savings": customer_profile.potential_savings,
                    "recommended_plan": customer_profile.recommended_plan,
                    "location": customer_profile.location,
                    "peak_usage_time": customer_profile.peak_usage_time,
                    "customer_history": customer_profile.history_summary
                }
                
                # Execute the workflow
                logger.info(f"Generating campaign for customer: {customer_profile.name}")
                results = self.workflow.invoke(inputs)
                
                # Create EmailCampaign object
                campaign = EmailCampaign(
                    customer_id=customer_profile.customer_id,
                    email_subject=self._extract_subject(results["final_email"]),
                    email_body=results["final_email"],
                    customer_insights=results["customer_insights"],
                    draft_version=results["email_draft"],
                    final_version=results["final_email"],
                    model_used=self.model_name
                )
                
                return campaign
                
        except Exception as e:
            logger.error(f"Error generating campaign: {str(e)}")
            raise
    
    def _extract_subject(self, email_text):
        """Extract the subject line from the generated email"""
        if "Subject:" in email_text:
            return email_text.split("Subject:")[1].split("\n")[0].strip()
        return "Special Offer from Octopus Energy"  # Default subject