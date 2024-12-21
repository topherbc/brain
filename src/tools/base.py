from typing import Optional
from pydantic import BaseModel, Field

class BaseTool(BaseModel):
    """Base class for all analysis tools in the brain project."""
    name: str = Field(description="Name of the tool")
    description: Optional[str] = Field(default=None, description="Description of the tool's functionality")
    
    class Config:
        arbitrary_types_allowed = True