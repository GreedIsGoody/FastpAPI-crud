# Bookly CRUD API

An asynchronous REST API for book management (CRUD operations), built with a modern Python backend stack. The project features full Docker containerization and automated database migration management.

## 🛠 Tech Stack
* **Backend:** Python 3.14+ / FastAPI (Async mode)
* **Database:** PostgreSQL 15
* **ORM & Migrations:** SQLAlchemy (Async) + Alembic
* **Containerization:** Docker / Docker Compose

## 🚀 Key Features
* Full CRUD (Create, Read, Update, Delete) architecture for the application resources.
* Secure user authentication with password hashing.
* Automated interactive API documentation (Swagger UI / ReDoc / Postman).
* Complete infrastructure isolation using Docker containers.
* Automated Alembic database migrations applied on container startup.
* Testing by pytest and logging recorder what helps you to debug and see what your app is doing

## 📦 Local Setup & Installation

### 1. Clone the repository:
bash
git clone [https://github.com/GreedIsGoody/FastpAPI-crud.git]
cd FastpAPI-crud
2. Configure Environment Variables:
Create a .env file in the root directory of the project and add your database credentials (you can use .env.example as a template):

POSTGRES_USER={your_db_username}
POSTGRES_PASSWORD={your_db_password}
POSTGRES_DB= {your_db}
DATABASE_URL= {your_db_url}
3. Run the application via Docker Compose:
A single command will spin up the PostgreSQL database, link it to the FastAPI application, and automatically run all pending Alembic migrations:

Bash
docker-compose up -d --build
4. Verify the deployment:
Check the status of the containers to ensure everything is up and running smoothly:

Bash
docker-compose ps
📂 API Documentation
Once the containers are running successfully, the interactive API documentation and testing playgrounds are available at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
