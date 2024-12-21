import os
import logging
from typing import List, Optional, Any, Dict
from crewai import Agent, Task, Crew, Process
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class BrainState(BaseModel):
    """Shared state for cognitive processing"""
    attention_focus: Dict[str, float] = Field(default_factory=dict)
    working_memory: Dict[str, Any] = Field(default_factory=dict)
    processing_depth: int = Field(default=1)
    confidence_threshold: float = Field(default=0.7)

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        """
        Initialize the Cognitive Crew with configurable verbosity and shared state
        
        Args:
            verbose: Enables detailed logging and output
        """
        self.verbose = verbose
        self.state = BrainState()
        self.crew_instance = self._create_crew()

    def _create_sensory_agent(self) -> Agent:
        """
        Enhanced Sensory Processing Agent with attention mechanism
        """
        return Agent(
            role="Sensory Perception Specialist",
            goal="Extract and filter key elements based on attention focus",
            backstory=(
                "You are the initial cognitive filter. Extract features with emphasis on "
                "areas highlighted by attention focus. Consider feedback from higher "
                "levels to modulate processing depth and feature selection."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_pattern_recognition_agent(self) -> Agent:
        """
        Enhanced Pattern Recognition Agent with hierarchical processing
        """
        return Agent(
            role="Cognitive Pattern Analyst",
            goal="Identify patterns with attention to highlighted features",
            backstory=(
                "You analyze patterns with special focus on attended features. "
                "Build hierarchical representations and maintain awareness of "
                "both local and global patterns. Consider feedback from memory "
                "and analytical processes."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_memory_agent(self) -> Agent:
        """
        Enhanced Memory Agent with working memory constraints
        """
        return Agent(
            role="Memory Integration Specialist",
            goal="Maintain and update working memory while considering capacity limits",
            backstory=(
                "You manage working memory with awareness of capacity limits. "
                "Prioritize information based on attention focus and relevance. "
                "Integrate new information with existing context within capacity "
                "constraints."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_executive_agent(self) -> Agent:
        """
        Enhanced Executive Agent with feedback control
        """
        return Agent(
            role="Executive Controller",
            goal="Coordinate processing and provide top-down feedback",
            backstory=(
                "You coordinate cognitive processes and provide feedback to earlier "
                "stages. Adjust attention focus, processing depth, and cognitive "
                "resources based on task demands and intermediate results."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_crew(self) -> Crew:
        """
        Create cognitive crew with enhanced interaction and feedback loops
        """
        # Create agents with shared state access
        agents = [
            self._create_sensory_agent(),
            self._create_pattern_recognition_agent(),
            self._create_memory_agent(),
            self._create_executive_agent()
        ]

        # Define tasks with feedback loops
        tasks = [
            Task(
                description=(
                    "Process input '{input}' with current attention focus: "
                    "{attention_focus}. Extract relevant features."
                ),
                agent=agents[0]
            ),
            Task(
                description=(
                    "Identify patterns in extracted features considering working "
                    "memory state: {working_memory}."
                ),
                agent=agents[1]
            ),
            Task(
                description=(
                    "Update working memory with new patterns while maintaining "
                    "capacity limits. Current state: {working_memory}."
                ),
                agent=agents[2]
            ),
            Task(
                description=(
                    "Review processing results and adjust cognitive parameters. "
                    "Provide feedback for next iteration if needed."
                ),
                agent=agents[3]
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
            model_kwargs={
                "temperature": 0.4,
                "max_tokens": 2000,
                "top_p": 0.8
            }
        )

    def _update_state(self, agent_outputs: Dict[str, str]):
        """
        Update shared brain state based on agent outputs
        
        Args:
            agent_outputs: Dictionary of agent outputs
        """
        # Update attention focus based on executive feedback
        if "executive" in agent_outputs:
            exec_output = agent_outputs["executive"]
            # Parse executive output for attention directives
            # (Implementation would depend on output format)
            pass

        # Update working memory with new information
        if "memory" in agent_outputs:
            mem_output = agent_outputs["memory"]
            # Update working memory while respecting capacity
            # (Implementation would depend on memory format)
            pass

    def process_input(self, input_data: Any) -> str:
        """
        Process input through cognitive pipeline with feedback loops
        
        Args:
            input_data: Input to be processed
        """
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")

            if self.verbose:
                print(f"\n🧠 Processing Input: '{input_data}'")

            # Initialize processing variables
            iteration = 0
            max_iterations = 3  # Prevent infinite loops
            processing_complete = False
            final_result = None

            # Processing loop with feedback
            while not processing_complete and iteration < max_iterations:
                # Update task inputs with current state
                task_inputs = {
                    'input': input_data,
                    'attention_focus': self.state.attention_focus,
                    'working_memory': self.state.working_memory
                }

                # Process through crew
                result = self.crew_instance.kickoff(inputs=task_inputs)

                # Update shared state based on results
                self._update_state({'executive': str(result)})

                # Check if processing is complete (could be based on confidence or other metrics)
                processing_complete = self.state.confidence_threshold >= 0.9
                final_result = result
                iteration += 1

            if self.verbose:
                print(f"\n🔄 Required {iteration} iterations")
                print("\n🔬 Final Output:")
                print(final_result)

            return str(final_result)

        except Exception as e:
            error_msg = f"Processing error: {e}"
            logger.error(error_msg)
            return error_msg

def main():
    # Test cases
    test_inputs = [
        "Analyze the environmental impact of electric vehicles",
        "Explain how neural networks learn from data",
        "Describe the process of photosynthesis"
    ]

    # Process with feedback loops
    crew = CognitiveCrew(verbose=True)
    for input_data in test_inputs:
        print("\n" + "="*50)
        print(f"Processing: {input_data}")
        print("="*50)
        result = crew.process_input(input_data)

if __name__ == "__main__":
    main()