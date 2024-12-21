import pytest
from src.agents.sensory import SensoryAgent
from crewai import Agent

def test_sensory_agent_creation():
    """Test sensory agent creation and configuration"""
    agent = SensoryAgent(verbose=False)
    created_agent = agent.create()
    
    assert isinstance(created_agent, Agent)
    assert created_agent.role == "Sensory Perception Specialist"
    assert not created_agent.allow_delegation

def test_sensory_agent_processing():
    """Test sensory agent processing capabilities"""
    agent = SensoryAgent(verbose=False)
    
    # Test feature extraction
    features = agent.process_input("Test input for feature extraction")
    
    assert isinstance(features, dict)
    assert 'keywords' in features
    assert 'intent' in features
    assert 'sentiment' in features
    assert 'entities' in features
    
    # Test memory storage
    assert agent.recall_memory('last_processed_input') is not None
    assert agent.recall_memory('extracted_features') is not None