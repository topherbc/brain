from typing import List, Optional, Any
from crewai import Agent, Task, Crew, Process
from .domain_synthesis import DomainSynthesizer

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.domain = 'science'  # Default domain

    def _create_executive_agent(self) -> Agent:
        """Create an executive agent sensitive to domain-specific synthesis"""
        return Agent(
            role="Cognitive Executive Synthesizer",
            goal="Synthesize final output with domain-specific reasoning",
            backstory="You integrate diverse cognitive inputs into a coherent, domain-specific conclusion.",
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """Process input with domain-specific executive synthesis"""
        try:
            # Set domain, defaulting to 'science' if not specified
            self.domain = domain.lower() if domain else 'science'
            
            # Create executive agent
            executive_agent = self._create_executive_agent()
            
            # Collect intermediate results (simulated for this example)
            intermediate_results = [
                "Initial perception",
                "Pattern analysis",
                "Contextual interpretation"
            ]
            
            # Select domain-specific synthesis strategy
            synthesis_strategy = DomainSynthesizer.DOMAIN_SYNTHESIS_STRATEGIES.get(
                self.domain, 
                DomainSynthesizer.DOMAIN_SYNTHESIS_STRATEGIES['science']
            )
            
            # Synthesize final output using domain-specific strategy
            final_output = synthesis_strategy(str(input_data), intermediate_results)
            
            return final_output
        
        except Exception as e:
            return f"Processing error: {e}"