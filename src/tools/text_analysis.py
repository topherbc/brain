from typing import Dict, Any, List
import re
from collections import Counter

class TextAnalysisTool:
    """Tool for analyzing text data."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the text analysis tool.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive text analysis.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        results = {
            'basic_stats': self._get_basic_stats(text),
            'word_stats': self._get_word_stats(text),
            'sentence_stats': self._get_sentence_stats(text)
        }
        return results
    
    def _get_basic_stats(self, text: str) -> Dict[str, int]:
        """Get basic text statistics.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of basic statistics
        """
        return {
            'char_count': len(text),
            'word_count': len(text.split()),
            'line_count': len(text.splitlines())
        }
    
    def _get_word_stats(self, text: str) -> Dict[str, Any]:
        """Analyze word usage patterns.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of word statistics
        """
        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(words)
        
        return {
            'unique_words': len(word_freq),
            'top_words': word_freq.most_common(10)
        }
    
    def _get_sentence_stats(self, text: str) -> Dict[str, Any]:
        """Analyze sentence patterns.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of sentence statistics
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        lengths = [len(s.split()) for s in sentences]
        return {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(lengths) / len(lengths) if lengths else 0,
            'max_sentence_length': max(lengths) if lengths else 0
        }