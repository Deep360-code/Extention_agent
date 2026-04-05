from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.prisma_client import connect_db, disconnect_db

# Routers
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.llm_routes import router as llm_router
from app.routes.usage_routes import router as usage_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Connecting to Prisma Database...")
    await connect_db()
    yield
    # Shutdown actions
    logger.info("Disconnecting from Prisma Database...")
    await disconnect_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Configuration for Chrome Extensions and local dev
origins = [
    "chrome-extension://*",  # For Chrome Extensions
    "http://localhost:3000", # Local Web UI
    "*"                      # Can restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(llm_router)
app.include_router(usage_router)

@app.get("/health")
async def health_check():
    """Health check endpoint to ensure API and DB are running."""
    from app.database.prisma_client import db
    db_status = "connected" if db.is_connected() else "disconnected"
    return {
        "status": "ok",
        "message": f"{settings.PROJECT_NAME} is running",
        "database": db_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
