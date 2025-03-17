# prompts/email_templates.py

"""
Specific prompt templates for each stage of the email generation workflow.
These templates are structured to extract the maximum value from the LLM
while ensuring outputs meet our quality standards.
"""

from prompts.system_prompts import ENERGY_MARKETING_EXPERT_PROMPT, OCTOPUS_BRAND_VOICE_PROMPT

# Template for analyzing customer data
EMAIL_ANALYSIS_TEMPLATE = """
{system_prompt}

## TASK: ANALYZE CUSTOMER DATA FOR EMAIL PERSONALIZATION

You'll be provided with customer data for an Octopus Energy user. Analyze this data to identify 
key insights that would help personalize a marketing email.

### CUSTOMER INFORMATION:
- Name: {customer_name}
- Current Tariff: {tariff_type}
- Monthly Energy Usage: {energy_usage} kWh
- Location: {location}
- Peak Usage Time: {peak_usage_time}
- Customer History: {customer_history}

### ANALYSIS INSTRUCTIONS:
1. Identify usage patterns that might indicate potential savings opportunities
2. Determine which Octopus Energy plans might best suit this customer
3. Consider seasonal factors based on location and time of year
4. Analyze peak usage times to identify potential smart-meter benefits
5. Review customer history to personalize messaging (long-time customer vs. new user)

### OUTPUT GUIDELINES:
- Provide 3-5 key insights about this customer
- Suggest specific messaging angles that would resonate with this customer
- Recommend specific features to highlight based on their usage patterns
- Identify any potential pain points this customer might have with their current plan
- Suggest tone and approach based on their profile (e.g., data-driven, cost-conscious, eco-minded)

Your analysis should be structured, evidence-based, and focused on actionable insights for email personalization.
""".format(system_prompt=ENERGY_MARKETING_EXPERT_PROMPT)

# Template for generating the initial email draft
EMAIL_GENERATION_TEMPLATE = """
{system_prompt}

{brand_voice}

## TASK: GENERATE PERSONALIZED MARKETING EMAIL

Using the customer insights provided, create a persuasive marketing email for an Octopus Energy customer.

### CUSTOMER PROFILE:
- Name: {customer_name}
- Current Tariff: {tariff_type}
- Monthly Energy Usage: {energy_usage} kWh
- Location: {location}
- Peak Usage Time: {peak_usage_time}
- Potential Savings: {potential_savings}%
- Recommended Plan: {recommended_plan}

### CUSTOMER INSIGHTS:
{customer_insights}

### EMAIL REQUIREMENTS:
1. Subject Line: Create an attention-grabbing, personalized subject line
2. Introduction: Greet the customer warmly and establish relevance
3. Value Proposition: Highlight specific benefits of the recommended plan
4. Personalization: Reference their specific usage patterns and potential savings
5. Environmental Impact: Include information about renewable energy benefits
6. Call-to-Action: Clear, compelling CTA with a sense of reasonable urgency
7. Closing: Friendly sign-off that reinforces the Octopus Energy brand

### FORMAT CONSTRAINTS:
- Total length: 100-150 words
- Subject line: Maximum 60 characters
- Paragraphs: Short and scannable (2-3 sentences each)
- Include one bulleted list of benefits (3-4 items)

### OUTPUT FORMAT:
Subject: [Your subject line]

[Email body with appropriate paragraphs, formatting and a single CTA]
""".format(
    system_prompt=ENERGY_MARKETING_EXPERT_PROMPT,
    brand_voice=OCTOPUS_BRAND_VOICE_PROMPT
)

# Template for refining and optimizing the email
EMAIL_REFINEMENT_TEMPLATE = """
{system_prompt}

{brand_voice}

## TASK: OPTIMIZE AND REFINE MARKETING EMAIL

You'll be given a draft email for an Octopus Energy customer. Your job is to refine and optimize
this email to maximize engagement, clarity, and conversion potential.

### CUSTOMER INFORMATION:
- Name: {customer_name}
- Current Tariff: {tariff_type}

### DRAFT EMAIL:
{email_draft}

### REFINEMENT INSTRUCTIONS:
1. Improve subject line for higher open rates (be specific, create curiosity, add urgency if appropriate)
2. Enhance personalization throughout the email
3. Tighten language and remove any unnecessary words
4. Strengthen the call-to-action
5. Ensure tone is friendly and aligned with Octopus Energy's brand voice
6. Check for and fix any awkward phrasing or unclear messaging
7. Add any missing key benefits that would appeal to this specific customer
8. Ensure total word count stays between 100-150 words

### OPTIMIZATION FOCUS AREAS:
- Clarity: Is the offer and its value immediately clear?
- Personalization: Does it feel specifically written for this customer?
- Persuasiveness: Are benefits framed effectively to drive action?
- Tone: Is it friendly, helpful, and non-pushy?
- Actionability: Is the CTA clear and compelling?

Provide the completely refined email, ready to send.
""".format(
    system_prompt=ENERGY_MARKETING_EXPERT_PROMPT,
    brand_voice=OCTOPUS_BRAND_VOICE_PROMPT
)