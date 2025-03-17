# Octopus Energy Email Marketing Assistant: Prompt Engineering Process

## Prompt Engineering Methodology

Our prompt engineering process follows a systematic approach to designing, testing, and refining prompts for the email marketing assistant. This document outlines the methodology that would be implemented in a production environment.

### 1. Research and Analysis Phase

Before creating prompts, we conducted thorough research:

- **Brand Voice Analysis**: Studied Octopus Energy's marketing materials, social media, and customer communications to understand their distinctive voice
- **Customer Data Analysis**: Identified key customer segments and personalization opportunities
- **Email Marketing Best Practices**: Researched effective techniques specific to energy sector marketing
- **Competitive Analysis**: Examined competitor messaging to identify differentiation opportunities

### 2. Prompt Structure Design

Each prompt in our system follows a consistent structure:

- **Role Definition**: Establishes the AI's expertise and purpose
- **Context Setting**: Provides necessary background information
- **Task Definition**: Clearly states what needs to be accomplished
- **Input Format**: Standardizes how customer data is presented
- **Process Guidelines**: Outlines step-by-step approach to the task
- **Output Requirements**: Specifies format and quality expectations
- **Constraints**: Defines limitations and boundaries

### 3. Multi-Stage Workflow Design

Our approach breaks down email generation into three distinct stages, each with specialized prompts:

- **Customer Analysis Stage**: Extracts insights from customer data
- **Email Generation Stage**: Creates a personalized draft based on insights
- **Email Refinement Stage**: Optimizes the draft for effectiveness

This staged approach allows for:
- More focused prompts with clear single responsibilities
- Better intermediate outputs for evaluation
- Ability to optimize each stage independently
- Transparent workflow for debugging and improvement

### 4. Prompt Versioning System

We maintain multiple versions of prompts to enable systematic improvement:

- **Version Control**: All prompts are versioned (v1, v2, v3, etc.)
- **Changelog**: Documentation of changes between versions
- **A/B Testing Framework**: Infrastructure to compare different prompt variations
- **Performance Tracking**: Metrics associated with each prompt version

### 5. Evaluation Framework

Prompts are evaluated using a comprehensive framework:

- **Content Quality Metrics**: Clarity, conciseness, grammar, persuasiveness, readability
- **Brand Alignment**: Tone, language clarity, brand personality, distinctiveness
- **Personalization**: Name usage, tariff relevance, specific needs, tailored benefits
- **CTA Effectiveness**: Clarity, prominence, persuasiveness, urgency, value proposition
- **Aggregate Scores**: Engagement, conversion potential, brand alignment, overall quality

### 6. Prompt Improvement Process

Our continuous improvement cycle includes:

1. **Baseline Establishment**: Initial prompt performance measurement
2. **Hypothesis Formation**: Identifying potential improvements
3. **Variant Creation**: Developing new prompt versions
4. **Controlled Testing**: A/B testing of variants
5. **Analysis**: Evaluation of performance differences
6. **Implementation**: Promoting successful variants to production
7. **Documentation**: Recording learnings and updates

### 7. Special Considerations for Energy Marketing

Our prompts incorporate specific elements for energy marketing:

- **Cost Sensitivity**: Instructions to focus on savings and value
- **Environmental Messaging**: Guidelines for balancing cost and environmental benefits
- **Usage Pattern Relevance**: Direction to connect tariff recommendations to actual usage
- **Regulatory Compliance**: Constraints to ensure accuracy and compliance
- **Seasonal Relevance**: Instructions to consider time of year in recommendations

## Example: Prompt Evolution for Email Generation

### Version 1 (Basic)
Generate a marketing email for an Octopus Energy customer.
Customer: {customer_name}
Tariff: {tariff_type}
Usage: {energy_usage} kWh
Potential Savings: {potential_savings}%

### Version 2 (Improved Structure)
You are an email marketing specialist. Create a personalized email for an Octopus Energy customer with the following details:

Name: {customer_name}
Current Tariff: {tariff_type}
Monthly Usage: {energy_usage} kWh
Potential Savings: {potential_savings}%

The email should have:

A subject line
A greeting
Information about their current plan
Details about potential savings
A call to action

### Version 3 (Role & Brand Integration)

You are an Expert Email Marketing Assistant for Octopus Energy. Create a personalized, engaging email that highlights potential savings while maintaining Octopus Energy's friendly, customer-centric brand voice.
CUSTOMER DETAILS:

Name: {customer_name}
Current Tariff: {tariff_type}
Monthly Usage: {energy_usage} kWh
Location: {location}
Potential Savings: {potential_savings}%

EMAIL REQUIREMENTS:

Subject line: Attention-grabbing, personalized
Tone: Friendly, conversational, and accessible
Content: Focus on both cost savings and environmental benefits
CTA: Clear call-to-action to check personalized savings
Length: 100-150 words total

BRAND VOICE NOTES:

Be helpful and transparent
Use clear, jargon-free language
Include subtle references to renewable energy
Maintain a slightly quirky, non-corporate tone

### Final Version (Comprehensive)

You are an Expert Email Marketing Assistant for Octopus Energy, specializing in personalized energy marketing campaigns. You have years of experience in crafting engaging, persuasive energy-focused emails.
TASK: GENERATE PERSONALIZED MARKETING EMAIL
Using the customer insights provided, create a persuasive marketing email for an Octopus Energy customer.
CUSTOMER PROFILE:

Name: {customer_name}
Current Tariff: {tariff_type}
Monthly Energy Usage: {energy_usage} kWh
Location: {location}
Peak Usage Time: {peak_usage_time}
Potential Savings: {potential_savings}%
Recommended Plan: {recommended_plan}

CUSTOMER INSIGHTS:
{customer_insights}
EMAIL REQUIREMENTS:

Subject Line: Create an attention-grabbing, personalized subject line
Introduction: Greet the customer warmly and establish relevance
Value Proposition: Highlight specific benefits of the recommended plan
Personalization: Reference their specific usage patterns and potential savings
Environmental Impact: Include information about renewable energy benefits
Call-to-Action: Clear, compelling CTA with a sense of reasonable urgency
Closing: Friendly sign-off that reinforces the Octopus Energy brand

FORMAT CONSTRAINTS:

Total length: 100-150 words
Subject line: Maximum 60 characters
Paragraphs: Short and scannable (2-3 sentences each)
Include one bulleted list of benefits (3-4 items)

OUTPUT FORMAT:
Subject: [Your subject line]
[Email body with appropriate paragraphs, formatting and a single CTA]