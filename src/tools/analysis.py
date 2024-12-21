"""Analysis tools for cognitive processing."""

from typing import Dict, Any, List, Union
from langchain.tools import BaseTool
import numpy as np
from collections import defaultdict

class TextAnalysisTool(BaseTool):
    """Tool for analyzing text data."""
    
    name = "text_analysis"
    description = """
    Analyze text data to extract features and patterns.
    Input should be a string of text to analyze.
    Returns statistical analysis of the text.
    """
    
    def _run(self, text: str) -> Dict[str, Any]:
        """Run text analysis.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        words = text.split()
        sentences = text.split('.')
        
        return {
            'basic_stats': {
                'char_count': len(text),
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
            },
            'readability': {
                'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
                'unique_words': len(set(words))
            }
        }

class DataAnalysisTool(BaseTool):
    """Tool for analyzing numerical and categorical data."""
    
    name = "data_analysis"
    description = """
    Analyze numerical or categorical data.
    Input should be a list of values to analyze.
    Returns statistical analysis based on data type.
    """
    
    def _run(self, data: List[Any]) -> Dict[str, Any]:
        """Run data analysis.
        
        Args:
            data: List of values to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        if not data:
            return {'error': 'Empty dataset'}
            
        # Detect data type
        if all(isinstance(x, (int, float)) for x in data):
            return self._analyze_numeric(data)
        else:
            return self._analyze_categorical(data)
    
    def _analyze_numeric(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Analyze numeric data."""
        np_data = np.array(data)
        return {
            'statistics': {
                'mean': float(np.mean(np_data)),
                'median': float(np.median(np_data)),
                'std': float(np.std(np_data)),
                'min': float(np.min(np_data)),
                'max': float(np.max(np_data))
            }
        }
    
    def _analyze_categorical(self, data: List[Any]) -> Dict[str, Any]:
        """Analyze categorical data."""
        freq_dict = defaultdict(int)
        for item in data:
            freq_dict[str(item)] += 1
            
        return {
            'frequencies': dict(freq_dict),
            'unique_values': len(freq_dict),
            'most_common': max(freq_dict.items(), key=lambda x: x[1])[0]
        }