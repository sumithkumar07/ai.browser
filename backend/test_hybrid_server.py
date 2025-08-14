from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Hybrid AI Test Server",
    description="Test server for hybrid AI endpoints",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import only the hybrid router
try:
    from api.ai_agents.hybrid_router import router as hybrid_ai_router
    app.include_router(hybrid_ai_router, prefix="/api/ai/hybrid", tags=["hybrid_ai"])
    print("✅ Hybrid router imported successfully")
except Exception as e:
    print(f"❌ Error importing hybrid router: {e}")

# Import user router for authentication
try:
    from api.user_management.router import router as user_router
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    print("✅ User router imported successfully")
except Exception as e:
    print(f"❌ Error importing user router: {e}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Hybrid AI Test Server is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to Hybrid AI Test Server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_hybrid_server:app", host="0.0.0.0", port=8002, reload=True)