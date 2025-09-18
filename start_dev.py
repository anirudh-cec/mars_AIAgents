#!/usr/bin/env python3
"""
Development server launcher for Mars AI Agents
Starts both FastAPI backend and React frontend
"""

import subprocess
import sys
import time
import signal
import os
from threading import Thread

def run_fastapi():
    """Run FastAPI server"""
    print("🚀 Starting FastAPI server on http://localhost:8000")
    try:
        subprocess.run([
            sys.executable, "api_server.py"
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("FastAPI server stopped")

def run_react():
    """Run React development server"""
    print("⚛️  Starting React development server on http://localhost:3000")
    time.sleep(2)  # Give FastAPI a head start
    try:
        subprocess.run([
            "npm", "start"
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("React server stopped")

def main():
    """Main function to start both servers"""
    print("🌟 Mars AI Agents - Development Environment")
    print("=" * 50)
    
    # Check if credentials.json exists
    if not os.path.exists("credentials.json"):
        print("⚠️  WARNING: credentials.json not found!")
        print("📖 Please follow the setup instructions in GMAIL_SETUP.md")
        print("🔗 Gmail API setup required for email processing functionality")
        print()
    
    # Start FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    try:
        # Start React in main thread
        run_react()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down development servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()