# Add this route to app.py

@app.route('/demo')
def demo():
    """Demo mode that walks through the prompt engineering process"""
    return render_template('demo.html', model_name=SELECTED_MODEL)