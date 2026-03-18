## TO-DO List manager( TASK MANAGER) + API AUTH

from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

# Swagger initialization
swagger = Swagger(app)

# In-memory database
tasks = []
task_id_counter = 1

# API Key
API_KEY = "12345"

# Function to check API key
def check_api_key():
    key = request.headers.get("x-api-key")
    return key == API_KEY

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks
    ---
    parameters:
      - name: x-api-key
        in: header
        type: string
        required: true
        description: API key for authentication
    responses:
      200:
        description: List of tasks
      401:
        description: Unauthorized
    """

    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single task
    ---
    parameters:
      - name: x-api-key
        in: header
        type: string
        required: true
        description: API key for authentication
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task found
      404:
        description: Task not found
      401:
        description: Unauthorized
    """

    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    ---
    parameters:
      - name: x-api-key
        in: header
        type: string
        required: true
        description: API key
      - name: task
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Complete REST API assignment"
    responses:
      201:
        description: Task created
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
    global task_id_counter

    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": task_id_counter,
        "title": data["title"],
        "status": "pending"
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a task
    ---
    parameters:
      - name: x-api-key
        in: header
        type: string
        required: true
        description: API key
      - name: task_id
        in: path
        type: integer
        required: true
      - name: task
        in: body
        schema:
          type: object
          properties:
            title:
              type: string
            status:
              type: string
              example: completed
    responses:
      200:
        description: Task updated
      404:
        description: Task not found
      401:
        description: Unauthorized
    """

    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["status"] = data.get("status", task["status"])
            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task
    ---
    parameters:
      - name: x-api-key
        in: header
        type: string
        required: true
        description: API key
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task deleted
      404:
        description: Task not found
      401:
        description: Unauthorized
    """

    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)