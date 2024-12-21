from typing import Any, Dict, Optional
from pydantic import BaseModel, validator

class InputValidator(BaseModel):
    """Validate cognitive system inputs"""
    
    input_data: Any
    domain: Optional[str] = None
    
    @validator('input_data')
    def validate_input_data(cls, v):
        if v is None:
            raise ValueError("Input data cannot be None")
        if isinstance(v, str) and not v.strip():
            raise ValueError("Input string cannot be empty")
        return v
    
    @validator('domain')
    def validate_domain(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError("Domain must be a string if provided")
        if isinstance(v, str) and not v.strip():
            raise ValueError("Domain string cannot be empty if provided")
        return v

class OutputValidator(BaseModel):
    """Validate cognitive system outputs"""
    
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    context: Optional[Dict] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['success', 'error']:
            raise ValueError("Status must be either 'success' or 'error'")
        return v
    
    @validator('result')
    def validate_result(cls, v, values):
        if values.get('status') == 'success' and v is None:
            raise ValueError("Result cannot be None for successful status")
        return v
    
    @validator('error')
    def validate_error(cls, v, values):
        if values.get('status') == 'error' and not v:
            raise ValueError("Error message required for error status")
        return v