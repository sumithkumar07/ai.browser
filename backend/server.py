from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api.browser.router import router as browser_router
from api.ai_agents.router import router as ai_router
from api.ai_agents.enhanced_router import router as enhanced_ai_router
from api.ai_agents.hybrid_router import router as hybrid_ai_router
from api.automation.router import router as automation_router
from api.automation.enhanced_router import router as enhanced_automation_router
from api.content.router import router as content_router
from api.user_management.router import router as user_router

# Import Phase 2-4 advanced routers
from api.ecosystem.router import router as ecosystem_router
from api.edge_computing.router import router as edge_computing_router
from api.emerging_tech.router import router as emerging_tech_router
from api.modular_ai.router import router as modular_ai_router
from api.global_intelligence.router import router as global_intelligence_router
from api.phase_capabilities.router import router as phase_capabilities_router

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

# CORS middleware - do not hardcode URLs
frontend_origin = os.environ.get("FRONTEND_ORIGIN")
allow_origins = [frontend_origin] if frontend_origin else ["*"]
allow_credentials = bool(frontend_origin)  # Only allow credentials when a specific origin is set

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers with API prefix
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(browser_router, prefix="/api/browser", tags=["browser"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai_agents"])
app.include_router(enhanced_ai_router, prefix="/api/ai/enhanced", tags=["enhanced_ai"])
app.include_router(automation_router, prefix="/api/automation", tags=["automation"])
app.include_router(enhanced_automation_router, prefix="/api/automation/enhanced", tags=["enhanced_automation"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

# Include Phase 2-4 advanced routers
app.include_router(ecosystem_router, tags=["ecosystem_integration"])
app.include_router(edge_computing_router, tags=["edge_computing"])
app.include_router(emerging_tech_router, tags=["emerging_technology"])
app.include_router(modular_ai_router, tags=["modular_ai"])
app.include_router(global_intelligence_router, tags=["global_intelligence"])
app.include_router(phase_capabilities_router, tags=["phase_capabilities"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agentic Browser API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agentic Browser API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)