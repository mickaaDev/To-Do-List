# FastAPI Project
This is a FastAPI-based web application for managing users and tasks. It provides a RESTful API for creating, reading, updating, and deleting users and tasks.

## Features
User authentication and authorization using OAuth2 and JWT
CRUD operations for users and tasks
Secure password hashing
SQLAlchemy ORM for database interactions
Middleware for handling database sessions
## Installation
Prerequisites
Docker and Docker Compose
Python 3.7 or higher (only if running locally without Docker)
SQLite (or another database of your choice)
Virtual environment (recommended for local development)
## Setup
## Clone the repository:

```bash
git clone https://github.com/mickaaDev/To-Do-List.git
cd <repository-directory>
```

## Set up the environment variables:

```bash
cp .env.example .env
```

Edit the .env file and fill in your specific values:

```bash
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
```

## Start the application using Docker Compose:

```bash
docker-compose up --build
```
This will build the Docker images and start the application along with the necessary services like the PostgreSQL database.

## Access the API documentation:

Open your browser and go to http://127.0.0.1:8000/docs for the Swagger UI or http://127.0.0.1:8000/redoc for ReDoc.


## API Endpoints
## Authentication
POST /token: Obtain a JWT token for authentication.
## Users
POST /users/: Create a new user.

GET /users/: Get a list of all users.

GET /users/{user_id}: Get details of a specific user.

DELETE /users/{user_id}: Delete a user.
## Tasks
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

