# Entrepreneurship Platform Backend (FastAPI)

Python FastAPI backend for the Entrepreneurship Platform.

## Technology Stack

- **Python 3.11**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database
- **Uvicorn** - ASGI server

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session management
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── project.py
│   ├── repositories/        # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── project_repository.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── project_service.py
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── auth.py
│       └── projects.py
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md

```

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set environment variables:
```bash
export DATABASE_URL=sqlite:///./data/app.db
```
Note: SQLite database will be created automatically if it doesn't exist.

3. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## API Endpoints

- `POST /api/auth/login` - User login (returns dummy token)
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create a new project

## Environment Variables

- `DATABASE_URL` - SQLite database connection string (default: `sqlite:///./data/app.db`)

## Database

The application uses SQLite, which stores the database file locally. The database file will be created automatically in the `data/` directory when the application starts.

