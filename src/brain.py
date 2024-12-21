from typing import Any, Optional
from .domain_knowledge import DomainKnowledgeBase

class CognitiveCrew:
    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Process input with domain-specific knowledge strategy
        """
        try:
            # Normalize domain to lowercase, default to 'default' if not specified
            domain_key = domain.lower() if domain else 'default'
            
            # Select processor based on domain
            processor = DomainKnowledgeBase.DOMAIN_PROCESSORS.get(
                domain_key, 
                DomainKnowledgeBase.DOMAIN_PROCESSORS['default']
            )
            
            # Process with domain-specific strategy
            result = processor(str(input_data))
            
            return result
        
        except Exception as e:
            return f"Processing error: {e}"