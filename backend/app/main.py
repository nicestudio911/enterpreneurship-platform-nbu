from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import auth, projects, competitions, files

app = FastAPI(title="Entrepreneurship Platform API", version="1.0.0")

# CORS configuration
# Note: When allow_credentials=True, allow_origins cannot be ["*"]
# Since we're using nginx proxy, we don't need credentials for same-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(competitions.router)
app.include_router(files.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
def root():
    return {"message": "Entrepreneurship Platform API"}

