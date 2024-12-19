from typing import List, Dict, Any
from langchain.tools import BaseTool
import re

class TokenizerTool(BaseTool):
    name: str = "tokenizer"
    description: str = "Tokenizes text into words, sentences, or custom patterns"
    return_direct: bool = False

    def _run(self, text: str, mode: str = 'word', pattern: str = None) -> Dict[str, Any]:
        """
        Tokenize text based on specified mode
        
        Args:
            text: Input text to tokenize
            mode: Tokenization mode ('word', 'sentence', or 'pattern')
            pattern: Custom regex pattern for tokenization (only used if mode='pattern')
            
        Returns:
            Dictionary containing tokenized results and statistics
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        result = {
            'original_length': len(text),
            'mode': mode
        }

        if mode == 'word':
            # Split on whitespace and punctuation
            tokens = re.findall(r'\w+', text)
            result['tokens'] = tokens
            result['token_count'] = len(tokens)
            
            # Additional word-level statistics
            result['avg_word_length'] = sum(len(word) for word in tokens) / len(tokens) if tokens else 0
            result['vocabulary_size'] = len(set(tokens))

        elif mode == 'sentence':
            # Split on sentence boundaries
            tokens = re.split(r'[.!?]+\s*', text)
            tokens = [t.strip() for t in tokens if t.strip()]
            result['tokens'] = tokens
            result['token_count'] = len(tokens)
            
            # Additional sentence-level statistics
            result['avg_sentence_length'] = sum(len(sent) for sent in tokens) / len(tokens) if tokens else 0
            result['words_per_sentence'] = [len(re.findall(r'\w+', sent)) for sent in tokens]

        elif mode == 'pattern' and pattern:
            # Use custom pattern for tokenization
            try:
                tokens = re.findall(pattern, text)
                result['tokens'] = tokens
                result['token_count'] = len(tokens)
                result['pattern_used'] = pattern
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {str(e)}")

        else:
            raise ValueError("Invalid mode or missing pattern for pattern mode")

        return result

    async def _arun(self, text: str, mode: str = 'word', pattern: str = None) -> Dict[str, Any]:
        """Async version of run"""
        raise NotImplementedError("TokenizerTool does not support async")
