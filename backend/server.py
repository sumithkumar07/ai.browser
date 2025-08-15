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
from api.ai_agents.advanced_router import router as advanced_ai_router
from api.automation.router import router as automation_router
from api.automation.enhanced_router import router as enhanced_automation_router
from api.content.router import router as content_router
from api.user_management.router import router as user_router

# Import comprehensive features router
try:
    from api.comprehensive_features.router import router as comprehensive_features_router
    COMPREHENSIVE_FEATURES_AVAILABLE = True
    print("✅ Comprehensive features router loaded successfully")
except Exception as e:
    print(f"⚠️ Comprehensive features router not available: {e}")
    COMPREHENSIVE_FEATURES_AVAILABLE = False

# Import enhanced features router (fallback)
try:
    from api.enhanced_features.router import router as enhanced_features_router
    ENHANCED_FEATURES_AVAILABLE = True
except Exception as e:
    print(f"Warning: Enhanced features router not available: {e}")
    ENHANCED_FEATURES_AVAILABLE = False

# Import Phase 2-4 advanced routers
try:
    from api.ecosystem.router import router as ecosystem_router
    from api.edge_computing.router import router as edge_computing_router
    from api.emerging_tech.router import router as emerging_tech_router
    from api.modular_ai.router import router as modular_ai_router
    from api.global_intelligence.router import router as global_intelligence_router
    from api.phase_capabilities.router import router as phase_capabilities_router
    ADVANCED_ROUTERS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Advanced routers not available: {e}")
    ADVANCED_ROUTERS_AVAILABLE = False

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

# Include routers with API prefix
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(browser_router, prefix="/api/browser", tags=["browser"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai_agents"])
app.include_router(enhanced_ai_router, prefix="/api/ai/enhanced", tags=["enhanced_ai"])
app.include_router(hybrid_ai_router, prefix="/api/ai/hybrid", tags=["hybrid_ai"])
app.include_router(advanced_ai_router, prefix="/api/ai/advanced", tags=["advanced_ai"])
app.include_router(automation_router, prefix="/api/automation", tags=["automation"])
app.include_router(enhanced_automation_router, prefix="/api/automation/enhanced", tags=["enhanced_automation"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

# Include comprehensive features router (if available)
if COMPREHENSIVE_FEATURES_AVAILABLE:
    try:
        app.include_router(comprehensive_features_router, prefix="/api/comprehensive-features", tags=["comprehensive_features"])
        print("✅ Comprehensive features router included successfully")
    except Exception as e:
        print(f"⚠️ Error including comprehensive features router: {e}")

# Include enhanced features router (fallback)
if ENHANCED_FEATURES_AVAILABLE:
    try:
        app.include_router(enhanced_features_router, prefix="/api/enhanced-features", tags=["enhanced_features"])
        print("✅ Enhanced features router included successfully")
    except Exception as e:
        print(f"⚠️ Error including enhanced features router: {e}")
else:
    print("⚠️ Enhanced features router skipped due to import errors")

# Include Phase 2-4 advanced routers with proper prefixes
if ADVANCED_ROUTERS_AVAILABLE:
    try:
        app.include_router(ecosystem_router, prefix="/api/ecosystem", tags=["ecosystem_integration"])
        app.include_router(edge_computing_router, prefix="/api/edge-computing", tags=["edge_computing"])
        app.include_router(emerging_tech_router, prefix="/api/emerging-tech", tags=["emerging_technology"])
        app.include_router(modular_ai_router, prefix="/api/modular-ai", tags=["modular_ai"])
        app.include_router(global_intelligence_router, prefix="/api/global-intelligence", tags=["global_intelligence"])
        app.include_router(phase_capabilities_router, prefix="/api/phase-capabilities", tags=["phase_capabilities"])
        print("✅ Advanced routers loaded successfully")
    except Exception as e:
        print(f"⚠️ Error loading advanced routers: {e}")
else:
    print("⚠️ Advanced routers skipped due to import errors")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agentic Browser API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agentic Browser API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)