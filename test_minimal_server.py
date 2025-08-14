#!/usr/bin/env python3
"""
Minimal server test to isolate the middleware issue
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Test API")

# Test CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test():
    return {"message": "Test successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_minimal_server:app", host="0.0.0.0", port=8002, reload=False)