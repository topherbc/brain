import logging
from typing import Optional
from datetime import datetime

class CognitiveLogger:
    """Enhanced logging for the cognitive system"""
    
    def __init__(self, name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Create handlers if they don't exist
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(
            f'logs/cognitive_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)
    
    def _get_formatter(self) -> logging.Formatter:
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def log_processing_start(self, input_data: Any, domain: Optional[str] = None):
        """Log the start of cognitive processing"""
        self.logger.info(
            f"Starting cognitive processing | Input: {input_data} | Domain: {domain}"
        )
    
    def log_processing_end(self, status: str, result: Any = None, error: str = None):
        """Log the end of cognitive processing"""
        if status == 'success':
            self.logger.info(f"Processing completed successfully | Result: {result}")
        else:
            self.logger.error(f"Processing failed | Error: {error}")
    
    def log_memory_operation(self, operation: str, key: str, success: bool):
        """Log memory operations"""
        if success:
            self.logger.debug(f"Memory operation: {operation} | Key: {key} | Status: Success")
        else:
            self.logger.warning(f"Memory operation: {operation} | Key: {key} | Status: Failed")