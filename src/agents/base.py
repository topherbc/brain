from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field
from crewai import Agent, Task, Process

class BrainAgent(Agent):
    """Base class for all cognitive agents in the brain architecture."""
    name: str = Field(description="Name of the agent")
    role: str = Field(description="Role of the agent in the cognitive architecture")
    goal: str = Field(description="Primary goal/objective of the agent")
    backstory: Optional[str] = Field(default=None, description="Agent's context and background")
    memory_span: Optional[int] = Field(default=5, description="Number of previous states to remember")
    allow_delegation: bool = Field(default=True, description="Whether agent can delegate tasks")
    
    class Config:
        arbitrary_types_allowed = True
        
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data according to agent's role."""
        raise NotImplementedError
        
    async def delegate(self, task: Task) -> Any:
        """Delegate a task to another agent if allowed."""
        if not self.allow_delegation:
            raise ValueError(f"Agent {self.name} does not allow delegation")
        # Implementation for delegation
        pass