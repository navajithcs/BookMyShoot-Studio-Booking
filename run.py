#!/usr/bin/env python3
"""
BookMyShoot - Master Startup Script
Starts both backend (Flask) and frontend (HTTP server) simultaneously
"""

import subprocess
import sys
import time
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

def run_backend():
    """Start Flask backend server"""
    print("🚀 Starting Backend (Flask)...")
    backend_cmd = [str(VENV_PYTHON), "app.py"]
    subprocess.Popen(backend_cmd, cwd=str(BACKEND_DIR))
    print("✅ Backend started on http://localhost:5000")

def run_frontend():
    """Start Python HTTP frontend server"""
    print("🚀 Starting Frontend (HTTP Server)...")
    frontend_cmd = [str(VENV_PYTHON), "serve_frontend.py"]
    subprocess.Popen(frontend_cmd, cwd=str(PROJECT_ROOT))
    print("✅ Frontend started on http://localhost:5173")

def main():
    print("\n" + "="*60)
    print("🎯 BookMyShoot - Full Stack Application")
    print("="*60 + "\n")
    
    try:
        # Start backend
        run_backend()
        time.sleep(2)
        
        # Start frontend
        run_frontend()
        
        print("\n" + "="*60)
        print("✨ Both servers are running!")
        print("="*60)
        print("\n📍 Access the application:")
        print("   🌐 Frontend: http://localhost:5173")
        print("   🔌 Backend API: http://localhost:5000")
        print("\n💡 Press Ctrl+C to stop all servers")
        print("="*60 + "\n")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n✅ Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
