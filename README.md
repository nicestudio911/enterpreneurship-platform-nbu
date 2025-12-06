# Entrepreneurship Platform

A full-stack web application for managing entrepreneurship projects and generating competition materials using AI, built with React, FastAPI, and SQLite.

## Architecture

- **Frontend**: React 18 with TypeScript, Vite, and React Router
- **Backend**: FastAPI with Python 3.11
- **Database**: SQLite
- **AI Integration**: OpenAI API for generating competition documents
- **Containerization**: Docker and Docker Compose

## Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── api/             # API client and service functions
│   │   │   ├── auth.ts      # Authentication API
│   │   │   ├── projects.ts  # Projects API
│   │   │   ├── competitions.ts # Competitions API
│   │   │   ├── files.ts     # File generation and download API
│   │   │   └── client.ts    # Axios client configuration
│   │   ├── components/      # Reusable React components
│   │   │   ├── Navigation.tsx
│   │   │   └── Navigation.css
│   │   ├── pages/           # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Dashboard.css
│   │   │   ├── ProjectCreate.tsx
│   │   │   ├── ProjectCreate.css
│   │   │   ├── ProjectView.tsx
│   │   │   └── ProjectView.css
│   │   ├── App.tsx          # Main application component with routing
│   │   ├── App.css          # Global app styles
│   │   ├── index.css        # Design system and base styles
│   │   └── main.tsx         # Application entry point
│   ├── Dockerfile           # Frontend Docker configuration
│   ├── nginx.conf           # Nginx configuration for production
│   ├── package.json         # Frontend dependencies
│   └── vite.config.ts       # Vite configuration
│
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── routers/         # API route handlers
│   │   │   ├── auth.py      # Authentication routes
│   │   │   ├── projects.py  # Project management routes
│   │   │   ├── competitions.py # Competition routes
│   │   │   └── files.py     # File generation and download routes
│   │   ├── services/        # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── project_service.py
│   │   │   └── file_generation_service.py # OpenAI integration
│   │   ├── repositories/    # Data access layer
│   │   │   ├── user_repository.py
│   │   │   ├── project_repository.py
│   │   │   ├── file_repository.py
│   │   │   └── log_repository.py
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── competition.py
│   │   │   ├── generated_file.py
│   │   │   └── generation_log.py
│   │   ├── database.py      # Database configuration
│   │   └── main.py          # FastAPI application entry point
│   ├── data/                # SQLite database storage
│   ├── Dockerfile           # Backend Docker configuration
│   ├── requirements.txt     # Python dependencies
│   ├── seed_competitions.py # Script to seed competition data
│   ├── update_competition_prompts.py # Script to update competition prompts
│   └── README.md            # Backend documentation
│
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables (not in git)
└── README.md               # This file

```

## Features

### Core Features

- **User Authentication**: Login and registration with JWT tokens
- **Project Management**: Create, view, edit, and delete entrepreneurship projects
- **Competition Integration**: Select from 20+ entrepreneurship competitions with custom prompts
- **AI-Powered File Generation**: Automatically generate competition documents using OpenAI:
  - Pitch Deck
  - Business Plan
  - Executive Summary
  - Financial Plan
- **File Management**: View, download, and regenerate generated files
- **Real-time Generation Logs**: Monitor file generation progress in real-time
- **File Preview**: Preview markdown files before downloading
- **Modern UI**: Standardized design system with responsive layout

### API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

#### Projects
- `GET /api/projects` - Get all projects for the authenticated user
- `GET /api/projects/{id}` - Get a specific project
- `POST /api/projects` - Create a new project
- `PUT /api/projects/{id}` - Update a project
- `DELETE /api/projects/{id}` - Delete a project

#### Competitions
- `GET /api/competitions` - Get all available competitions
- `GET /api/competitions/{id}` - Get a specific competition

#### Files
- `POST /api/files/generate/{project_id}` - Generate files for a project
- `POST /api/files/generate/{project_id}/file/{filename}` - Regenerate a specific file
- `GET /api/files/project/{project_id}` - Get all files for a project
- `GET /api/files/{file_id}/content` - Get file content for preview
- `GET /api/files/{file_id}/download` - Download a specific file
- `GET /api/files/project/{project_id}/download-all` - Download all files as ZIP
- `GET /api/files/project/{project_id}/logs` - Get generation logs for a project

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- OpenAI API Key (for file generation feature)

## Getting Started

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/nicestudio911/enterpreneurship-platform-nbu.git
cd enterpreneurship-platform-nbu
```

2. Create a `.env` file in the root directory:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

3. Start all services using Docker Compose:
```bash
docker compose up --build
```

This command will:
- Build the frontend and backend Docker images
- Start the FastAPI backend
- Start the React frontend with Nginx
- Initialize SQLite database automatically

4. (Optional) Seed competition data:
```bash
docker compose exec backend python seed_competitions.py
```

5. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/docs (FastAPI auto-generated docs)

### Stopping the Application

To stop all services:
```bash
docker compose down
```

To stop and remove all data (including database volumes):
```bash
docker compose down -v
```

## Development

### Frontend Development

To run the frontend in development mode:

```bash
cd frontend
npm install
npm run dev
```

The development server will start at http://localhost:5173

**Note**: You'll need to set `VITE_API_URL=http://localhost:8000/api` in a `.env` file in the frontend directory for API calls to work in development mode.

### Backend Development

To run the backend locally:

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./data/app.db
export OPENAI_API_KEY=your_openai_api_key_here
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The SQLite database will be created automatically in the `data/` directory.

### Environment Variables

#### Root `.env` file (for Docker Compose)
```
OPENAI_API_KEY=your_openai_api_key_here
```

#### Frontend `.env` (for local development)
```
VITE_API_URL=http://localhost:8000/api
```

#### Backend Environment Variables
- `DATABASE_URL` - SQLite database connection string (default: `sqlite:///./data/app.db`)
- `OPENAI_API_KEY` - OpenAI API key for file generation (required)

## Database

The application uses SQLite, which is a file-based database. The database file is automatically created when you run the application for the first time.

### Database Location
- **Local Development**: `backend/data/app.db`
- **Docker**: The database file is persisted in `backend/data/` directory (mounted as a volume)

The database schema is automatically created by SQLAlchemy based on the model definitions when the application starts.

### Seeding Data

To populate the database with competition data:

```bash
docker compose exec backend python seed_competitions.py
```

This will add 20+ entrepreneurship competitions with custom prompts for file generation.

## Technology Stack

### Frontend
- React 18.2
- TypeScript 5.3
- Vite 5.0
- React Router 6.20
- Axios 1.6
- React Markdown 9.1 (for file preview)
- Remark GFM 4.0 (GitHub Flavored Markdown support)
- Nginx (for production)

### Backend
- Python 3.11
- FastAPI 0.104
- SQLAlchemy 2.0
- Uvicorn (ASGI server)
- Pydantic 2.5 (data validation)
- OpenAI API 1.12+ (for AI-powered file generation)
- Python-dotenv 1.0 (environment variable management)

### Infrastructure
- Docker
- Docker Compose
- SQLite (file-based database)

## Project Status

This is a fully functional application with the following implemented features:

✅ User authentication and registration  
✅ Project CRUD operations  
✅ Competition selection and management  
✅ AI-powered file generation (Pitch Deck, Business Plan, Executive Summary, Financial Plan)  
✅ Real-time generation progress tracking  
✅ File preview and download  
✅ Modern, responsive UI with standardized design system  
✅ Project editing and regeneration  

## License

This project is part of the NBU Entrepreneurship Platform initiative.
