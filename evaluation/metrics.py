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

def calculate_personalization_score(email_content, customer_data):
    """
    Calculate how well the email is personalized to the customer.
    
    Args:
        email_content: Generated email text
        customer_data: Customer profile data
        
    Returns:
        float: Personalization score on a scale of 0-10
    """
    score = 0.0
    max_score = 0.0
    
    # Check for name usage
    if customer_data.get("name") and customer_data["name"] in email_content:
        score += 2.0
    max_score += 2.0
    
    # Check for tariff reference
    if customer_data.get("tariff_type") and customer_data["tariff_type"] in email_content:
        score += 2.0
    max_score += 2.0
    
    # Check for energy usage reference
    if customer_data.get("energy_usage") and str(customer_data["energy_usage"]) in email_content:
        score += 1.5
    max_score += 1.5
    
    # Check for location reference
    if customer_data.get("location") and customer_data["location"] in email_content:
        score += 1.5
    max_score += 1.5
    
    # Check for savings reference
    if customer_data.get("potential_savings") and str(customer_data["potential_savings"]) in email_content:
        score += 2.0
    max_score += 2.0
    
    # Check for recommended plan reference
    if customer_data.get("recommended_plan") and customer_data["recommended_plan"] in email_content:
        score += 1.0
    max_score += 1.0
    
    # Normalize score to 0-10 scale
    if max_score > 0:
        normalized_score = (score / max_score) * 10
    else:
        normalized_score = 5.0  # Default if no customer data available
    
    return round(normalized_score, 1)

def calculate_reading_time(text):
    """
    Calculate estimated reading time in seconds.
    
    Args:
        text: Email content
        
    Returns:
        int: Estimated reading time in seconds
    """
    # Average reading speed: 200-250 words per minute
    words = len(text.split())
    reading_time_minutes = words / 225  # Using 225 words per minute
    return round(reading_time_minutes * 60)  # Convert to seconds

def calculate_overall_score(evaluation_results):
    """
    Calculate an overall quality score based on multiple dimensions.
    
    Args:
        evaluation_results: Dict containing evaluation metrics
        
    Returns:
        float: Overall score on a scale of 0-10
    """
    try:
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
    except (TypeError, ValueError):
        return 5.0  # Default value if calculation fails

def grade_performance(score):
    """
    Convert numeric score to letter grade.
    
    Args:
        score: Numeric score (0-10)
        
    Returns:
        str: Letter grade (A+, A, B, C, D, F)
    """
    if score >= 9.5:
        return "A+"
    elif score >= 9.0:
        return "A"
    elif score >= 8.0:
        return "A-"
    elif score >= 7.0:
        return "B+"
    elif score >= 6.0:
        return "B"
    elif score >= 5.0:
        return "C"
    elif score >= 4.0:
        return "D"
    else:
        return "F"