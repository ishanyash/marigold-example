# evaluation/test_cases.py

import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from langchain_core.tracers import LangChainTracer
from langsmith import Client

from config.settings import LANGSMITH_API_KEY, AVAILABLE_MODELS
from orchestration.workflow import EmailCampaignWorkflow
from schemas.customer import CustomerProfile
from evaluation.evaluators import EmailContentEvaluator
from utils.logger import get_logger

logger = get_logger(__name__)

class ModelComparisonRunner:
    """
    Runs systematic comparisons of different LLMs using standardized test cases.
    Records results in LangSmith for analysis and model selection.
    """
    
    def __init__(self, project_name="octopus-model-comparison"):
        self.project_name = project_name
        self.langsmith_client = Client(api_key=LANGSMITH_API_KEY)
        self.evaluator = EmailContentEvaluator()
        self.models_to_test = AVAILABLE_MODELS
        self.results = {}
    
    def load_test_cases(self, test_case_path="./data/test_customers.json"):
        """Load customer test cases from JSON file"""
        try:
            with open(test_case_path, 'r') as f:
                test_cases = json.load(f)
            
            # Convert to CustomerProfile objects
            self.test_customers = [
                CustomerProfile(**customer_data)
                for customer_data in test_cases
            ]
            logger.info(f"Loaded {len(self.test_customers)} test cases")
            return self.test_customers
        except Exception as e:
            logger.error(f"Error loading test cases: {str(e)}")
            # Fallback to sample test cases
            self.test_customers = self._generate_sample_test_cases()
            return self.test_customers
    
    def _generate_sample_test_cases(self):
        """Generate sample test cases if file loading fails"""
        return [
            CustomerProfile(
                customer_id="TEST001",
                name="Alex Johnson",
                tariff_type="Standard Variable",
                energy_usage=350,
                potential_savings=12,
                recommended_plan="GreenFlex",
                location="London",
                peak_usage_time="Evening",
                history_summary="Customer for 2 years, previously inquired about solar"
            ),
            CustomerProfile(
                customer_id="TEST002",
                name="Sarah Williams",
                tariff_type="Economy 7",
                energy_usage=480,
                potential_savings=18,
                recommended_plan="Agile Octopus",
                location="Manchester",
                peak_usage_time="Morning and Evening",
                history_summary="New customer, switched from competitor last month"
            ),
            CustomerProfile(
                customer_id="TEST003",
                name="Mohammed Khan",
                tariff_type="Fixed Rate",
                energy_usage=290,
                potential_savings=8,
                recommended_plan="Super Green Octopus",
                location="Birmingham",
                peak_usage_time="Daytime",
                history_summary="Customer for 5 years, very environmentally conscious"
            ),
        ]
    
    def run_comparisons(self):
        """Run email generation with all models on all test cases"""
        results = []
        
        for model_name in self.models_to_test:
            logger.info(f"Testing model: {model_name}")
            
            try:
                # Initialize workflow with this model
                workflow = EmailCampaignWorkflow(
                    model_name=model_name,
                    trace_name=f"{self.project_name}-{model_name}"
                )
                
                # Run all test cases
                model_results = []
                for customer in self.test_customers:
                    try:
                        # Generate email campaign
                        campaign = workflow.generate_campaign(customer)
                        
                        # Evaluate the campaign
                        evaluation = self.evaluator.evaluate_run(campaign)
                        
                        # Record results
                        model_results.append({
                            "customer_id": customer.customer_id,
                            "model": model_name,
                            "overall_score": evaluation["overall_score"],
                            "engagement_score": evaluation["engagement_score"],
                            "conversion_potential": evaluation["conversion_potential"],
                            "brand_alignment": evaluation["brand_alignment_score"],
                            "email_content": campaign.email_body
                        })
                        
                    except Exception as e:
                        logger.error(f"Error with {model_name} on {customer.customer_id}: {str(e)}")
                
                # Add all results for this model
                results.extend(model_results)
                
            except Exception as e:
                logger.error(f"Error initializing model {model_name}: {str(e)}")
        
        # Store results
        self.comparison_results = results
        return results
    
    def analyze_results(self):
        """Analyze comparison results and create reports"""
        if not hasattr(self, 'comparison_results'):
            logger.error("No comparison results found. Run comparisons first.")
            return None
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(self.comparison_results)
        
        # Calculate average scores by model
        model_scores = df.groupby('model').agg({
            'overall_score': ['mean', 'std'],
            'engagement_score': 'mean',
            'conversion_potential': 'mean',
            'brand_alignment': 'mean'
        }).round(2)
        
        # Identify best performing model
        best_model = model_scores['overall_score']['mean'].idxmax()
        
        # Create summary report
        summary = {
            "best_model": best_model,
            "model_rankings": model_scores.sort_values(('overall_score', 'mean'), ascending=False).to_dict(),
            "sample_counts": df['model'].value_counts().to_dict(),
            "top_score": model_scores['overall_score']['mean'].max()
        }
        
        # Log findings
        logger.info(f"Best performing model: {best_model}")
        
        # Create visualizations
        self._create_comparison_charts(df)
        
        return summary
    
    def _create_comparison_charts(self, results_df):
        """Create visualization of model comparison results"""
        try:
            # Group data by model
            model_summary = results_df.groupby('model').agg({
                'overall_score': 'mean',
                'engagement_score': 'mean',
                'conversion_potential': 'mean',
                'brand_alignment': 'mean'
            }).reset_index()
            
            # Creating the bar chart
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Set width of bars
            bar_width = 0.2
            x = range(len(model_summary))
            
            # Create bars
            ax.bar([i - bar_width*1.5 for i in x], model_summary['overall_score'], 
                   width=bar_width, label='Overall', color='navy')
            ax.bar([i - bar_width*0.5 for i in x], model_summary['engagement_score'], 
                   width=bar_width, label='Engagement', color='royalblue')
            ax.bar([i + bar_width*0.5 for i in x], model_summary['conversion_potential'], 
                   width=bar_width, label='Conversion', color='skyblue')
            ax.bar([i + bar_width*1.5 for i in x], model_summary['brand_alignment'], 
                   width=bar_width, label='Brand Alignment', color='lightblue')
            
            # Add labels and title
            ax.set_xlabel('Model')
            ax.set_ylabel('Score (0-10)')
            ax.set_title('LLM Performance Comparison for Email Generation')
            ax.set_xticks(x)
            ax.set_xticklabels(model_summary['model'], rotation=45, ha='right')
            ax.legend()
            ax.set_ylim(0, 10)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            plt.tight_layout()
            
            # Save the figure
            plt.savefig('./static/model_comparison.png')
            logger.info("Created model comparison visualization")
        
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
    
    def get_best_model(self):
        """Return the name of the best performing model"""
        if hasattr(self, 'comparison_results'):
            df = pd.DataFrame(self.comparison_results)
            best_model = df.groupby('model')['overall_score'].mean().idxmax()
            return best_model
        else:
            logger.warning("No comparison results available. Using default model.")
            return AVAILABLE_MODELS[0]  # Return first available model as default


# Example usage in config/settings.py:

AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-3.5-turbo",
    "claude-3-opus",
    "claude-3-sonnet",
    "bedrock-anthropic.claude-3-sonnet",
    "bedrock-amazon.titan-text-express"
]

# Model selection logic for production use
def select_production_model():
    """
    Select the best model for production use based on comparison data.
    Falls back to default if comparison data isn't available.
    """
    try:
        # Try to load saved comparison results
        with open('./data/model_comparison_results.json', 'r') as f:
            comparison_data = json.load(f)
        
        if 'best_model' in comparison_data:
            return comparison_data['best_model']
        else:
            return "gpt-4"  # Default to GPT-4 if no best model found
    except:
        # Fallback if file doesn't exist or can't be read
        return "gpt-4"