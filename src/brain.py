import os
import logging
from typing import List, Optional, Any
from crewai import Agent, Task, Crew, Process
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Reduce logging noise
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        """
        Initialize the Cognitive Crew with configurable verbosity
        
        :param verbose: Enables detailed logging and output
        """
        self.verbose = verbose
        self.current_input = None
        
        # Initialize crew
        self.crew_instance = self._create_crew()

    def _create_sensory_agent(self) -> Agent:
        """
        Sensory Processing Agent
        Raw input perception and initial feature extraction
        """
        return Agent(
            role="Sensory Perception Specialist",
            goal="Precisely extract key elements, keywords, and semantic signals from the input",
            backstory=(
                "You are the initial point of cognitive processing. Your job is to break down "
                "the input into its most fundamental components. Extract exact keywords, "
                "identify the primary intent, and capture the core semantic signals with "
                "laser-sharp precision. Do not summarize or interpret - just extract."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_crew(self) -> Crew:
        """
        Create the cognitive processing crew with neural-like sequential processing
        """
        # Create agents
        agents = [
            self._create_sensory_agent(),
            self._create_pattern_recognition_agent(),
            self._create_memory_agent(),
            self._create_risk_assessment_agent(),
            self._create_analytical_agent(),
            self._create_specialist_agent(),
            self._create_executive_agent()
        ]

        # Define tasks with proper input handling
        def create_task(agent: Agent, description: str, expected_output: str) -> Task:
            return Task(
                description=description,
                agent=agent,
                expected_output=expected_output,
                context=lambda: f"Processing input: {self.current_input}"
            )

        # Define tasks with proper input context
        tasks = [
            create_task(
                agents[0],
                "Extract precise keywords, identify primary intent, and capture core semantic signals from the input.",
                "A list of exact keywords, core intent, and primary semantic signals, with no interpretation or summary"
            ),
            create_task(
                agents[1],
                "Analyze extracted features to reveal underlying cognitive patterns. Create a structured mapping of conceptual connections.",
                "A clear, logical mapping of conceptual relationships and patterns"
            ),
            create_task(
                agents[2],
                "Synthesize the pattern-identified features into a comprehensive context. Explain how different elements interact and contribute to understanding.",
                "A holistic contextual framework explaining interconnections"
            ),
            create_task(
                agents[3],
                "Critically evaluate potential implications, limitations, and areas of uncertainty in the current understanding.",
                "A detailed analysis of potential risks and limitations"
            ),
            create_task(
                agents[4],
                "Transform integrated and risk-assessed information into sophisticated, nuanced insights. Develop clear, actionable recommendations.",
                "Sophisticated insights with precise, actionable recommendations"
            ),
            create_task(
                agents[5],
                "Apply deep, domain-specific knowledge to provide nuanced, expert-level insights that add depth to the analysis.",
                "Expert-level insights specific to the input's domain"
            ),
            create_task(
                agents[6],
                "Synthesize all previous insights into a single, coherent, and directly actionable response.",
                "A crisp, clear, and immediately actionable final response"
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
            model_kwargs={
                "temperature": 0.4,  # Balanced between creativity and precision
                "max_tokens": 2000,  # Increased to allow more comprehensive processing
                "top_p": 0.8  # Allows for more diverse but still focused responses
            }
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """
        Process input through the advanced cognitive pipeline
        
        :param input_data: Input to be processed
        :param domain: Optional domain-specific context
        """
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            # Store current input for task context
            self.current_input = input_data
            
            if self.verbose:
                print(f"\n🧠 Advanced Cognitive Processing Input: '{input_data}'")
            
            # Customize specialist agent if domain is provided
            if domain:
                self.crew_instance.agents[-2].backstory = (
                    f"You are a specialized expert in the {domain} domain. "
                    "Provide nuanced, expert-level insights specific to this field, "
                    "drawing on deep domain knowledge to offer precise and relevant interpretations."
                )
            
            # Process input through the crew
            result = self.crew_instance.kickoff()
            
            if self.verbose:
                print("\n🔬 Final Cognitive Output:")
                print(result)
            
            return str(result)
        
        except Exception as e:
            error_msg = f"Advanced cognitive processing error: {e}"
            print(error_msg)
            logger.error(error_msg)
            return error_msg

def main():
    # Initialize Cognitive Crew with verbose output
    cognitive_crew = CognitiveCrew(verbose=True)
    
    # Test with sample inputs
    test_inputs = [
        ("What color is the sky?", "physics"),
        ("What are all the evenly divisible numbers from 1 to 100?", "math")
    ]
    
    # Process each input
    for input_text, domain in test_inputs:
        print("\n" + "="*50)
        print(f"Processing: {input_text}")
        print("="*50)
        
        result = cognitive_crew.process_input(input_text, domain)

if __name__ == "__main__":
    main()