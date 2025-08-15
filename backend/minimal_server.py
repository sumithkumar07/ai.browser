from fastapi import FastAPI

app = FastAPI(
    title="Minimal Test API",
    description="Testing middleware issue",
    version="1.0.0"
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Minimal API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to Minimal API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("minimal_server:app", host="0.0.0.0", port=8002, reload=True)