#!/usr/bin/env python3
"""
Mars AI Agents - FastAPI Backend Server
Handles processing requests from React frontend and integrates with Gmail API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import logging
import os
from pathlib import Path
from datetime import datetime

# Import our Gmail data retrieval module
from .get_data import process_gmail_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Mars AI Agents API",
    description="Backend API for Mars AI Agents processing system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for document serving
if os.path.exists("data"):
    app.mount("/documents", StaticFiles(directory="data"), name="documents")

# Pydantic models for request/response
class ProcessingRequest(BaseModel):
    """Request model for processing endpoint"""
    action: str = "start_processing"

class ProcessingResponse(BaseModel):
    """Response model for processing results"""
    success: bool
    message: str
    files_downloaded: List[str] = []
    emails_processed: int = 0
    error: Optional[str] = None
    timestamp: str

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    service: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API is running"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="Mars AI Agents API"
    )

# Main processing endpoint
@app.post("/api/process", response_model=ProcessingResponse)
async def start_processing(request: ProcessingRequest):
    """
    Main processing endpoint that triggers Gmail data retrieval
    
    Args:
        request: Processing request with action type
        
    Returns:
        ProcessingResponse with results
    """
    logger.info(f"Processing request received: {request.action}")
    
    try:
        # Call the Gmail data processing function
        result = await asyncio.get_event_loop().run_in_executor(
            None, process_gmail_data
        )
        
        # Prepare response
        response = ProcessingResponse(
            success=result.get('success', False),
            message=result.get('message', 'No new records to display'),
            files_downloaded=result.get('files_downloaded', []),
            emails_processed=result.get('emails_processed', 0),
            error=result.get('error'),
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Processing completed: {response.message}")
        return response
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        
        # Return error response
        return ProcessingResponse(
            success=False,
            message="Processing failed due to internal error",
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

# Get processing status endpoint
@app.get("/api/status")
async def get_processing_status():
    """
    Get current processing status and system information
    
    Returns:
        System status information
    """
    try:
        # Check if credentials exist
        import os
        credentials_exist = os.path.exists('credentials.json')
        token_exists = os.path.exists('token.json')
        data_folder_exists = os.path.exists('data')
        
        return {
            "status": "ready",
            "credentials_configured": credentials_exist,
            "token_exists": token_exists,
            "data_folder_exists": data_folder_exists,
            "target_email": "demotest.tcs@gmail.com",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get status: {str(e)}"}
        )

# Get downloaded files endpoint
@app.get("/api/files")
async def get_downloaded_files():
    """
    Get list of downloaded files in the data directory
    
    Returns:
        List of downloaded files with metadata
    """
    try:
        import os
        from pathlib import Path
        
        data_dir = Path("data")
        if not data_dir.exists():
            return {"files": [], "total_count": 0}
        
        files_info = []
        for file_path in data_dir.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files_info.append({
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "folder": str(file_path.parent)
                })
        
        # Sort by modification date (newest first)
        files_info.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "files": files_info,
            "total_count": len(files_info),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get files: {str(e)}"}
        )

# Configuration endpoint
@app.get("/api/config")
async def get_configuration():
    """
    Get current configuration settings
    
    Returns:
        Configuration information
    """
    return {
        "target_email": "demotest.tcs@gmail.com",
        "data_folder": "data",
        "gmail_api_scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
        "search_hours_back": 24,
        "max_results": 10,
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url.path)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Mars AI Agents API starting up...")
    logger.info("API Documentation available at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Mars AI Agents API shutting down...")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "service": "Mars AI Agents API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )