from typing import List, Optional, Any, Dict
from crewai import Agent, Task, Crew, Process
from .domain_synthesis import DomainSynthesizer

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.domain = 'science'  # Default domain
        self.specialization = None  # New attribute for domain specialization

    def _create_director_agent(self, domain: str, specialization: Optional[str] = None) -> Agent:
        """Create a director agent with domain and specialization awareness"""
        domain_contexts = {
            'science': {
                'physics': "Analytical approach focusing on fundamental principles and quantitative reasoning",
                'biology': "Holistic approach considering systems, interactions, and evolutionary context",
                'chemistry': "Focused on molecular interactions and compositional analysis"
            },
            'philosophy': {
                'ethics': "Examining moral principles and their practical implications",
                'epistemology': "Analyzing the nature of knowledge and understanding",
                'metaphysics': "Exploring fundamental nature of reality and existence"
            }
        }

        # Default to general context if specific domain or specialization not found
        backstory_context = domain_contexts.get(domain, {}).get(
            specialization, 
            f"Expert cognitive director for {domain} domain with interdisciplinary perspective"
        )

        return Agent(
            role=f"{domain.capitalize()} Cognitive Director",
            goal=f"Direct cognitive processing in {domain} domain, leveraging {specialization or 'interdisciplinary'} insights",
            backstory=backstory_context,
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None, specialization: Optional[str] = None) -> str:
        """Process input with domain and specialization-specific executive synthesis"""
        try:
            # Set domain and specialization, defaulting to 'science' if not specified
            self.domain = domain.lower() if domain else 'science'
            self.specialization = specialization.lower() if specialization else None
            
            # Create director agent with domain and specialization
            director_agent = self._create_director_agent(self.domain, self.specialization)
            
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