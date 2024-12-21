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
        
        # Initialize crews for different processing stages
        self.initial_crew = self._create_initial_crew()
        self.parallel_crew = self._create_parallel_crew()
        self.final_crew = self._create_final_crew()

    # Agent creation methods remain the same...
    def _create_sensory_agent(self) -> Agent:
        return Agent(
            role="Sensory Perception Specialist",
            goal="Extract key elements and semantic signals from input",
            backstory=(
                "Break down input into fundamental components. Extract keywords, "
                "identify intent, and capture semantic signals. Mark important "
                "elements with [FOCUS]. Just extract - don't interpret."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_pattern_recognition_agent(self) -> Agent:
        return Agent(
            role="Pattern Analyst",
            goal="Identify patterns and relationships in sensory data",
            backstory=(
                "Map connections between extracted elements. Create structured "
                "understanding of relationships. Focus on [FOCUS] elements."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    # Other agent creation methods stay the same...

    def _create_initial_crew(self) -> Crew:
        """Create crew for initial sequential processing"""
        agents = [
            self._create_sensory_agent(),
            self._create_pattern_recognition_agent()
        ]

        tasks = [
            Task(
                description="Process input: '{input}' - Extract key elements and mark with [FOCUS]",
                agent=agents[0],
                expected_output="Extracted features with attention markers"
            ),
            Task(
                description="Map patterns in: {previous_output}",
                agent=agents[1],
                expected_output="Pattern structure and relationships"
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def _create_parallel_crew(self) -> Crew:
        """Create crew for parallel analysis tasks"""
        agents = [
            self._create_memory_agent(),
            self._create_risk_assessment_agent(),
            self._create_specialist_agent()
        ]

        tasks = [
            Task(
                description="Integrate context for: {input} using {patterns}",
                agent=agents[0],
                expected_output="Contextual framework"
            ),
            Task(
                description="Assess risks in: {input} based on {patterns}",
                agent=agents[1],
                expected_output="Risk analysis"
            ),
            Task(
                description="Provide domain expertise on: {input} considering {patterns}",
                agent=agents[2],
                expected_output="Domain-specific insights"
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.parallel,
            verbose=self.verbose
        )

    def _create_final_crew(self) -> Crew:
        """Create crew for final synthesis"""
        agents = [self._create_executive_agent()]

        tasks = [
            Task(
                description="Synthesize final response from: {context}, {risks}, and {expertise}",
                agent=agents[0],
                expected_output="Final synthesized response"
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """Process input through parallel cognitive pipeline"""
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            if self.verbose:
                print(f"\n🧠 Processing Input: '{input_data}'")
            
            # Update specialist for domain if provided
            if domain:
                self.parallel_crew.agents[2].backstory = (
                    f"Expert in {domain}. Provide specific insights "
                    "and recommendations for this domain."
                )
            
            # Stage 1: Initial Processing
            initial_result = self.initial_crew.kickoff(
                inputs={'input': input_data}
            )
            
            if self.verbose:
                print("\n1️⃣ Initial Processing Complete")
            
            # Stage 2: Parallel Analysis
            parallel_results = self.parallel_crew.kickoff(
                inputs={
                    'input': input_data,
                    'patterns': initial_result
                }
            )
            
            if self.verbose:
                print("\n2️⃣ Parallel Analysis Complete")
            
            # Stage 3: Final Synthesis
            final_result = self.final_crew.kickoff(
                inputs={
                    'context': parallel_results[0],
                    'risks': parallel_results[1],
                    'expertise': parallel_results[2]
                }
            )
            
            if self.verbose:
                print("\n3️⃣ Final Synthesis Complete")
                print("\n🔬 Output:")
                print(final_result)
            
            return str(final_result)
        
        except Exception as e:
            error_msg = f"Processing error: {e}"
            logger.error(error_msg)
            return error_msg

def main():
    # Test problems
    test_problems = [
        ("When were open stem coupe glasses made?", "glassware_history"),
        ("What materials were traditionally used in open stem coupe glass production?", "glassware_materials"),
        ("How can you identify authentic open stem coupe glasses from reproductions?", "glassware_authentication")
    ]

    crew = CognitiveCrew(verbose=True)
    for problem, domain in test_problems:
        print("\n" + "="*50)
        print(f"Processing: {problem}")
        print("="*50)
        result = crew.process_input(problem, domain)

if __name__ == "__main__":
    main()