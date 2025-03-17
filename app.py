from flask import Flask, render_template, request, jsonify
import os
import json

from utils.logger import get_logger
from utils.mock_llm import MockLLM
from schemas.customer import CustomerProfile
from schemas.email import EmailCampaign
from config.settings import select_production_model

# Create Flask application
app = Flask(__name__)

# Initialize logger
logger = get_logger(__name__)

# Initialize the mock LLM for demo purposes
SELECTED_MODEL = select_production_model()
mock_llm = MockLLM(model_name=SELECTED_MODEL)

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html', model_name=SELECTED_MODEL)

@app.route('/demo')
def demo():
    """Demo mode that walks through the prompt engineering process"""
    # Make sure you're not restricting access in any way
    return render_template('demo.html', model_name=SELECTED_MODEL)

@app.route('/assistant')
def assistant():
    """Marketing assistant chat interface"""
    return render_template('assistant.html', model_name=SELECTED_MODEL)

@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """API endpoint to generate email based on customer data"""
    try:
        # Get customer data from request
        customer_data = request.json
        
        # Create CustomerProfile object
        customer = CustomerProfile(**customer_data)
        
        # Generate mock responses for each stage
        customer_insights = mock_llm.invoke("analyze customer data")
        email_draft = mock_llm.invoke("generate personalized marketing email")
        final_email = mock_llm.invoke("optimize and refine marketing email")
        
        # Extract subject line
        if "Subject:" in final_email:
            email_subject = final_email.split("Subject:")[1].split("\n")[0].strip()
        else:
            email_subject = f"Special Offer for {customer.name} from Octopus Energy"
        
        # Return generated email
        return jsonify({
            "email_subject": email_subject,
            "email_body": final_email,
            "customer_insights": customer_insights,
            "draft_version": email_draft,
            "final_version": final_email
        })
    except Exception as e:
        logger.error(f"Error generating email: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatting with the marketing assistant agent"""
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        # Generate mock response based on the message content
        response = mock_llm.invoke(user_message)
        
        # Return agent response
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/models', methods=['GET'])
def get_models():
    """API endpoint to get list of available models"""
    from config.settings import AVAILABLE_MODELS
    return jsonify({"models": AVAILABLE_MODELS})

if __name__ == '__main__':
    print("Starting Octopus Energy Email Marketing Assistant...")
    print("Open http://localhost:5000 in your browser")
    print("For the demonstration of prompt engineering workflow, visit http://localhost:5000/demo")
    app.run(debug=True, port=5000)