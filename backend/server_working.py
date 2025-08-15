from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import core routers only
from api.user_management.router import router as user_router
from api.ai_agents.enhanced_router import router as enhanced_ai_router

# Import database connection
from database.connection import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="AI Agentic Browser API",
    description="Next-generation AI-powered browser with autonomous capabilities",
    version="1.0.0"
)

# Manual startup and shutdown handlers instead of lifespan for worker compatibility
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown") 
async def shutdown_event():
    await close_mongo_connection()

# CORS middleware - simplified configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include core routers with API prefix
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(enhanced_ai_router, prefix="/api/ai/enhanced", tags=["enhanced_ai"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agentic Browser API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agentic Browser API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_working:app", host="0.0.0.0", port=8001, reload=True)