# Entrepreneurship Platform Backend (FastAPI)

Python FastAPI backend for the Entrepreneurship Platform with AI-powered file generation.

## Technology Stack

- **Python 3.11**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database
- **Uvicorn** - ASGI server
- **OpenAI API** - AI-powered file generation
- **Pydantic** - Data validation

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session management
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── project.py       # Project model
│   │   ├── competition.py   # Competition model
│   │   ├── generated_file.py # Generated file model
│   │   └── generation_log.py # Generation log model
│   ├── repositories/        # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── file_repository.py
│   │   └── log_repository.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   └── file_generation_service.py # OpenAI integration
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── projects.py      # Project management routes
│       ├── competitions.py  # Competition routes
│       └── files.py         # File generation and download routes
├── data/                    # SQLite database storage
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── seed_competitions.py    # Script to seed competition data
├── update_competition_prompts.py # Script to update competition prompts
└── README.md
```

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export DATABASE_URL=sqlite:///./data/app.db
export OPENAI_API_KEY=your_openai_api_key_here
```

Note: SQLite database will be created automatically if it doesn't exist.

3. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

Build and run with Docker Compose:
```bash
docker compose up --build
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

### Projects
- `GET /api/projects` - Get all projects for authenticated user
- `GET /api/projects/{id}` - Get a specific project
- `POST /api/projects` - Create a new project
- `PUT /api/projects/{id}` - Update a project
- `DELETE /api/projects/{id}` - Delete a project

### Competitions
- `GET /api/competitions` - Get all available competitions
- `GET /api/competitions/{id}` - Get a specific competition

### Files
- `POST /api/files/generate/{project_id}` - Generate files for a project (background task)
- `POST /api/files/generate/{project_id}/file/{filename}` - Regenerate a specific file
- `GET /api/files/project/{project_id}` - Get all files for a project
- `GET /api/files/{file_id}/content` - Get file content for preview
- `GET /api/files/{file_id}/download` - Download a specific file
- `GET /api/files/project/{project_id}/download-all` - Download all files as ZIP
- `GET /api/files/project/{project_id}/logs` - Get generation logs for a project

## Environment Variables

- `DATABASE_URL` - SQLite database connection string (default: `sqlite:///./data/app.db`)
- `OPENAI_API_KEY` - OpenAI API key for file generation (required)

## Database

The application uses SQLite, which stores the database file locally. The database file will be created automatically in the `data/` directory when the application starts.

### Models

- **User**: User accounts with authentication
- **Project**: Entrepreneurship projects with idea descriptions
- **Competition**: Entrepreneurship competitions with custom prompts
- **GeneratedFile**: AI-generated files (pitch decks, business plans, etc.)
- **GenerationLog**: Real-time logs for file generation process

### Seeding Data

To populate the database with competition data:

```bash
python seed_competitions.py
```

Or in Docker:
```bash
docker compose exec backend python seed_competitions.py
```

This will add 20+ entrepreneurship competitions with custom prompts for file generation.

## File Generation

The backend integrates with OpenAI API to generate competition documents. When a project is created or files are regenerated, the system:

1. Retrieves the project and competition details
2. Builds a custom prompt based on the competition requirements
3. Calls OpenAI API to generate the required files
4. Parses the response and saves files to the database
5. Provides real-time logs of the generation process

Generated files include:
- Pitch Deck (markdown)
- Business Plan (markdown)
- Executive Summary (text)
- Financial Plan (markdown)

## API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
