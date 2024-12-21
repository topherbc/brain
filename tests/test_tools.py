import pytest
from src.tools.text_analysis import TextAnalysisTool
from src.tools.analysis import AnalysisTool
from crewai import Tool

def test_text_analysis_tools_creation():
    """Test text analysis tools creation"""
    keyword_tool = TextAnalysisTool.create_keyword_extraction_tool()
    intent_tool = TextAnalysisTool.create_intent_recognition_tool()
    
    assert isinstance(keyword_tool, Tool)
    assert isinstance(intent_tool, Tool)
    assert keyword_tool.name == "keyword_extraction"
    assert intent_tool.name == "intent_recognition"

def test_analysis_tools_creation():
    """Test analysis tools creation"""
    pattern_tool = AnalysisTool.create_pattern_analysis_tool()
    risk_tool = AnalysisTool.create_risk_assessment_tool()
    
    assert isinstance(pattern_tool, Tool)
    assert isinstance(risk_tool, Tool)
    assert pattern_tool.name == "pattern_analysis"
    assert risk_tool.name == "risk_assessment"