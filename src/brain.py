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

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        """
        Initialize the Cognitive Crew with brain-inspired parallel processing
        
        :param verbose: Enables detailed logging and output
        """
        self.verbose = verbose
        self.crew_instance = self._create_crew()

    def _create_perception_agent(self) -> Agent:
        """
        Perception Agent - Inspired by Visual/Auditory Cortices
        Handles multi-modal sensory processing and feature detection
        """
        return Agent(
            role="Multi-Modal Perception Specialist",
            goal="Process and integrate multiple input modalities and extract key features",
            backstory=(
                "You are the primary sensory processing system, inspired by how the brain's "
                "sensory cortices work. You handle multiple input modalities simultaneously, "
                "detecting both low-level features (keywords, tone) and high-level features "
                "(semantic meaning, emotional content). Your processing occurs in parallel "
                "streams, similar to the brain's dorsal and ventral pathways."
            ),
            tools=[],
            allow_delegation=True,  # Enables parallel processing
            verbose=self.verbose
        )

    def _create_attention_agent(self) -> Agent:
        """
        Attention Network Agent - Inspired by Frontoparietal Network
        Manages focus and resource allocation
        """
        return Agent(
            role="Attention Network Controller",
            goal="Direct cognitive resources and maintain relevant information in focus",
            backstory=(
                "You represent the brain's attention networks, dynamically allocating "
                "cognitive resources based on salience and relevance. You maintain "
                "goal-relevant information in focus while filtering out distractions, "
                "similar to how the frontoparietal network operates."
            ),
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def _create_memory_integration_agent(self) -> Agent:
        """
        Memory Integration Agent - Inspired by Hippocampal-Cortical Systems
        Handles both working memory and episodic integration
        """
        return Agent(
            role="Memory Integration Specialist",
            goal="Integrate current input with existing knowledge and maintain working memory",
            backstory=(
                "You embody the brain's memory systems, particularly the hippocampal-cortical "
                "networks. You maintain and update working memory representations while also "
                "integrating new information with existing knowledge structures. This creates "
                "a dynamic, contextually-rich understanding of the input."
            ),
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def _create_emotional_agent(self) -> Agent:
        """
        Emotional Processing Agent - Inspired by Limbic System
        Processes emotional content and influences decision-making
        """
        return Agent(
            role="Emotional Intelligence Processor",
            goal="Analyze emotional content and its influence on cognitive processing",
            backstory=(
                "You represent the brain's emotional processing systems, similar to the "
                "limbic system. You evaluate the emotional significance of information, "
                "its potential impact on decision-making, and how it might influence "
                "the overall response generation."
            ),
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def _create_executive_control_agent(self) -> Agent:
        """
        Executive Control Agent - Inspired by Prefrontal Cortex
        Manages high-level control and decision-making
        """
        return Agent(
            role="Executive Control Manager",
            goal="Coordinate cognitive processes and generate adaptive responses",
            backstory=(
                "You embody the prefrontal cortex's executive functions, coordinating "
                "multiple cognitive processes and generating adaptive responses. You "
                "maintain goal-directed behavior, inhibit inappropriate responses, and "
                "ensure the final output aligns with current objectives."
            ),
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def _create_learning_agent(self) -> Agent:
        """
        Learning & Adaptation Agent - Inspired by Plasticity Mechanisms
        Handles learning and adaptation of responses
        """
        return Agent(
            role="Learning Systems Coordinator",
            goal="Facilitate learning and adaptation of cognitive responses",
            backstory=(
                "You represent the brain's learning and plasticity mechanisms. Your role "
                "is to identify patterns that could improve future processing, suggest "
                "adaptations to existing strategies, and maintain flexibility in "
                "cognitive responses based on feedback and context."
            ),
            tools=[],
            allow_delegation=True,
            verbose=self.verbose
        )

    def _create_crew(self) -> Crew:
        """
        Create the cognitive processing crew with parallel processing capabilities
        """
        # Create agents
        agents = [
            self._create_perception_agent(),
            self._create_attention_agent(),
            self._create_memory_integration_agent(),
            self._create_emotional_agent(),
            self._create_executive_control_agent(),
            self._create_learning_agent()
        ]

        # Define tasks with parallel processing capability
        tasks = [
            Task(
                description="Process input '{input}' across multiple modalities and extract features",
                agent=agents[0],
                expected_output="Multi-modal feature analysis including semantic and emotional content"
            ),
            Task(
                description="Allocate attention and identify key elements in '{input}'",
                agent=agents[1],
                expected_output="Prioritized information with attention allocation strategy"
            ),
            Task(
                description="Integrate '{input}' with existing knowledge and maintain working memory",
                agent=agents[2],
                expected_output="Integrated contextual understanding with memory components"
            ),
            Task(
                description="Analyze emotional aspects and implications of '{input}'",
                agent=agents[3],
                expected_output="Emotional analysis and its cognitive implications"
            ),
            Task(
                description="Coordinate processing and generate response for '{input}'",
                agent=agents[4],
                expected_output="Coordinated cognitive response with executive control"
            ),
            Task(
                description="Identify learning opportunities and adaptations from processing '{input}'",
                agent=agents[5],
                expected_output="Learning insights and adaptation recommendations"
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.hierarchical,  # Enables more flexible processing
            verbose=self.verbose,
            model_kwargs={
                "temperature": 0.4,  # Balance between creativity and precision
                "max_tokens": 2000,  # Allow comprehensive processing
                "top_p": 0.8  # Enable diverse but focused responses
            }
        )

    def process_input(self, input_data: Any, context: Optional[Dict] = None) -> str:
        """
        Process input through the cognitive pipeline
        
        :param input_data: Input to be processed
        :param context: Optional contextual information
        """
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            if self.verbose:
                print(f"\n🧠 Processing Input: '{input_data}'")
            
            # Update context if provided
            if context:
                # Customize relevant agents based on context
                for agent in self.crew_instance.agents:
                    if agent.role in context:
                        agent.backstory += f"\nContext Update: {context[agent.role]}"
            
            # Process input through the crew
            result = self.crew_instance.kickoff(inputs={'input': input_data})
            
            if self.verbose:
                print("\n🔬 Final Output:")
                print(result)
            
            return str(result)
        
        except Exception as e:
            error_msg = f"Processing error: {e}"
            print(error_msg)
            logger.error(error_msg)
            return error_msg

def main():
    # Define test scenarios with various cognitive demands
    test_scenarios = [
        (
            "How would you explain quantum entanglement to a high school student?",
            {"Learning Systems Coordinator": "Educational context requiring clear explanations"}
        ),
        (
            "What are the ethical implications of autonomous vehicles?",
            {"Emotional Intelligence Processor": "Complex moral reasoning scenario"}
        ),
        (
            "Can you help me optimize my daily routine for better productivity?",
            {"Executive Control Manager": "Personal optimization context"}
        )
    ]

    # Initialize Cognitive Crew with verbose output
    cognitive_crew = CognitiveCrew(verbose=True)
    
    # Process each scenario
    for input_text, context in test_scenarios:
        print("\n" + "="*50)
        print(f"Processing Scenario:\n{input_text}")
        print("="*50)
        
        result = cognitive_crew.process_input(input_text, context)

if __name__ == "__main__":
    main()