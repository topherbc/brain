from typing import Dict, Any
import json

class DataFormatter:
    def format_data(self, data: Any) -> Dict[str, Any]:
        """Format data into a standardized structure.
        
        Args:
            data: Input data to format (can be string, dict, or other types)
            
        Returns:
            dict: Formatted data in standardized structure
        """
        formatted = {
            'type': self._get_data_type(data),
            'content': None,
            'metadata': {
                'timestamp': None,
                'format_version': '1.0'
            }
        }
        
        # Handle different input types
        if isinstance(data, str):
            # Try to parse as JSON first
            try:
                formatted['content'] = json.loads(data)
            except json.JSONDecodeError:
                # If not JSON, treat as plain text
                formatted['content'] = {'text': data}
                
        elif isinstance(data, dict):
            formatted['content'] = data
            
        elif isinstance(data, (list, tuple)):
            formatted['content'] = {'items': list(data)}
            
        else:
            # For other types, convert to string
            formatted['content'] = {'value': str(data)}
            
        return formatted
    
    def _get_data_type(self, data: Any) -> str:
        """Determine the type of input data."""
        if isinstance(data, str):
            try:
                json.loads(data)
                return 'json'
            except json.JSONDecodeError:
                return 'text'
        elif isinstance(data, dict):
            return 'dict'
        elif isinstance(data, (list, tuple)):
            return 'array'
        else:
            return type(data).__name__