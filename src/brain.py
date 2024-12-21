from typing import Any, Optional
from .domain_processors import DOMAIN_PROCESSORS

class CognitiveCrew:
    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Process input with domain-specific strategy
        """
        try:
            # Select processor based on domain
            processor = DOMAIN_PROCESSORS.get(domain, DOMAIN_PROCESSORS['science'])
            
            # Process with domain-specific strategy
            result = processor(str(input_data))
            
            return result
        
        except Exception as e:
            return f"Processing error: {e}"

    def verbose_process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Verbose processing with additional context
        """
        result = self.process_input(input_data, domain)
        print(f"Domain: {domain or 'default'}")
        print(f"Input: {input_data}")
        print(f"Result: {result}")
        return result