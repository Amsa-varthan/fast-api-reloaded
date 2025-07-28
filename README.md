# FastAPI Job Portal API

This project is a backend for a job portal application, built with FastAPI and PostgreSQL. It includes a complete user registration and login system featuring phone OTP verification and JWT-based authentication.

---

## Features

-   User signup with phone number verification.
-   OTP generation and validation.
-   Secure password and token hashing.
-   JWT access and refresh token generation.
-   Database schema management with Alembic migrations.

## Project Structure


/
├── alembic/              # Alembic migration scripts
├── api/
│   └── routers/
│       └── auth.py       # Authentication API endpoints
├── venv/                 # Virtual environment
├── config.py             # Application configuration (DB URL, secrets)
├── database.py           # Database session setup
├── main.py               # Main FastAPI application entrypoint
├── models.py             # SQLAlchemy database models
├── requirements.txt      # Project dependencies
├── schemas.py            # Pydantic data validation schemas
├── security.py           # Security utilities (hashing, JWT, OTP)
└── alembic.ini           # Alembic configuration


---

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
-   Python 3.9+
-   PostgreSQL
-   Git

### 2. Clone the Repository
```bash
git clone [https://github.com/Amsa-varthan/fastapi-postgres-project.git](https://github.com/Amsa-varthan/fastapi-postgres-project.git)
cd fastapi-postgres-project

3. Create and Activate Virtual Environment

# Create the virtual environment
python -m venv venv

# Activate it (on Windows)
venv\Scripts\activate

4. Install Dependencies

Install all the required packages from the requirements.txt file.

pip install -r requirements.txt

5. Configure the Environment

    Open pgAdmin and create a new, empty database named myprojectdb.

    In the project, open the config.py file and replace "YOUR_PASSWORD" with your actual PostgreSQL password.

    Open the alembic.ini file and do the same for the sqlalchemy.url line.

6. Run Database Migrations

This command will create all the necessary tables in your database.

alembic upgrade head

How to Run the Application

With the virtual environment active, run the following command to start the FastAPI server:

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

You can access the interactive API documentation at http://127.0.0.1:8000/docs.
Terminal Commands Used

Here is a summary of all the key commands used to build this project:

# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install all packages from the requirements file
pip install -r requirements.txt

# (Individual package installation commands used during development)
# pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary pydantic-settings alembic
# pip install "python-jose[cryptography]" "passlib[bcrypt]" "pydantic[email]"

# 3. Run the server
uvicorn main:app --reload

# 4. Initialize Alembic (only done once)
alembic init alembic

# 5. Create a new database migration after changing models.py
alembic revision --autogenerate -m "Your migration message"

# 6. Apply migrations to the database
alembic upgrade head

