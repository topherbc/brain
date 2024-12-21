import pytest
from src.brain import CognitiveCrew
from src.utils.validation import InputValidator, OutputValidator
from src.memory.memory_store import MemoryStore

def test_cognitive_crew_initialization():
    """Test CognitiveCrew initialization"""
    crew = CognitiveCrew(verbose=True)
    assert crew is not None
    assert crew.memory is not None
    assert crew.crew is not None

def test_input_validation():
    """Test input validation"""
    with pytest.raises(ValueError):
        InputValidator(input_data=None)
    
    with pytest.raises(ValueError):
        InputValidator(input_data="", domain="test")
    
    validator = InputValidator(input_data="test input", domain="test domain")
    assert validator.input_data == "test input"
    assert validator.domain == "test domain"

def test_output_validation():
    """Test output validation"""
    with pytest.raises(ValueError):
        OutputValidator(status="invalid")
    
    with pytest.raises(ValueError):
        OutputValidator(status="success", result=None)
    
    validator = OutputValidator(
        status="success",
        result="test result",
        context={"test": "context"}
    )
    assert validator.status == "success"
    assert validator.result == "test result"

def test_memory_store():
    """Test MemoryStore operations"""
    memory = MemoryStore()
    
    # Test short-term memory
    memory.store_short_term("test_key", "test_value")
    assert memory.get_short_term("test_key") == "test_value"
    
    # Test long-term memory
    memory.store_long_term("test_key", "test_value")
    assert memory.get_long_term("test_key") == "test_value"
    
    # Test working memory
    memory.update_working_memory("test_key", "test_value")
    assert memory.get_working_memory("test_key") == "test_value"

def test_cognitive_processing():
    """Test cognitive processing pipeline"""
    crew = CognitiveCrew(verbose=False)
    
    # Test basic processing
    result = crew.process_input(
        "Test input for cognitive processing",
        domain="testing"
    )
    assert result['status'] == 'success'
    assert 'result' in result
    assert 'context' in result
    
    # Test error handling
    result = crew.process_input(None)
    assert result['status'] == 'error'
    assert 'error' in result