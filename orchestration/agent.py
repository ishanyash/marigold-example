# orchestration/agent.py

from langchain.agents import Tool, AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from orchestration.workflow import EmailCampaignWorkflow
from prompts.system_prompts import ENERGY_MARKETING_EXPERT_PROMPT
from schemas.customer import CustomerProfile
from utils.logger import get_logger

logger = get_logger(__name__)

class MarketingEmailAgent:
    """
    Intelligent agent that assists marketers in generating and refining
    email campaigns for Octopus Energy customers.
    """
    
    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Initialize workflow for email generation
        self.email_workflow = EmailCampaignWorkflow(model_name=model_name)
        
        # Build the agent
        self.agent_executor = self._build_agent()
    
    def _build_agent(self):
        """Build the marketing assistant agent with appropriate tools"""
        
        # Define tools available to the agent
        tools = [
            Tool(
                name="generate_email_campaign",
                func=self._generate_email,
                description="Generate a personalized marketing email for an Octopus Energy customer. "
                           "Input should be a JSON with customer details including name, tariff_type, energy_usage, "
                           "potential_savings, recommended_plan, location, and peak_usage_time."
            ),
            Tool(
                name="analyze_customer_data",
                func=self._analyze_customer,
                description="Analyze a customer's energy usage data to provide personalized insights. "
                           "Input should be a JSON with customer details including name, tariff_type, energy_usage, "
                           "location, and peak_usage_time."
            ),
            Tool(
                name="refine_email_content",
                func=self._refine_email,
                description="Refine and improve an existing email draft. Input should be a JSON with "
                           "email_draft, customer_name, and tariff_type fields."
            ),
            Tool(
                name="get_email_templates",
                func=self._get_templates,
                description="Get available email templates for different types of campaigns like "
                           "new plans, seasonal offers, or retention. Input can be template type or 'all'."
            )
        ]
        
        # System message for the agent
        system_message = f"""
        {ENERGY_MARKETING_EXPERT_PROMPT}
        
        You are a marketing email assistant for Octopus Energy marketers. Your job is to help them:
        1. Generate personalized marketing emails for customers
        2. Analyze customer energy data to provide insights
        3. Refine existing email drafts
        4. Access email templates for different campaign types
        
        IMPORTANT GUIDELINES:
        - Always ask for necessary customer details before generating emails
        - Ensure all emails follow Octopus Energy's brand voice
        - Prioritize personalization in all communications
        - Always check if customer data is available before proceeding
        - When generating emails, maintain a friendly, non-corporate tone
        - Focus on both cost savings and environmental benefits
        """
        
        # Create the agent
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=tools,
            system_message=SystemMessage(content=system_message)
        )
        
        # Create the agent executor
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def run(self, input_query):
        """
        Run the agent with a user query
        
        Args:
            input_query: String query from the marketer
            
        Returns:
            Agent response
        """
        try:
            logger.info(f"Running agent with input: {input_query[:100]}...")
            response = self.agent_executor.invoke({"input": input_query})
            return response["output"]
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            return f"I encountered an error processing your request: {str(e)}"
    
    def _generate_email(self, customer_json_str):
        """Tool function to generate an email campaign"""
        try:
            # Parse customer data from JSON string
            import json
            customer_data = json.loads(customer_json_str)
            
            # Create CustomerProfile object
            customer = CustomerProfile(**customer_data)
            
            # Generate the campaign
            campaign = self.email_workflow.generate_campaign(customer)
            
            return campaign.email_body
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return f"Error generating email: {str(e)}"
    
    def _analyze_customer(self, customer_json_str):
        """Tool function to analyze customer data"""
        try:
            # Parse customer data from JSON string
            import json
            customer_data = json.loads(customer_json_str)
            
            # Create CustomerProfile object
            customer = CustomerProfile(**customer_data)
            
            # Use the analysis chain directly
            analysis_input = {
                "customer_name": customer.name,
                "tariff_type": customer.tariff_type,
                "energy_usage": customer.energy_usage,
                "location": customer.location,
                "peak_usage_time": customer.peak_usage_time,
                "customer_history": customer.history_summary if hasattr(customer, "history_summary") else ""
            }
            
            result = self.email_workflow.analysis_chain.invoke(analysis_input)
            return result["customer_insights"]
        except Exception as e:
            logger.error(f"Error analyzing customer: {str(e)}")
            return f"Error analyzing customer data: {str(e)}"
    
    def _refine_email(self, input_json_str):
        """Tool function to refine an email draft"""
        try:
            # Parse input data from JSON string
            import json
            input_data = json.loads(input_json_str)
            
            # Use the refinement chain directly
            refinement_input = {
                "email_draft": input_data["email_draft"],
                "customer_name": input_data["customer_name"],
                "tariff_type": input_data["tariff_type"]
            }
            
            result = self.email_workflow.refinement_chain.invoke(refinement_input)
            return result["final_email"]
        except Exception as e:
            logger.error(f"Error refining email: {str(e)}")
            return f"Error refining email: {str(e)}"
    
    def _get_templates(self, template_type="all"):
        """Tool function to provide email templates"""
        templates = {
            "new_plan": """
                Subject: {customer_name}, Introducing Our New {plan_name} Plan!
                
                Hi {customer_name},
                
                We've just launched our new {plan_name} designed specifically for customers like you using around {energy_usage} kWh monthly.
                
                This plan offers:
                • {feature_1}
                • {feature_2}
                • {feature_3}
                
                Based on your usage, you could save approximately {potential_savings}% compared to your current {tariff_type} tariff.
                
                Ready to learn more? Check your personalized savings:
                
                [Check My Savings]
                
                The Octopus Energy Team
            """,
            "seasonal": """
                Subject: Prepare for {season}, {customer_name} - Special Offer Inside
                
                Hi {customer_name},
                
                With {season} approaching, we've analyzed your {tariff_type} plan and found you could optimize your energy usage to save during the {season} months.
                
                Our {season} {plan_name} offers:
                • {seasonal_benefit_1}
                • {seasonal_benefit_2}
                • Up to {potential_savings}% savings
                
                Your current usage of {energy_usage} kWh would cost less with our seasonal adjustments!
                
                Take 2 minutes to switch before {deadline}:
                
                [Switch to {Season} Plan]
                
                Stay {warm/cool} and save,
                Octopus Energy
            """,
            "retention": """
                Subject: We'd Love You to Stay, {customer_name}
                
                Hi {customer_name},
                
                We noticed you've been with us on the {tariff_type} tariff for {duration}, and we wanted to thank you for choosing Octopus Energy.
                
                To show our appreciation, we've prepared a special loyalty offer:
                • {loyalty_benefit_1}
                • {loyalty_benefit_2}
                • An extra {loyalty_discount}% off your current rate
                
                With your average usage of {energy_usage} kWh, this means approximately £{savings_amount} in additional savings annually.
                
                Activate your loyalty rewards here:
                
                [Claim My Loyalty Offer]
                
                Thank you for being an amazing customer!
                The Octopus Energy Team
            """
        }
        
        if template_type.lower() == "all":
            return json.dumps(templates, indent=2)
        elif template_type.lower() in templates:
            return templates[template_type.lower()]
        else:
            return f"Template '{template_type}' not found. Available templates: {', '.join(templates.keys())}"


# app.py

from flask import Flask, render_template, request, jsonify
import os
import json

from orchestration.agent import MarketingEmailAgent
from schemas.customer import CustomerProfile
from config.settings import select_production_model

app = Flask(__name__)

# Initialize the marketing agent with the best model
SELECTED_MODEL = select_production_model()
agent = MarketingEmailAgent(model_name=SELECTED_MODEL)

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html', model_name=SELECTED_MODEL)

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """API endpoint to generate email based on customer data"""
    try:
        # Get customer data from request
        customer_data = request.json
        
        # Create CustomerProfile object
        customer = CustomerProfile(**customer_data)
        
        # Generate campaign
        email_workflow = agent.email_workflow
        campaign = email_workflow.generate_campaign(customer)
        
        # Return generated email
        return jsonify({
            "email_subject": campaign.email_subject,
            "email_body": campaign.email_body,
            "customer_insights": campaign.customer_insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatting with the marketing assistant agent"""
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        # Run the agent with the user message
        response = agent.run(user_message)
        
        # Return agent response
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/models', methods=['GET'])
def get_models():
    """API endpoint to get list of available models"""
    from config.settings import AVAILABLE_MODELS
    return jsonify({"models": AVAILABLE_MODELS})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# templates/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Octopus Energy Email Assistant</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding-top: 20px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 1200px;
        }
        .header {
            background-color: #4c12a1;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 15px;
            background-color: white;
        }
        .message {
            padding: 10px 15px;
            border-radius: 18px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .user-message {
            background-color: #e9ecef;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .assistant-message {
            background-color: #4c12a1;
            color: white;
            margin-right: auto;
            border-bottom-left-radius: 5px;
        }
        .input-group {
            margin-top: 15px;
        }
        .customer-form {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .email-preview {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            white-space: pre-line;
        }
        .nav-tabs .nav-link.active {
            background-color: #4c12a1;
            color: white;
        }
        .nav-tabs .nav-link {
            color: #4c12a1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header text-center">
            <h1>Octopus Energy Marketing Email Assistant</h1>
            <p>Using LangChain and {{ model_name }} to generate personalized marketing emails</p>
        </div>
        
        <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="generator-tab" data-bs-toggle="tab" data-bs-target="#generator" type="button" role="tab" aria-controls="generator" aria-selected="true">Email Generator</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="assistant-tab" data-bs-toggle="tab" data-bs-target="#assistant" type="button" role="tab" aria-controls="assistant" aria-selected="false">Marketing Assistant</button>
            </li>
        </ul>
        
        <div class="tab-content" id="myTabContent">
            <!-- Email Generator Tab -->
            <div class="tab-pane fade show active" id="generator" role="tabpanel" aria-labelledby="generator-tab">
                <div class="row">
                    <div class="col-md-6">
                        <div class="customer-form">
                            <h3>Customer Details</h3>
                            <form id="customerForm">
                                <div class="mb-3">
                                    <label for="customerName" class="form-label">Customer Name</label>
                                    <input type="text" class="form-control" id="customerName" required>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="tariffType" class="form-label">Current Tariff</label>
                                            <select class="form-control" id="tariffType" required>
                                                <option value="Standard Variable">Standard Variable</option>
                                                <option value="Fixed Rate">Fixed Rate</option>
                                                <option value="Economy 7">Economy 7</option>
                                                <option value="Green Energy">Green Energy</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="energyUsage" class="form-label">Monthly Energy Usage (kWh)</label>
                                            <input type="number" class="form-control" id="energyUsage" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="location" class="form-label">Location</label>
                                            <input type="text" class="form-control" id="location">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="peakUsageTime" class="form-label">Peak Usage Time</label>
                                            <select class="form-control" id="peakUsageTime">
                                                <option value="Morning">Morning</option>
                                                <option value="Afternoon">Afternoon</option>
                                                <option value="Evening">Evening</option>
                                                <option value="Night">Night</option>
                                                <option value="Morning and Evening">Morning and Evening</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="potentialSavings" class="form-label">Potential Savings (%)</label>
                                            <input type="number" class="form-control" id="potentialSavings" required>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="recommendedPlan" class="form-label">Recommended Plan</label>
                                            <select class="form-control" id="recommendedPlan" required>
                                                <option value="Agile Octopus">Agile Octopus</option>
                                                <option value="Super Green Octopus">Super Green Octopus</option>
                                                <option value="Octopus Go">Octopus Go</option>
                                                <option value="GreenFlex">GreenFlex</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="customerHistory" class="form-label">Customer History (optional)</label>
                                    <textarea class="form-control" id="customerHistory" rows="3"></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">Generate Email</button>
                            </form>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="email-preview">
                            <h3>Generated Email</h3>
                            <div id="loadingIndicator" class="text-center d-none">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <p>Generating personalized email...</p>
                            </div>
                            <div id="emailResult">
                                <p class="text-muted">Fill out the customer details and click "Generate Email" to create a personalized marketing campaign.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Marketing Assistant Tab -->
            <div class="tab-pane fade" id="assistant" role="tabpanel" aria-labelledby="assistant-tab">
                <div class="row">
                    <div class="col-12">
                        <div class="chat-container" id="chatMessages">
                            <div class="message assistant-message">
                                Hi there! I'm your Octopus Energy Marketing Assistant. I can help you create personalized email campaigns, analyze customer data, refine email drafts, and provide email templates. How can I help you today?
                            </div>
                        </div>
                        <div class="input-group">
                            <input type="text" id="userMessage" class="form-control" placeholder="Type your message here...">
                            <button class="btn btn-primary" id="sendMessage">Send</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Email Generator Form
            const customerForm = document.getElementById('customerForm');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const emailResult = document.getElementById('emailResult');
            
            customerForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Show loading indicator
                loadingIndicator.classList.remove('d-none');
                emailResult.innerHTML = '';
                
                // Collect form data
                const customerData = {
                    customer_id: "WEB" + Math.floor(Math.random() * 10000),
                    name: document.getElementById('customerName').value,
                    tariff_type: document.getElementById('tariffType').value,
                    energy_usage: parseInt(document.getElementById('energyUsage').value),
                    potential_savings: parseInt(document.getElementById('potentialSavings').value),
                    recommended_plan: document.getElementById('recommendedPlan').value,
                    location: document.getElementById('location').value,
                    peak_usage_time: document.getElementById('peakUsageTime').value,
                    history_summary: document.getElementById('customerHistory').value
                };
                
                // Send API request
                fetch('/api/generate-email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(customerData)
                })
                .then(response => response.json())
                .then(data => {
                    // Hide loading indicator
                    loadingIndicator.classList.add('d-none');
                    
                    // Display results
                    if (data.error) {
                        emailResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    } else {
                        emailResult.innerHTML = `
                            <div class="card mb-3">
                                <div class="card-header bg-primary text-white">
                                    <strong>Subject:</strong> ${data.email_subject}
                                </div>
                                <div class="card-body">
                                    ${data.email_body.replace(/\n/g, '<br>')}
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <strong>Customer Insights</strong>
                                </div>
                                <div class="card-body">
                                    ${data.customer_insights.replace(/\n/g, '<br>')}
                                </div>
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    loadingIndicator.classList.add('d-none');
                    emailResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                });
            });
            
            // Chat Assistant
            const chatMessages = document.getElementById('chatMessages');
            const userMessage = document.getElementById('userMessage');
            const sendMessage = document.getElementById('sendMessage');
            
            function addMessage(content, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
                messageDiv.textContent = content;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            function sendChatMessage() {
                const message = userMessage.value.trim();
                if (message) {
                    // Add user message to chat
                    addMessage(message, true);
                    userMessage.value = '';
                    
                    // Add typing indicator
                    const typingIndicator = document.createElement('div');
                    typingIndicator.className = 'message assistant-message';
                    typingIndicator.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Thinking...';
                    typingIndicator.id = 'typingIndicator';
                    chatMessages.appendChild(typingIndicator);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    // Send message to API
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Remove typing indicator
                        document.getElementById('typingIndicator').remove();
                        
                        // Add assistant response
                        if (data.error) {
                            addMessage(`Error: ${data.error}`, false);
                        } else {
                            addMessage(data.response, false);
                        }
                    })
                    .catch(error => {
                        document.getElementById('typingIndicator').remove();
                        addMessage(`Sorry, I encountered an error: ${error.message}`, false);
                    });
                }
            }
            
            sendMessage.addEventListener('click', sendChatMessage);
            userMessage.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendChatMessage();
                }
            });
        });
    </script>
</body>
</html>