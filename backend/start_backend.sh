#!/bin/bash
cd /app/backend
/root/.venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001 --reload
