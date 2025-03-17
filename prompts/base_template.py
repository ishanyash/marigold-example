# prompts/base_templates.py

"""
Base templates with versioning and A/B testing variations.
These templates allow for systematic testing of different prompt approaches.
"""

# Base template versions for customer analysis
ANALYSIS_TEMPLATE_V1 = """
Analyze the following customer data and provide insights for email personalization:
Customer: {customer_name}
Tariff: {tariff_type}
Usage: {energy_usage} kWh
Location: {location}

Provide 3 key insights about this customer's energy usage patterns.
"""

ANALYSIS_TEMPLATE_V2 = """
You are an energy marketing analyst. Review this customer profile:
- Name: {customer_name}
- Tariff: {tariff_type}
- Monthly Usage: {energy_usage} kWh
- Location: {location}
- Peak Usage: {peak_usage_time}

Identify specific opportunities for plan optimization and savings.
List 3-5 personalized recommendations based on their usage patterns.
"""

ANALYSIS_TEMPLATE_V3 = """
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
"""

# Base template versions for email generation
GENERATION_TEMPLATE_V1 = """
Create a marketing email for this Octopus Energy customer:
Name: {customer_name}
Tariff: {tariff_type}
Usage: {energy_usage} kWh
Potential Savings: {potential_savings}%

The email should highlight the savings they could achieve.
"""

GENERATION_TEMPLATE_V2 = """
You are an email marketer for Octopus Energy. Write a personalized email to this customer:
- Name: {customer_name}
- Current Tariff: {tariff_type}
- Monthly Usage: {energy_usage} kWh
- Potential Savings: {potential_savings}%
- Recommended Plan: {recommended_plan}

Customer Insights: {customer_insights}

Include a subject line, personalized greeting, and highlight potential savings.
Focus on both cost savings and environmental benefits.
End with a clear call-to-action.
"""

GENERATION_TEMPLATE_V3 = """
## EMAIL GENERATION TASK

Create a persuasive marketing email for this Octopus Energy customer:
* Name: {customer_name}
* Current Plan: {tariff_type}
* Monthly Usage: {energy_usage} kWh
* Location: {location}
* Usage Peak: {peak_usage_time}
* Potential Savings: {potential_savings}%
* Recommended Plan: {recommended_plan}

Based on these insights: {customer_insights}

Write an email with:
1. Attention-grabbing subject line
2. Personalized greeting
3. Reference to their current usage
4. Clear value proposition
5. Specific savings amount
6. Environmental benefits
7. Strong call-to-action

Keep it under 150 words and use a friendly, conversational tone.
"""

# Base template versions for email refinement
REFINEMENT_TEMPLATE_V1 = """
Improve this marketing email draft for an Octopus Energy customer:

{email_draft}

Make it more persuasive and personalized.
"""

REFINEMENT_TEMPLATE_V2 = """
You are an email optimization specialist. Refine this Octopus Energy email draft:

{email_draft}

Customer: {customer_name}
Tariff: {tariff_type}

Improve the subject line, strengthen personalization, and make the call-to-action more compelling.
Keep the total length under 150 words.
"""

REFINEMENT_TEMPLATE_V3 = """
## EMAIL REFINEMENT TASK

Optimize this Octopus Energy marketing email draft:

{email_draft}

For customer:
* Name: {customer_name}
* Current Plan: {tariff_type}

Improve the following aspects:
1. Subject line: Make it more attention-grabbing
2. Personalization: Enhance customer-specific elements
3. Clarity: Ensure the value proposition is clear
4. Persuasiveness: Strengthen the benefits
5. Call-to-action: Make it more compelling
6. Tone: Ensure it's friendly and conversational
7. Length: Keep it under 150 words

The final email should be ready to send without further edits.
"""

# A/B testing variants for email subject lines
SUBJECT_LINE_VARIANTS = {
    "savings_focused": "{customer_name}, Save {potential_savings}% on Your Energy Bills This Month",
    "question_based": "Are You Overpaying for Energy, {customer_name}?",
    "eco_focused": "Power Your Home with 100% Green Energy & Save {potential_savings}%",
    "urgency_based": "Last Chance: Switch & Save {potential_savings}% Before Prices Change",
    "benefit_focused": "More Control, Lower Bills: A Special Offer for {customer_name}"
}

# A/B testing variants for email CTAs
CTA_VARIANTS = {
    "action_oriented": "Switch to {recommended_plan} Now",
    "benefit_focused": "See Your Personalized Savings",
    "low_commitment": "Explore Your Energy Options",
    "urgency_based": "Lock In These Savings Today",
    "curiosity_based": "Discover How Much You Could Save"
}

# Functions to create template variations for testing
def create_template_variation(base_template, subject_variant, cta_variant):
    """Create a template variation with specific subject and CTA styles"""
    return base_template.replace(
        "[SUBJECT_VARIANT]", SUBJECT_LINE_VARIANTS[subject_variant]
    ).replace(
        "[CTA_VARIANT]", CTA_VARIANTS[cta_variant]
    )