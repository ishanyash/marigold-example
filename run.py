# run.py

from app import app

if __name__ == "__main__":
    print("Starting Octopus Energy Email Marketing Assistant...")
    print("Open http://localhost:5000 in your browser")
    print("For the demonstration of prompt engineering workflow, visit http://localhost:5000/demo")
    app.run(debug=True, port=5000)