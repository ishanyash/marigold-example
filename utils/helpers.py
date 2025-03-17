# utils/helpers.py

import re
import json
from typing import Dict, List, Any, Optional

def extract_subject_line(email_text: str) -> str:
    """
    Extract the subject line from a generated email.
    
    Args:
        email_text: Full email text including subject line
        
    Returns:
        str: Extracted subject line, or default if not found
    """
    subject_pattern = r"Subject:([^\n]*)"
    match = re.search(subject_pattern, email_text)
    
    if match:
        return match.group(1).strip()
    return "Special Offer from Octopus Energy"  # Default subject

def parse_customer_data(customer_text: str) -> Dict[str, Any]:
    """
    Parse customer data from structured text input.
    
    Args:
        customer_text: Text containing customer information
        
    Returns:
        Dict: Parsed customer data
    """
    patterns = {
        "name": r"Name:?\s*([^\n,]+)",
        "tariff_type": r"Tariff:?\s*([^\n,]+)",
        "energy_usage": r"Usage:?\s*(\d+)\s*kWh",
        "location": r"Location:?\s*([^\n,]+)",
        "peak_usage_time": r"Peak(?:\s*usage)?(?:\s*time)?:?\s*([^\n,]+)"
    }
    
    result = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, customer_text, re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()
    
    # Convert energy usage to int if found
    if "energy_usage" in result:
        try:
            result["energy_usage"] = int(result["energy_usage"])
        except ValueError:
            pass
    
    return result

def format_email_for_display(email_body: str) -> str:
    """
    Format an email body for HTML display.
    
    Args:
        email_body: Raw email body text
        
    Returns:
        str: HTML-formatted email for display
    """
    # Replace newlines with HTML breaks
    formatted = email_body.replace('\n', '<br>')
    
    # Make bullet points into HTML lists
    bullet_pattern = r'(?:^|\n)[\s]*[•\-\*][\s]+(.+)'
    if re.search(bullet_pattern, email_body, re.MULTILINE):
        # Start list
        formatted = re.sub(r'(?:^|\n)[\s]*[•\-\*][\s]+', r'<ul><li>', formatted, count=1, flags=re.MULTILINE)
        # Middle items
        formatted = re.sub(r'(?:\n)[\s]*[•\-\*][\s]+', r'</li><li>', formatted)
        # End list
        bullet_end_pattern = r'</li><li>(.+?)(?=<br>|$)'
        match = re.search(bullet_end_pattern, formatted)
        if match:
            formatted = re.sub(bullet_end_pattern, r'</li><li>\1</li></ul>', formatted, count=1)
    
    # Highlight CTA in button-like style
    cta_patterns = [
        r'\[([^\]]+)\]',  # [Text in brackets]
        r'<\s*([^>]+)\s*>',  # <Text in angle brackets>
    ]
    
    for pattern in cta_patterns:
        formatted = re.sub(
            pattern,
            r'<div style="display:inline-block; background-color:#4c12a1; color:white; padding:8px 15px; border-radius:5px; margin:10px 0;">\1</div>',
            formatted
        )
    
    return formatted

def calculate_savings_amount(energy_usage: int, potential_savings: float) -> float:
    """
    Calculate estimated savings amount based on usage and percentage.
    
    Args:
        energy_usage: Monthly energy usage in kWh
        potential_savings: Savings percentage (e.g., 15 for 15%)
        
    Returns:
        float: Estimated monthly savings in pounds
    """
    # Average cost per kWh (simplified for demo)
    avg_cost_per_kwh = 0.28  # £0.28 per kWh
    
    # Calculate current monthly cost
    current_cost = energy_usage * avg_cost_per_kwh
    
    # Calculate savings
    savings = current_cost * (potential_savings / 100)
    
    return round(savings, 2)

def calculate_annual_savings(monthly_savings: float) -> float:
    """
    Calculate annual savings based on monthly amount.
    
    Args:
        monthly_savings: Monthly savings amount
        
    Returns:
        float: Annual savings estimate
    """
    return round(monthly_savings * 12, 2)

def get_recommended_plan(tariff_type: str, energy_usage: int, peak_usage_time: str) -> str:
    """
    Get a plan recommendation based on customer data.
    
    Args:
        tariff_type: Current tariff type
        energy_usage: Monthly energy usage in kWh
        peak_usage_time: When customer uses most energy
        
    Returns:
        str: Recommended plan name
    """
    if peak_usage_time and "evening" in peak_usage_time.lower():
        return "Octopus Go"
    elif energy_usage > 400:
        return "Super Green Octopus"
    elif "variable" in tariff_type.lower():
        return "GreenFlex"
    else:
        return "Agile Octopus"

def estimate_potential_savings(tariff_type: str, energy_usage: int) -> int:
    """
    Estimate potential savings percentage based on current tariff and usage.
    
    Args:
        tariff_type: Current tariff type
        energy_usage: Monthly energy usage in kWh
        
    Returns:
        int: Estimated savings percentage
    """
    if "standard variable" in tariff_type.lower():
        if energy_usage > 500:
            return 18
        elif energy_usage > 300:
            return 15
        else:
            return 12
    elif "fixed" in tariff_type.lower():
        if energy_usage > 400:
            return 10
        else:
            return 8
    elif "economy 7" in tariff_type.lower():
        return 14
    else:
        return 10  # Default savings estimate


