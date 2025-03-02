from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app.api.api import api_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Meeting.AI API",
    description="API for transcribing and summarizing audio/video content",
    version="0.1.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Meeting.AI API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
