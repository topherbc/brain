import re
from typing import List

class TextCleaner:
    def __init__(self):
        self.special_chars_regex = re.compile(r'[^a-zA-Z0-9\s]')
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize input text.
        
        Args:
            text: Input text to clean
            
        Returns:
            str: Cleaned and normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = self.special_chars_regex.sub(' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text
        
    def tokenize(self, text: str) -> List[str]:
        """Split text into tokens.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        # Clean text first
        cleaned_text = self.clean_text(text)
        
        # Split into tokens
        tokens = cleaned_text.split()
        
        return tokens