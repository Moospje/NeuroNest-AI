import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import api_router
from config.settings import settings
from database.session import SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup: Initialize database connection
    logger.info("Starting up NeuroNest-AI API")
    
    # Create database tables if they don't exist
    from database.base import Base
    from database.session import engine
    
    Base.metadata.create_all(bind=engine)
    
    # Initialize agents in database
    initialize_agents()
    
    yield
    
    # Shutdown: Close database connection
    logger.info("Shutting down NeuroNest-AI API")


def initialize_agents():
    """
    Initialize agents in the database.
    """
    from database.models import Agent
    
    db = SessionLocal()
    try:
        # Check if agents already exist
        if db.query(Agent).count() == 0:
            # Create default agents
            agents = [
                Agent(
                    name="Thinker",
                    description="I analyze problems and think through solutions step by step.",
                    agent_type="ThinkerAgent",
                ),
                Agent(
                    name="Developer",
                    description="I write code, review code, and provide technical guidance.",
                    agent_type="DeveloperAgent",
                ),
                Agent(
                    name="AutoGen",
                    description="I coordinate multiple AI agents to solve complex problems.",
                    agent_type="AutoGenAgent",
                ),
                Agent(
                    name="CrewAI",
                    description="I coordinate a crew of specialized AI agents to solve complex problems.",
                    agent_type="CrewAIAgent",
                ),
            ]
            db.add_all(agents)
            db.commit()
            logger.info("Default agents initialized")
    finally:
        db.close()


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return JSONResponse(
        content={
            "message": "Welcome to NeuroNest-AI API",
            "version": settings.PROJECT_VERSION,
            "docs_url": "/docs",
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )