from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Basic Test Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Basic server working"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Basic health check"}

if __name__ == "__main__":
    uvicorn.run("test_basic_server:app", host="0.0.0.0", port=8001, reload=False)