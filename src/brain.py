from typing import Any, Optional
from .domain_reasoning import DomainReasoning

class CognitiveCrew:
    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Process input with domain-specific reasoning strategy
        """
        try:
            # Normalize domain, default to scientific reasoning
            domain_key = domain.lower() if domain else 'science'
            
            # Select reasoning strategy based on domain
            reasoning_strategy = DomainReasoning.DOMAIN_STRATEGIES.get(
                domain_key, 
                DomainReasoning.DOMAIN_STRATEGIES['science']
            )
            
            # Apply domain-specific reasoning
            result = reasoning_strategy(str(input_data))
            
            return result
        
        except Exception as e:
            return f"Processing error: {e}"