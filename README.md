# Entrepreneurship Platform

A full-stack web application for managing entrepreneurship projects, built with React, FastAPI, and SQLite.

## Architecture

- **Frontend**: React 18 with TypeScript, Vite, and React Router
- **Backend**: FastAPI with Python 3.11
- **Database**: SQLite
- **Containerization**: Docker and Docker Compose

## Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── api/             # API client and service functions
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components (Login, Dashboard, ProjectCreate)
│   │   ├── App.tsx          # Main application component with routing
│   │   └── main.tsx         # Application entry point
│   ├── Dockerfile           # Frontend Docker configuration
│   ├── nginx.conf           # Nginx configuration for production
│   └── package.json         # Frontend dependencies
│
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic layer
│   │   ├── repositories/    # Data access layer
│   │   ├── models/          # SQLAlchemy models
│   │   ├── database.py      # Database configuration
│   │   └── main.py          # FastAPI application entry point
│   ├── data/                # SQLite database storage
│   ├── Dockerfile           # Backend Docker configuration
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Backend documentation
│
└── docker-compose.yml       # Docker Compose configuration

```

## Features

### Current Implementation (MVP)

- User authentication (mock implementation)
- Project listing
- Project creation
- SQLite database integration
- RESTful API endpoints
- Responsive UI with React Router

### API Endpoints

- `POST /api/auth/login` - User login (returns dummy token)
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create a new project

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Getting Started

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/nicestudio911/enterpreneurship-platform-nbu.git
cd enterpreneurship-platform-nbu
```

2. Start all services using Docker Compose:
```bash
docker compose up --build
```

This command will:
- Build the frontend and backend Docker images
- Start the FastAPI backend
- Start the React frontend with Nginx
- Initialize SQLite database automatically

3. Access the application:
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

### Backend Development

To run the backend locally:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The SQLite database will be created automatically in the `data/` directory.

### Environment Variables

#### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

#### Backend
```bash
export DATABASE_URL=sqlite:///./data/app.db
```

Note: The `DATABASE_URL` defaults to `sqlite:///./data/app.db` if not set. The database file will be created automatically.

## Database

The application uses SQLite, which is a file-based database. The database file is automatically created when you run the application for the first time.

### Database Location
- **Local Development**: `backend/data/app.db`
- **Docker**: The database file is persisted in `backend/data/` directory (mounted as a volume)

The database schema is automatically created by SQLAlchemy based on the model definitions when the application starts.

## Technology Stack

### Frontend
- React 18.2
- TypeScript 5.3
- Vite 5.0
- React Router 6.20
- Axios 1.6
- Nginx (for production)

### Backend
- Python 3.11
- FastAPI 0.104
- SQLAlchemy 2.0
- Uvicorn (ASGI server)
- Pydantic (data validation)

### Infrastructure
- Docker
- Docker Compose
- SQLite (file-based database)

## Project Status

This is an MVP (Minimum Viable Product) skeleton with basic functionality. The authentication is currently mocked and returns dummy tokens. Future enhancements will include:

- Real authentication with JWT tokens
- User registration
- Project management features
- Role-based access control
- Advanced project filtering and search

## License

This project is part of the NBU Entrepreneurship Platform initiative.
