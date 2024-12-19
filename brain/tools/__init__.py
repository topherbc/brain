from .perception import ExtractContextTool
from .text import TokenizerTool

def extract_context():
    return ExtractContextTool()

def tokenizer():
    return TokenizerTool()
