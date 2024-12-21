from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

class BaseTool(BaseModel):
    """Base class for all analysis tools."""
    name: str = Field(default="base_tool", description="Name of the tool")
    description: Optional[str] = Field(default=None, description="Tool description")
    
    class Config:
        arbitrary_types_allowed = True
        
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze input data."""
        raise NotImplementedError