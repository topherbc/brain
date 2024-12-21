from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

# Import the CognitiveCrew from your existing project
from src.brain import CognitiveCrew

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
        "app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload during development
    )