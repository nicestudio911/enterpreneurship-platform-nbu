# Entrepreneurship Platform

A full-stack web application for managing entrepreneurship projects, built with React, Spring Boot, and PostgreSQL.

## Architecture

- **Frontend**: React 18 with TypeScript, Vite, and React Router
- **Backend**: Spring Boot 3.2 with Java 21
- **Database**: PostgreSQL 16
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
├── backend/                 # Spring Boot backend application
│   ├── src/main/java/com/entrepreneurship/platform/
│   │   ├── controller/      # REST API controllers
│   │   ├── service/         # Business logic layer
│   │   ├── repository/      # Data access layer
│   │   ├── model/entity/    # JPA entities
│   │   └── config/          # Application configuration
│   ├── Dockerfile           # Backend Docker configuration
│   └── pom.xml              # Maven dependencies
│
└── docker-compose.yml       # Docker Compose configuration

```

## Features

### Current Implementation (MVP)

- User authentication (mock implementation)
- Project listing
- Project creation
- PostgreSQL database integration
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
- Start the PostgreSQL database
- Start the Spring Boot backend
- Start the React frontend with Nginx

3. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080/api
- **Database**: localhost:5432

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
mvn spring-boot:run
```

Make sure PostgreSQL is running and accessible at localhost:5432.

### Environment Variables

#### Frontend (.env)
```
VITE_API_URL=http://localhost:8080/api
```

#### Backend (application.properties)
```
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/appdb
SPRING_DATASOURCE_USERNAME=app
SPRING_DATASOURCE_PASSWORD=app
```

## Database

The PostgreSQL database is automatically initialized when you run `docker compose up`. The schema is created automatically by Spring Boot JPA based on the entity definitions.

### Database Credentials (Development)
- **Host**: localhost
- **Port**: 5432
- **Database**: appdb
- **Username**: app
- **Password**: app

## Technology Stack

### Frontend
- React 18.2
- TypeScript 5.3
- Vite 5.0
- React Router 6.20
- Axios 1.6
- Nginx (for production)

### Backend
- Java 21
- Spring Boot 3.2
- Spring Data JPA
- PostgreSQL Driver
- Maven

### Infrastructure
- Docker
- Docker Compose
- PostgreSQL 16

## Project Status

This is an MVP (Minimum Viable Product) skeleton with basic functionality. The authentication is currently mocked and returns dummy tokens. Future enhancements will include:

- Real authentication with JWT tokens
- User registration
- Project management features
- Role-based access control
- Advanced project filtering and search

## License

This project is part of the NBU Entrepreneurship Platform initiative.
