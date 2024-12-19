import re
from typing import List
from .base import BaseTool

def clean_text(text: str) -> str:
    """Clean and normalize input text.
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    special_chars_regex = re.compile(r'[^a-zA-Z0-9\s]')
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters
    text = special_chars_regex.sub(' ', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text

def tokenize(text: str) -> List[str]:
    """Split text into tokens.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List[str]: List of tokens
    """
    # Clean text first
    cleaned_text = clean_text(text)
    
    # Split into tokens
    tokens = cleaned_text.split()
    
    return tokens

# Create tool instances
text_cleaner = BaseTool(
    name="text_cleaner",
    func=clean_text,
    description="Cleans and normalizes input text by removing special characters, converting to lowercase, and normalizing whitespace."
)

tokenizer = BaseTool(
    name="tokenizer",
    func=tokenize,
    description="Splits text into tokens after cleaning. Returns a list of cleaned tokens."
)