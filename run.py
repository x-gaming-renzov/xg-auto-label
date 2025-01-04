from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

import test

# Create a Flask application instance
app = Flask(__name__)

# Define the /process endpoint
@app.route('/process', methods=['POST'])
def process_task():
    try:
        # Parse JSON request data
        data = request.get_json()
        
        # Validate the task_id argument
        if not data or 'task_id' not in data:
            return jsonify({"error": "Missing required argument: task_id"}), 400
        
        task_id = data['task_id']

        if not isinstance(task_id, str):
            return jsonify({"error": "task_id must be a string"}), 400

        # Call the function with task_id
        result = test.process_task_completion(task_id)

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

# The app is ready to be used with gunicorn without binding any ports or hosts
