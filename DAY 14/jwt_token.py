from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

app = Flask(__name__)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "THE_HOUSE_OF_STARS"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Swagger configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "API with JWT Authentication",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <JWT_TOKEN>"
        }
    }
}

swagger = Swagger(app, template=swagger_template)

# In-memory database
tasks = []
task_id_counter = 1

# Dummy user
USER = {
    "username": "admin",
    "password": "1234"
}


# LOGIN ROUTE
@app.route("/login", methods=["POST"])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    parameters:
      - name: credentials
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: 1234
    responses:
      200:
        description: JWT token generated
      401:
        description: Invalid credentials
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    if data["username"] == USER["username"] and data["password"] == USER["password"]:
        token = create_access_token(identity=data["username"])
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401


# GET ALL TASKS
@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Get All Tasks
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: List of tasks
    """

    return jsonify(tasks)


# CREATE TASK
@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    """
    Create Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Complete Flask project
    responses:
      201:
        description: Task created
    """

    global task_id_counter

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title required"}), 400

    current_user = get_jwt_identity()

    new_task = {
        "id": task_id_counter,
        "title": data["title"],
        "status": "pending",
        "created_by": current_user
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201


# UPDATE TASK
@app.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Updated task title
            status:
              type: string
              example: completed
    responses:
      200:
        description: Task updated
      404:
        description: Task not found
    """

    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["status"] = data.get("status", task["status"])
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


# DELETE TASK
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: Task deleted
      404:
        description: Task not found
    """

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True,port=8000)