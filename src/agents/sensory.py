from typing import Dict, Any
from .base import BaseAgent

class SensoryAgent(BaseAgent):
    """Agent responsible for initial sensory processing of inputs."""
    
    def _get_agent_config(self) -> Dict[str, Any]:
        """Get sensory agent configuration.
        
        Returns:
            Dictionary containing agent configuration
        """
        return {
            'name': 'Sensory Processing',
            'goal': 'Process and extract features from input data',
            'backstory': 'Specialized in initial data processing and feature extraction',
            'allow_delegation': False,
            'tools': self.config.get('tools', []),
            'verbose': self.config.get('verbose', False)
        }
    
    def process_input(self, input_data: Any) -> Dict[str, Any]:
        """Process input data through sensory analysis.
        
        Args:
            input_data: Raw input data to process
            
        Returns:
            Dictionary containing processed features
        """
        # Initial processing logic
        features = {}
        
        # Extract basic features based on input type
        if isinstance(input_data, str):
            features['text_length'] = len(input_data)
            features['word_count'] = len(input_data.split())
        
        return features