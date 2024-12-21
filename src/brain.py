from typing import List, Optional, Any
from crewai import Agent, Task, Crew, Process
from .domain_contexts import DomainContext

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.domain = 'science'  # Default domain

    def _apply_domain_lens(self, output: str, input_query: str) -> str:
        """
        Apply domain-specific lens to agent output
        """
        lens_function = DomainContext.DOMAIN_LENSES.get(
            self.domain, 
            DomainContext.DOMAIN_LENSES['science']
        )
        return lens_function(output, input_query)

    def _create_sensory_agent(self) -> Agent:
        return Agent(
            role="Sensory Perception Specialist",
            goal="Extract precise keywords and semantic signals",
            backstory="You are the initial point of cognitive processing, breaking down input into fundamental components.",
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_pattern_recognition_agent(self) -> Agent:
        return Agent(
            role="Cognitive Pattern Analyst",
            goal="Identify underlying cognitive patterns and structural relationships",
            backstory="You specialize in uncovering hidden connections and structural patterns.",
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Process input with domain-specific cognitive pipeline
        """
        try:
            # Set domain, defaulting to 'science' if not specified
            self.domain = domain.lower() if domain else 'science'
            
            # Create agents
            sensory_agent = self._create_sensory_agent()
            pattern_agent = self._create_pattern_recognition_agent()
            
            # Extract sensory information
            sensory_output = sensory_agent.execute_task(
                Task(description=f"Analyze: {input_data}", agent=sensory_agent)
            )
            
            # Apply domain lens to sensory output
            sensory_output_with_lens = self._apply_domain_lens(sensory_output, input_data)
            
            # Perform pattern recognition
            pattern_output = pattern_agent.execute_task(
                Task(description=f"Analyze pattern in: {sensory_output_with_lens}", agent=pattern_agent)
            )
            
            # Apply domain lens to pattern output
            pattern_output_with_lens = self._apply_domain_lens(pattern_output, input_data)
            
            return pattern_output_with_lens
        
        except Exception as e:
            return f"Processing error: {e}"