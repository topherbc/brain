from typing import Any, Dict, List, Optional
from pydantic import Field
from .base import BrainAgent
from ..tools.analysis import TextAnalysisTool, DataAnalysisTool

class SensoryProcessor(BrainAgent):
    """Agent responsible for initial sensory processing and feature extraction."""
    name: str = Field(default="sensory_processor", description="Sensory processing agent")
    role: str = Field(default="sensory_processing", description="Initial input processing and feature extraction")
    goal: str = Field(
        default="Process and extract meaningful features from input data",
        description="Extract and organize sensory information"
    )
    
    tools: List[Any] = Field(default_factory=lambda: [
        TextAnalysisTool(),
        DataAnalysisTool()
    ])
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        features = {}
        
        if isinstance(input_data, str):
            tool = next(t for t in self.tools if isinstance(t, TextAnalysisTool))
            features = await tool.analyze(input_data)
        elif isinstance(input_data, (dict, list)):
            tool = next(t for t in self.tools if isinstance(t, DataAnalysisTool))
            features = await tool.analyze(input_data)
            
        return {
            "agent": self.name,
            "features": features,
            "metadata": {
                "input_type": type(input_data).__name__,
                "processing_status": "complete"
            }
        }