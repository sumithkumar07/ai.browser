from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minimal Test API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Minimal API is running"}

@app.get("/")
async def root():
    return {"message": "Minimal API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_minimal:app", host="0.0.0.0", port=8002, reload=True)