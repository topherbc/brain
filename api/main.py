from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from pathlib import Path

# Import the CognitiveCrew from your existing project
from src.brain import CognitiveCrew

# Initialize FastAPI app
app = FastAPI(title="Brain Project API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web interface
static_path = Path(__file__).parent.parent / "web"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")

# Initialize CognitiveCrew
crew = CognitiveCrew(verbose=True)

class ProcessRequest(BaseModel):
    input: str
    domain: Optional[str] = None

class ProcessResponse(BaseModel):
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None

@app.post("/api/process", response_model=ProcessResponse)
async def process_input(request: ProcessRequest):
    try:
        # Process the input using CognitiveCrew
        result = crew.process_input(
            request.input,
            domain=request.domain
        )
        
        # Check the result status
        if result.get('status') == 'success':
            return {
                "status": "success",
                "result": result.get('result')
            }
        else:
            return {
                "status": "error",
                "error": result.get('error', 'Unknown error occurred')
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the FastAPI application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload during development
    )