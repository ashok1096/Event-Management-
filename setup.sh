#!/bin/bash
set -e

echo "Setting up EventPulse project..."

# 1. Install backend dependencies
echo "Installing backend dependencies..."
cd backend
python -m venv venv
source venv/Scripts/activate || source venv/bin/activate
pip install -r requirements.txt
pip install pytest flake8

# 2. Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

# 3. Run the seeder
echo "Seeding database..."
cd ../backend
python seed.py

echo "Setup complete! You can now run the backend (uvicorn app.main:app) and frontend (npm run dev)."
