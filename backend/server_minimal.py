from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import only core routers that are likely to work
from api.user_management.router import router as user_router

# Database
from database.connection import get_database, connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 AI Agentic Browser - Minimal Test Starting...")
    
    # Initialize database connection
    try:
        await connect_to_mongo()
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    yield
    # Shutdown
    print("👋 AI Browser shutting down...")
    await close_mongo_connection()

# Create FastAPI app
app = FastAPI(
    title="AI Agentic Browser - Minimal Test",
    description="Minimal version for debugging",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"Internal server error: {str(exc)}",
            "message": "The AI browser encountered an unexpected error."
        }
    )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "🚀 AI Agentic Browser - Minimal Test",
        "status": "running",
        "version": "0.1.0"
    }

# API Health check endpoint
@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    try:
        # Test database connection
        db = await get_database()
        db_status = "connected" if db is not None else "disconnected"
        
        return {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": "2025-01-XX",
            "services": {
                "database": db_status,
                "api": "operational"
            },
            "message": "AI Agentic Browser API is operational"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "message": "API health check failed"
            }
        )

# Include minimal routers
try:
    app.include_router(user_router, prefix="/api/users", tags=["User Management"])
    print("✅ User management router included")
except Exception as e:
    print(f"❌ User management router failed: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(
        "server_minimal:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False,
        log_level="info"
    )