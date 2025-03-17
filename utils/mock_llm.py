# utils/mock_llm.py

class MockLLM:
    """
    Mock LLM implementation that simulates responses without requiring API access.
    For demonstration and testing purposes only.
    """
    
    def __init__(self, model_name="mock-gpt-4", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        
    def invoke(self, prompt):
        """
        Simulate an LLM response based on the content of the prompt.
        In a real implementation, this would call the actual LLM API.
        """
        if "analyze customer data" in prompt.lower():
            return self._generate_customer_analysis()
        elif "generate personalized marketing email" in prompt.lower():
            return self._generate_email_draft()
        elif "optimize and refine" in prompt.lower():
            return self._generate_refined_email()
        else:
            return "This is a simulated response. In production, this would connect to an actual LLM API."
    
    def _generate_customer_analysis(self):
        """Generate a mock customer analysis response"""
        return """
Based on the customer data analysis, here are the key insights:

1. This customer has higher than average energy usage during evening hours (7pm-11pm), suggesting they might benefit from an Economy 7 tariff or time-of-use optimization.

2. Their location in London indicates they're in an area with high adoption of smart home technology and environmental consciousness.

3. Their current Standard Variable tariff is not optimized for their usage patterns, which show consistency month-to-month.

4. Given their energy consumption and current tariff, there's potential for 12-15% savings by switching to the GreenFlex plan.

5. Customer history shows interest in renewable energy options but concern about initial costs - messaging should emphasize immediate savings alongside environmental benefits.

Recommended messaging angles:
- Focus on immediate cost savings with specific numbers
- Highlight the simplicity of switching plans
- Emphasize smart energy management through the app
- Include specific environmental impact metrics (e.g., carbon reduction)

Suggested tone: Data-driven but friendly, emphasizing both practical benefits and environmental impact.
        """
    
    def _generate_email_draft(self):
        """Generate a mock email draft response"""
        return """
Subject: Alex, Save 15% on Your Energy Bills with Our GreenFlex Plan

Hi Alex,

We've been looking at your energy usage on your Standard Variable tariff (around 350 kWh monthly), and noticed something interesting: you're using most energy during evening hours.

Great news! By switching to our GreenFlex plan, you could save approximately 15% on your monthly bills while supporting renewable energy. Based on your usage patterns, this could mean about £180 in savings over the next year.

Why GreenFlex makes sense for you:
- Smart time-of-use rates that match your evening usage pattern
- 100% renewable electricity at competitive rates
- Easy energy tracking through our top-rated app
- No exit fees or long-term commitments

It takes just 2 minutes to switch online, and we'll handle everything else.

[Check Your Personalized Savings]

Warmly,
The Octopus Energy Team
        """
    
    def _generate_refined_email(self):
        """Generate a mock refined email response"""
        return """
Subject: Alex, Cut Your Evening Energy Costs by 15% This Month

Hi Alex,

Looking at your recent energy usage, I noticed you're using most power during evenings on your Standard Variable tariff. This presents a perfect opportunity!

Switch to our GreenFlex plan and save 15% on your monthly bills – that's around £180 over the next year based on your 350 kWh monthly usage. Plus, you'll be powering your home with 100% renewable electricity.

Perfect for your lifestyle:
- Lower rates during your actual usage hours
- Real-time consumption tracking in our simple app
- 100% green energy without the premium price
- No contract lock-in – flexibility guaranteed

Take 2 minutes to switch now and start saving immediately.

[See Your Exact Savings]

The Octopus Energy Team
        """