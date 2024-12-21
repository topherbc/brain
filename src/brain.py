import os
import logging
from typing import List, Optional, Any
from crewai import Agent, Task, Crew, Process
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .domain_contexts import get_domain_context

# Rest of the previous code remains the same...

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.domain_context = None
        self.crew_instance = self._create_crew()

    def _create_specialist_agent(self) -> Agent:
        """
        Domain-Specific Specialist Agent with enhanced contextual awareness
        """
        backstory_template = (
            "You are a specialized expert in the {domain} domain. {perspective} "
            "Approach this query with a {tone} perspective. {approach} Transcend "
            "mere factual reporting and seek deeper, more nuanced understanding."
        )

        return Agent(
            role="Holistic Domain Expert",
            goal="Provide profound, context-rich insights that reveal deeper layers of understanding",
            backstory=backstory_template.format(**self.domain_context) if self.domain_context else "",
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Enhanced input processing with domain-specific context
        """
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            # Retrieve domain-specific context
            self.domain_context = get_domain_context(domain) if domain else None
            
            # Dynamically recreate specialist agent with domain context
            self.crew_instance.agents[-2] = self._create_specialist_agent()
            
            result = self.crew_instance.kickoff(inputs={'input': input_data})
            
            return str(result)
        
        except Exception as e:
            error_msg = f"Processing error: {e}"
            print(error_msg)
            logger.error(error_msg)
            return error_msg

# Rest of the code remains the same
