from typing import Any, Dict
from pydantic import Field
from crewai import Tool
from .base import BaseTool

class TextAnalysisTool(BaseTool):
    """Tool for text analysis operations."""
    name: str = Field(default="text_analysis", description="Text analysis tool name")
    
    @classmethod
    def create_keyword_extraction_tool(cls) -> Tool:
        """Create a keyword extraction tool."""
        return Tool(
            name="keyword_extraction",
            description="Extracts keywords from text",
            func=cls._extract_keywords
        )
    
    @classmethod
    def create_intent_recognition_tool(cls) -> Tool:
        """Create an intent recognition tool."""
        return Tool(
            name="intent_recognition",
            description="Recognizes intent in text",
            func=cls._recognize_intent
        )
    
    @staticmethod
    async def _extract_keywords(text: str) -> Dict[str, Any]:
        """Extract keywords from text."""
        return {
            "keywords": text.split(),
            "confidence": 0.8,
            "status": "success"
        }
    
    @staticmethod
    async def _recognize_intent(text: str) -> Dict[str, Any]:
        """Recognize intent in text."""
        return {
            "intent": "unknown",
            "confidence": 0.8,
            "status": "success"
        }