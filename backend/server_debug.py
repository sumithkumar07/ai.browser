from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Agentic Browser API - Debug",
    description="Debug version of the API",
    version="1.0.0"
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
    return {"message": "Welcome to AI Agentic Browser API - Debug"}

# Try importing routers one by one
try:
    from api.user_management.router import router as user_router
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    print("✅ User router included")
except Exception as e:
    print(f"❌ User router failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_debug:app", host="0.0.0.0", port=8003, reload=True)