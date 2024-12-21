from typing import Any, Dict, List, Optional
from pydantic import Field
from .base import BaseAgent
from ..tools.text_analysis import TextAnalysisTool
from ..tools.analysis import AnalysisTool

class SensoryProcessor(BaseAgent):
    """Agent responsible for initial sensory processing and feature extraction."""
    name: str = Field(default="sensory_processor", description="Sensory processing agent")
    role: str = Field(default="sensory_processing", description="Initial input processing")
    goal: str = Field(
        default="Process and extract meaningful features from input data",
        description="Extract and organize sensory information"
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        self.text_tool = TextAnalysisTool()
        self.analysis_tool = AnalysisTool()
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process incoming sensory data and extract features."""
        if isinstance(input_data, str):
            text_tool = self.text_tool.create_keyword_extraction_tool()
            features = await text_tool.func(input_data)
        else:
            pattern_tool = self.analysis_tool.create_pattern_analysis_tool()
            features = await pattern_tool.func(input_data)
            
        return {
            "agent": self.name,
            "features": features,
            "metadata": {
                "input_type": type(input_data).__name__,
                "processing_status": "complete"
            }
        }