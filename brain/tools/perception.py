from typing import Dict, Any
from langchain.tools import BaseTool
from brain.agents.memory import MemorySystem

class ExtractContextTool(BaseTool):
    name = "extract_context"
    description = "Extracts relevant contextual information from input data"

    def __init__(self):
        super().__init__()
        self.memory = MemorySystem()

    def _run(self, data: Any) -> Dict[str, Any]:
        """
        Extract context from input data
        Args:
            data: Input data to extract context from
        Returns:
            Dictionary containing extracted contextual information
        """
        # Extract basic metadata
        context = {
            'type': str(type(data).__name__),
            'length': len(str(data)) if hasattr(data, '__str__') else None,
        }

        # If input is a dictionary, extract keys as context
        if isinstance(data, dict):
            context['keys'] = list(data.keys())
            context['value_types'] = {k: str(type(v).__name__) for k, v in data.items()}

        # If input is a list, extract basic list properties
        elif isinstance(data, (list, tuple)):
            context['count'] = len(data)
            if data:
                context['element_type'] = str(type(data[0]).__name__)

        # If input is a string, extract basic text properties
        elif isinstance(data, str):
            context['word_count'] = len(data.split())
            context['has_numbers'] = any(c.isdigit() for c in data)

        return context

    def _arun(self, data: Any) -> Dict[str, Any]:
        """Async version of run"""
        raise NotImplementedError("ExtractContextTool does not support async")
