📘 FastAPI Calculator API — Module 12

A secure, modular, test-driven REST API built with FastAPI, SQLAlchemy, PostgreSQL, Docker, and JWT authentication.

This project implements a calculation service (addition, subtraction, multiplication, division) with full user registration, authentication, token management, and CRUD operations for saved calculations.
It includes complete unit, integration, and end-to-end tests, along with production-ready Docker support.

🚀 Features
🔐 User Authentication

Register new users

Login with username or email

Secure password hashing (bcrypt)

JWT Access + Refresh tokens

Token expiration and validation

Redis-based blacklist for logout

🧮 Calculator Operations

Supported operations:

Addition

Subtraction

Multiplication

Division (with zero-division handling)

📦 Calculation Management

Authenticated users can:

Create a calculation

Retrieve all calculations

Get a calculation by ID

Update calculation inputs

Delete a calculation

🛠 Technology Stack

FastAPI

PostgreSQL

SQLAlchemy ORM

Docker & Docker Compose

Uvicorn

Redis (via redis.asyncio)

Pytest (unit, integration, e2e)

📂 Project Structure
app/
 ├── auth/
 ├── core/
 ├── models/
 ├── schemas/
 ├── operations/
 ├── main.py
 ├── database.py
 └── database_init.py
tests/
 ├── unit/
 ├── integration/
 └── e2e/
Dockerfile
docker-compose.yml
README.md

🐳 Run with Docker (Recommended)
1. Build and start all services
docker compose up -d


Services started:

Service	Port	Description
FastAPI	8000	API server
PostgreSQL	5432	Main DB
PGAdmin	5050	GUI DB management
🧪 Running Tests
Run all tests (unit + integration + e2e):
pytest -v

Run only integration tests:
pytest tests/integration -v

Run only user auth tests:
pytest tests/integration/test_user_auth.py -v


The project requires all tests to pass for full credit.

📘 API Documentation

Once running, visit:

👉 Swagger UI
http://localhost:8000/docs

👉 OpenAPI JSON
http://localhost:8000/openapi.json

👉 Health Check
http://localhost:8000/health

🧑‍💻 Development (Running Locally)
1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

2. Install requirements
pip install -r requirements.txt

3. Run the app
uvicorn app.main:app --reload

🗄 Database Access (PGAdmin)

Visit:

http://localhost:5050

Use the credentials in .env.

🔑 Environment Variables

Your .env file should include:

DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin

🧺 DockerHub Image

Pull this project from DockerHub:

docker pull msaju20/module12_is601
