# Octopus Energy Marketing Email Assistant

A LangChain-powered intelligent assistant that helps marketers create personalized email campaigns for Octopus Energy customers.

## Overview

This project showcases a complete implementation of a prompt engineering system for generating marketing emails using LangChain, with a focus on prompt curation, model evaluation, and workflow orchestration. The system is designed to help marketers at Octopus Energy create highly personalized and effective email campaigns.

## Key Features

- **Multi-stage Email Generation**: Uses a sequential workflow with customer analysis, draft generation, and refinement stages
- **Advanced Prompt Engineering**: Systematically designed prompts with versioning, A/B testing, and prompt templates
- **Comprehensive Model Evaluation**: Evaluates email outputs on content quality, brand alignment, personalization, and CTA effectiveness
- **Model Comparison Framework**: Tests different LLMs to identify the best performer for email marketing
- **Simple Web Interface**: Provides a user-friendly interface for marketers to generate emails and chat with the assistant

## Architectural Design

### Orchestration Workflow

The email generation process follows a carefully orchestrated workflow:

1. **Customer Data Analysis**: The system analyzes customer data (usage patterns, location, tariff, etc.) to generate personalized insights.
2. **Email Draft Generation**: Using these insights, it creates a personalized email draft tailored to the customer's specific situation.
3. **Email Refinement**: The draft is optimized for clarity, engagement, and conversion potential.

This workflow is implemented as a LangChain sequential chain with memory, allowing each stage to build upon the previous ones.

### Prompt Engineering Approach

The project demonstrates advanced prompt engineering techniques:

- **System Prompts**: Define the overall context, role, and constraints for the LLM
- **Template Variations**: Multiple versions of each prompt template for systematic testing
- **Structured Outputs**: Clear formatting guidelines to ensure consistent email structure
- **A/B Testing Framework**: Tests different subject lines and CTAs to optimize performance
- **Brand Voice Integration**: Embeds Octopus Energy's specific tone and style guidelines

### Model Evaluation Framework

A comprehensive evaluation system assesses the quality of generated emails:

- **Content Quality**: Clarity, conciseness, grammar, persuasiveness, and readability
- **Brand Alignment**: How well the email matches Octopus Energy's brand voice
- **Personalization**: Effective use of customer data to create a tailored message
- **CTA Effectiveness**: Clarity, prominence, persuasiveness, and value proposition of the call-to-action
- **Aggregate Metrics**: Engagement score, conversion potential, and overall quality

### LangSmith Integration

The project leverages LangSmith for:
- Tracing and debugging the email generation workflow
- Logging and analyzing prompt performances
- Running systematic evaluations of different models
- Monitoring production performance

## Technology Stack

- **LangChain**: For orchestrating the entire email generation workflow
- **LangSmith**: For evaluation, tracing, and model comparison
- **Multiple LLMs**: OpenAI GPT-4, Anthropic Claude, AWS Bedrock models
- **Flask**: For the web interface
- **Pydantic**: For data validation and schema definition

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/octopus-email-assistant.git
cd octopus-email-assistant
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up environment variables:
```
cp .env.example .env
```
Edit the `.env` file to add your API keys and configuration.

4. Run the application:
```
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Highlights for Prompt Engineering Role

This project specifically demonstrates the skills required for the Prompt Engineer role at Octopus Energy:

### Prompt Crafting and Maintenance

- Systematic approach to prompt development with versioning
- Template variations for A/B testing
- Clear structure with specific instructions for model outputs
- Brand voice integration within prompts

### Test Prompts and Evaluation

- Comprehensive evaluation framework for email quality
- Systematic testing of different prompt variations
- Metrics for measuring effectiveness and brand alignment
- LangSmith integration for prompt tracking and performance analysis

### Safeguards and Quality Control

- Input validation and sanitization
- Error handling for edge cases
- Constraints to ensure output quality and brand alignment
- Monitoring system to detect problematic outputs

### Prompt Optimization

- Iterative refinement based on evaluation results
- A/B testing of different prompt structures
- Performance tracking through LangSmith
- Automated selection of the best-performing model and prompt combinations

## Usage Examples

### Generating an Email Campaign

```python
from orchestration.workflow import EmailCampaignWorkflow
from schemas.customer import CustomerProfile

# Create a customer profile
customer = CustomerProfile(
    customer_id="C1234",
    name="John Smith",
    tariff_type="Standard Variable",
    energy_usage=320,
    potential_savings=15,
    recommended_plan="GreenFlex",
    location="London",
    peak_usage_time="Evening",
    history_summary="Customer for 3 years, previously inquired about solar panels"
)

# Initialize the workflow
workflow = EmailCampaignWorkflow(model_name="gpt-4")

# Generate the campaign
campaign = workflow.generate_campaign(customer)

# Print the generated email
print(f"Subject: {campaign.email_subject}\n\n{campaign.email_body}")
```

### Using the Marketing Assistant Agent

```python
from orchestration.agent import MarketingEmailAgent

# Initialize the agent
agent = MarketingEmailAgent(model_name="claude-3-opus")

# Chat with the agent
response = agent.run("I need to create a seasonal winter campaign for customers on the Economy 7 tariff who use electric heating. What would you recommend?")

print(response)
```

## Why This Project Demonstrates Prompt Engineering Excellence

This project showcases the skills needed for a prompt engineering role in several ways:

1. **Systematic Prompt Development**: Rather than ad-hoc prompts, it demonstrates a structured approach to creating, testing, and refining prompts.

2. **Evaluation Framework**: It includes comprehensive metrics to measure prompt effectiveness and output quality.

3. **Orchestration Understanding**: Shows how to chain prompts together effectively in a multi-stage workflow.

4. **Brand Alignment**: Demonstrates how to ensure outputs match a specific brand voice and style.

5. **Model Comparison**: Provides a framework for testing different LLMs to select the best performer.

6. **Practical Application**: The system solves a real business need (personalized email marketing) with tangible value.

7. **Technical Implementation**: Shows not just prompt theory but practical implementation in a complete system.

This project would give the interviewer a clear demonstration of how you approach prompt engineering in a systematic, results-driven way.