### FastAPI Project
This is a FastAPI-based web application for managing users and tasks. It provides a RESTful API for creating, reading, updating, and deleting users and tasks.

## Features
User authentication and authorization using OAuth2 and JWT
CRUD operations for users and tasks
Secure password hashing
SQLAlchemy ORM for database interactions
Middleware for handling database sessions
## Installation
Prerequisites
Python 3.7 or higher
SQLite (or another database of your choice)
Virtual environment (recommended)
## Setup
# Clone the repository:

```bash
git clone https://github.com/mickaaDev/To-Do-List.git
cd <repository-directory>
```

# Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

# Install dependencies:

```bash
pip install -r requirements.txt
```
# Run database migrations (if any):

For SQLite, the database file will be created automatically.
# Start the application:

```bash
uvicorn api.main:app --reload
```
# Access the API documentation:

Open your browser and go to http://127.0.0.1:8000/docs for the Swagger UI or http://127.0.0.1:8000/redoc for ReDoc.


## API Endpoints
# Authentication
POST /token: Obtain a JWT token for authentication.
# Users
POST /users/: Create a new user.
GET /users/: Get a list of all users.
GET /users/{user_id}: Get details of a specific user.
DELETE /users/{user_id}: Delete a user.
# Tasks
POST /users/{user_id}/items/: Create a task for a specific user.
GET /tasks/: Get a list of all tasks.
DELETE /tasks/{task_id}: Delete a task.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project has not been licensed yet.

## Acknowledgements
[FastAPI](https://fastapi.tiangolo.com/)
[SQLAlchemy](https://www.sqlalchemy.org/)
[Uvicorn](https://www.uvicorn.org/)

