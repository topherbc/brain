import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import the ThinkingProcess from brain2
from src.brain2 import ThinkingProcess

# Initialize FastAPI app
app = FastAPI(title="Brain Project API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ThinkingProcess
try:
    brain = ThinkingProcess(verbose=True)
except Exception as e:
    print(f"Error initializing ThinkingProcess: {e}")
    brain = None

class ProcessRequest(BaseModel):
    text: str  # Changed from 'input' to match frontend
    domain: Optional[str] = None

class ProcessResponse(BaseModel):
    response: str  # Changed to match what frontend expects

@app.post("/process")
async def process_input(request: ProcessRequest):
    if brain is None:
        raise HTTPException(
            status_code=500,
            detail="ThinkingProcess not properly initialized"
        )

    try:
        # Process the input using ThinkingProcess
        result = brain.process(
            request.text,
            domain=request.domain
        )
        
        # Return in format expected by frontend
        return ProcessResponse(response=str(result))
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "brain_initialized": brain is not None}

if __name__ == "__main__":
    # Default to port 8001
    port = int(os.getenv("PORT", 8001))
    
    # Run the FastAPI application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload during development
    )