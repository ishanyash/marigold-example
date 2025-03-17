# Octopus Energy Marketing Email Assistant

## Project Overview

A demonstration project showcasing a prompt engineering approach for creating personalized marketing emails using LangChain and LLMs.

![Email Generation Workflow](
    graph TD
    A[Customer Profile Data] --> B[Stage 1: Analysis]
    B --> C[Customer Insights]
    C --> D[Stage 2: Email Generation]
    D --> E[Email Draft]
    E --> F[Stage 3: Refinement]
    F --> G[Final Email]
    
    subgraph "Analysis Stage"
    B
    end
    
    subgraph "Generation Stage"
    D
    end
    
    subgraph "Refinement Stage"
    F
    end
    
    style B fill:#4c12a1,color:white
    style D fill:#4c12a1,color:white
    style F fill:#4c12a1,color:white)

## Project Goals

This project demonstrates my approach to prompt engineering for generating marketing emails at Octopus Energy. It specifically addresses:

1. **Orchestration Workflow**: How I designed a multi-stage process for email generation
2. **Model Evaluation**: How I systematically assessed LLMs for this task
3. **Prompt Curation**: How I crafted and iterated on prompts to achieve optimal results

## Orchestration Workflow

I designed a three-stage workflow to break down the complex email generation task:

1. **Analysis Stage**: The LLM analyzes customer data (usage patterns, location, tariff) to generate personalized insights
2. **Generation Stage**: Using these insights, it creates a personalized email draft
3. **Refinement Stage**: The draft is optimized for clarity, engagement, and conversion potential

```python
def generate_campaign(customer_profile):
    # Stage 1: Analyze customer data
    customer_insights = analysis_chain.invoke({
        "customer_name": customer_profile.name,
        "tariff_type": customer_profile.tariff_type,
        "energy_usage": customer_profile.energy_usage,
        "location": customer_profile.location,
        "peak_usage_time": customer_profile.peak_usage_time,
        "customer_history": customer_profile.history_summary
    })
    
    # Stage 2: Generate email draft
    email_draft = generation_chain.invoke({
        **customer_profile.dict(),
        "customer_insights": customer_insights["customer_insights"]
    })
    
    # Stage 3: Refine and optimize email
    final_email = refinement_chain.invoke({
        "email_draft": email_draft["email_draft"],
        "customer_name": customer_profile.name,
        "tariff_type": customer_profile.tariff_type
    })
    
    return EmailCampaign(
        customer_id=customer_profile.customer_id,
        email_subject=extract_subject(final_email["final_email"]),
        email_body=final_email["final_email"],
        customer_insights=customer_insights["customer_insights"],
        draft_version=email_draft["email_draft"],
        final_version=final_email["final_email"]
    )
```

This modular approach provides several advantages:
- Each stage can be optimized independently
- The system can trace and evaluate performance at each step
- Complex reasoning is broken into manageable chunks for the LLM

## Model Evaluation Framework

I developed a comprehensive evaluation framework to assess LLM performance:

![Model Comparison](https://raw.githubusercontent.com/username/octopus-email-assistant/main/static/model_comparison.png)

The evaluation system assesses email outputs along four key dimensions:
- **Content Quality**: Clarity, conciseness, grammar, persuasiveness, readability
- **Brand Alignment**: Tone, language clarity, brand personality, distinctiveness
- **Personalization**: Name usage, tariff relevance, specific needs, tailored benefits
- **CTA Effectiveness**: Clarity, prominence, persuasiveness, urgency, value proposition

These dimensions are combined into aggregate metrics:
- **Engagement Score**: How likely the email is to be read and engaged with
- **Conversion Potential**: How effectively it drives action
- **Brand Alignment Score**: How well it matches Octopus Energy's voice
- **Overall Score**: Weighted combination of all metrics

```python
def calculate_overall_score(evaluation_results):
    """Calculate an overall quality score based on multiple dimensions"""
    engagement_score = evaluation_results.get("engagement_score", 5.0)
    conversion_potential = evaluation_results.get("conversion_potential", 5.0)
    brand_alignment_score = evaluation_results.get("brand_alignment_score", 5.0)
    
    # Weighted score calculation
    overall_score = (
        engagement_score * 0.3 +
        conversion_potential * 0.4 +
        brand_alignment_score * 0.3
    )
    
    return round(overall_score, 1)
```

## Prompt Curation Methodology

My prompt development process followed a systematic approach:

![Prompt Engineering Workflow](
    graph TD
    A[Research Brand Voice] --> B[Design Initial Prompts]
    B --> C[Create Prompt Variations]
    C --> D[Test on Sample Data]
    D --> E[Evaluate Outputs]
    E --> F{Meets Quality Standards?}
    F -->|No| G[Refine Prompts]
    G --> C
    F -->|Yes| H[Release to Production]
    H --> I[Monitor Performance]
    I --> J{Need Improvement?}
    J -->|Yes| G
    J -->|No| I
    
    style B fill:#4c12a1,color:white
    style E fill:#4c12a1,color:white
    style G fill:#4c12a1,color:white
    style I fill:#4c12a1,color:white
)

### 1. System Prompts as Foundation
I started with carefully crafted system prompts that:
- Define the AI's role as an expert email marketing assistant
- Establish Octopus Energy's brand voice and constraints
- Set quality expectations

```
You are an Expert Email Marketing Assistant for Octopus Energy, specializing in personalized
energy marketing campaigns. You have years of experience in crafting engaging, persuasive
energy-focused emails that drive conversions while maintaining Octopus Energy's friendly,
customer-centric brand voice.
```

### 2. Structured Prompt Templates
Each task has a dedicated prompt template with:
- Clear task definition
- Specific input format
- Step-by-step process guidelines
- Concrete output requirements
- Constraints and quality standards

### 3. Prompt Versioning
I implemented multiple versions of each prompt to enable systematic testing:

**Analysis Prompt Evolution:**
```
# Version 1 (Basic)
Analyze the following customer data and provide insights for email personalization:
Customer: {customer_name}
Tariff: {tariff_type}
Usage: {energy_usage} kWh
Location: {location}

Provide 3 key insights about this customer's energy usage patterns.

# Version 3 (Advanced)
## CUSTOMER ANALYSIS TASK

Thoroughly analyze this Octopus Energy customer:
* Customer: {customer_name}
* Current Plan: {tariff_type}
* Monthly Usage: {energy_usage} kWh
* Location: {location}
* Usage Peak: {peak_usage_time}
* History: {customer_history}

First, identify usage patterns.
Second, compare to similar customers.
Third, calculate potential savings opportunities.
Finally, recommend specific messaging angles.

Your analysis should be data-driven and actionable.
```

### 4. A/B Testing Framework
The implementation includes frameworks for testing variations in:
- **Subject Line Styles**: Savings-focused, question-based, eco-focused, etc.
- **CTA Variations**: Action-oriented, benefit-focused, low-commitment, etc.
- **Structure**: Various email formats and content organization

```python
# A/B testing variants for email subject lines
SUBJECT_LINE_VARIANTS = {
    "savings_focused": "{customer_name}, Save {potential_savings}% on Your Energy Bills This Month",
    "question_based": "Are You Overpaying for Energy, {customer_name}?",
    "eco_focused": "Power Your Home with 100% Green Energy & Save {potential_savings}%",
    "urgency_based": "Last Chance: Switch & Save {potential_savings}% Before Prices Change",
    "benefit_focused": "More Control, Lower Bills: A Special Offer for {customer_name}"
}
```

## Project Structure

```
octopus-email-assistant/
├── orchestration/
│   ├── workflow.py      # Multi-stage email generation workflow
│   ├── chains.py        # LangChain components for each stage
│   └── agent.py         # Marketing assistant agent
├── prompts/
│   ├── system_prompts.py    # Foundational role definitions
│   ├── email_templates.py   # Main prompt templates
│   └── base_templates.py    # Versioned template variations
├── evaluation/
│   ├── evaluators.py    # LLM output evaluation framework
│   ├── metrics.py       # Scoring functions
│   └── test_cases.py    # Systematic model testing
└── schemas/
    └── customer.py      # Data validation schemas
```

## Sample Output

**Customer Insights:**
```
Based on the customer data analysis, here are the key insights:

1. This customer has higher than average energy usage during evening hours (7pm-11pm),
   suggesting they might benefit from an Economy 7 tariff or time-of-use optimization.

2. Their location in London indicates they're in an area with high adoption of smart
   home technology and environmental consciousness.

3. Their current Standard Variable tariff is not optimized for their usage patterns,
   which show consistency month-to-month.

4. Given their energy consumption and current tariff, there's potential for 12-15%
   savings by switching to the GreenFlex plan.

5. Customer history shows interest in renewable energy options but concern about
   initial costs - messaging should emphasize immediate savings alongside
   environmental benefits.
```

**Generated Email:**
```
Subject: Alex, Cut Your Evening Energy Costs by 15% This Month

Hi Alex,

Looking at your recent energy usage, I noticed you're using most power during
evenings on your Standard Variable tariff. This presents a perfect opportunity!

Switch to our GreenFlex plan and save 15% on your monthly bills – that's around
£180 over the next year based on your 350 kWh monthly usage. Plus, you'll be
powering your home with 100% renewable electricity.

Perfect for your lifestyle:
• Lower rates during your actual usage hours
• Real-time consumption tracking in our simple app
• 100% green energy without the premium price
• No contract lock-in – flexibility guaranteed

Take 2 minutes to switch now and start saving immediately.

[See Your Exact Savings]

The Octopus Energy Team
```

## Key Advantages

This implementation demonstrates several strengths relevant to a prompt engineering role:

1. **Systematic Methodology**: A structured approach to prompt development rather than ad-hoc solutions
2. **Evaluation Framework**: Comprehensive metrics for measuring prompt effectiveness
3. **Prompt Versioning**: Clear system for tracking prompt iterations and improvements
4. **Brand Voice Integration**: Techniques for ensuring AI outputs match specific brand guidelines
5. **LangChain Expertise**: Leveraging LangChain for complex multi-stage workflows

This project showcases my approach to prompt engineering as a systematic discipline requiring careful design, testing, evaluation, and refinement.