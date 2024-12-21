from typing import Any, Dict, List, Optional
from pydantic import Field
from .base import BrainAgent
from ..tools.analysis import TextAnalysisTool, DataAnalysisTool

class AnalyticalProcessor(BrainAgent):
    """Agent responsible for deep analysis and insight generation."""
    name: str = Field(default="analytical_processor", description="Analytical processing agent")
    role: str = Field(default="deep_analysis", description="Deep analysis and insight generation")
    goal: str = Field(
        default="Perform comprehensive analysis and generate insights",
        description="Generate deep analytical insights from processed data"
    )
    
    analysis_depth: int = Field(
        default=3,
        description="Depth level of analysis (1-5)"
    )
    
    analysis_modes: List[str] = Field(
        default=[
            "correlational",
            "causal",
            "predictive",
            "diagnostic"
        ],
        description="Types of analysis to perform"
    )
    
    tools: List[Any] = Field(default_factory=lambda: [
        TextAnalysisTool(name="deep_text_analysis"),
        DataAnalysisTool(name="deep_data_analysis")
    ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        insights = {}
        recommendations = []
        
        for mode in self.analysis_modes:
            mode_insights = await self._analyze_mode(input_data, mode)
            insights[mode] = mode_insights
            
            if mode_insights.get("significance", 0) > 0.7:
                recommendations.extend(
                    await self._generate_recommendations(mode_insights)
                )
        
        return {
            "agent": self.name,
            "insights": insights,
            "recommendations": recommendations,
            "metadata": {
                "analysis_depth": self.analysis_depth,
                "modes_analyzed": self.analysis_modes
            }
        }
    
    async def _analyze_mode(
        self,
        data: Dict[str, Any],
        mode: str
    ) -> Dict[str, Any]:
        return {
            "mode": mode,
            "findings": {},
            "significance": 0.8,
            "confidence": 0.8
        }
    
    async def _generate_recommendations(
        self,
        insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return [{
            "source": insights["mode"],
            "priority": "high",
            "recommendation": "Generic recommendation",
            "confidence": 0.8
        }]