#!/bin/bash
set -e

# 1) Install Python deps
cd backend
python -m pip install -r requirements.txt

# 2) Build frontend into backend/app/frontend
cd ../frontend
npm install
npm run build

# 3) Start FastAPI
cd ../backend
python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
