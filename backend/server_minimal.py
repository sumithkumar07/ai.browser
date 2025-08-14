from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connection
from database.connection import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="AI Agentic Browser API",
    description="Next-generation AI-powered browser with autonomous capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - simplified configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agentic Browser API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agentic Browser API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_minimal:app", host="0.0.0.0", port=8001, reload=True)