from typing import Any, Dict, List, Optional
from pydantic import Field
from .base import BaseAgent

class SensoryAgent(BaseAgent):
    """Agent responsible for initial sensory processing and feature extraction."""
    name: str = Field(default="sensory_agent", description="Sensory processing agent")
    role: str = Field(default="sensory_processing", description="Initial input processing")
    goal: str = Field(
        default="Process and extract meaningful features from input data",
        description="Extract and organize sensory information"
    )
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process incoming sensory data and extract features."""
        # Basic feature extraction implementation
        features = {}
        
        if isinstance(input_data, str):
            features = await self._process_text(input_data)
        elif isinstance(input_data, (dict, list)):
            features = await self._process_structured(input_data)
            
        return {
            "agent": self.name,
            "features": features,
            "metadata": {
                "input_type": type(input_data).__name__,
                "processing_status": "complete"
            }
        }
        
    async def _process_text(self, text: str) -> Dict[str, Any]:
        """Process text input."""
        return {
            "type": "text",
            "length": len(text),
            "tokens": text.split()
        }
        
    async def _process_structured(self, data: Any) -> Dict[str, Any]:
        """Process structured data input."""
        return {
            "type": "structured",
            "size": len(data) if hasattr(data, "__len__") else 0
        }