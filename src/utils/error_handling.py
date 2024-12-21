from typing import Dict, Any, Optional
from functools import wraps
import traceback

class CognitiveError(Exception):
    """Base exception class for cognitive system errors"""
    pass

class InputError(CognitiveError):
    """Exception for input validation errors"""
    pass

class ProcessingError(CognitiveError):
    """Exception for processing errors"""
    pass

class MemoryError(CognitiveError):
    """Exception for memory operation errors"""
    pass

def handle_cognitive_errors(func):
    """Decorator for handling cognitive system errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except InputError as e:
            return {
                'status': 'error',
                'error': f"Input validation error: {str(e)}",
                'context': None
            }
        except ProcessingError as e:
            return {
                'status': 'error',
                'error': f"Processing error: {str(e)}",
                'context': None
            }
        except MemoryError as e:
            return {
                'status': 'error',
                'error': f"Memory operation error: {str(e)}",
                'context': None
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Unexpected error: {str(e)}\n{traceback.format_exc()}",
                'context': None
            }
    return wrapper