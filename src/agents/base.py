from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

class BaseAgent(BaseModel):
    """Base class for all cognitive agents."""
    name: str = Field(description="Name of the agent")
    role: str = Field(description="Role of the agent")
    goal: str = Field(description="Primary goal/objective of the agent")
    memory_span: Optional[int] = Field(default=5, description="Number of previous states to remember")
    
    class Config:
        arbitrary_types_allowed = True
        
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data according to agent's role."""
        raise NotImplementedError