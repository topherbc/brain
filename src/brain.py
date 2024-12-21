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

    def _create_pattern_recognition_agent(self) -> Agent:
        """
        Pattern Recognition Agent
        Identifies underlying structures and connections
        """
        return Agent(
            role="Cognitive Pattern Analyst",
            goal="Identify and map underlying cognitive patterns and structural relationships",
            backstory=(
                "You specialize in uncovering hidden connections and structural patterns. "
                "Analyze the extracted features to reveal underlying cognitive frameworks. "
                "Create a clear, logical mapping of how different elements interrelate. "
                "Your output should be a structured breakdown of conceptual connections."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_memory_agent(self) -> Agent:
        """
        Working Memory Agent
        Contextualizes and integrates information
        """
        return Agent(
            role="Contextual Memory Integrator",
            goal="Synthesize and contextualize extracted information into a comprehensive framework",
            backstory=(
                "You are responsible for creating a holistic context for the information. "
                "Take the pattern-identified features and weave them into a coherent narrative. "
                "Provide a comprehensive context that explains how different elements interact "
                "and contribute to the overall understanding of the input."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_risk_assessment_agent(self) -> Agent:
        """
        Risk and Uncertainty Analysis Agent
        Evaluates potential implications and limitations
        """
        return Agent(
            role="Cognitive Risk Assessor",
            goal="Critically evaluate potential implications, limitations, and areas of uncertainty",
            backstory=(
                "Your role is to provide a critical, analytical perspective on the integrated "
                "information. Identify potential blind spots, assess risks, and highlight "
                "areas of uncertainty. Your analysis should reveal potential limitations "
                "or challenges in the current understanding."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_analytical_agent(self) -> Agent:
        """
        Analytical Reasoning Agent
        Generates deep insights and precise reasoning
        """
        return Agent(
            role="Advanced Analytical Reasoner",
            goal="Generate sophisticated insights and provide precise, actionable reasoning",
            backstory=(
                "You are the highest level of cognitive processing. Transform the integrated "
                "and risk-assessed information into sophisticated, nuanced insights. "
                "Develop clear, actionable recommendations that address the core intent "
                "of the original input with depth and precision."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_specialist_agent(self) -> Agent:
        """
        Domain-Specific Specialist Agent
        Provides expert-level insights based on input domain
        """
        return Agent(
            role="Domain-Specific Knowledge Expert",
            goal="Provide expert-level, domain-specific insights that add depth to the analysis",
            backstory=(
                "You are a specialized expert tailored to the specific domain of the input. "
                "Apply deep, domain-specific knowledge to provide nuanced insights that "
                "go beyond general reasoning. Offer practical, expert-level recommendations "
                "that leverage specialized understanding."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_executive_agent(self) -> Agent:
        """
        Executive Function Agent
        Synthesizes final output and ensures coherence
        """
        return Agent(
            role="Cognitive Executive Synthesizer",
            goal="Synthesize the final output into a clear, coherent, and actionable response",
            backstory=(
                "Your ultimate function is to take all previous insights and synthesize them "
                "into a single, coherent, and directly actionable response. Ensure the final "
                "output is crisp, clear, and provides immediate value to the user."
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

        # Define tasks with explicit instructions
        tasks = [
            Task(
                description="Analyze this input: '{input}' - Extract precise keywords, identify primary intent, and capture core semantic signals.",
                agent=agents[0],
                expected_output="A list of exact keywords, core intent, and primary semantic signals from the question"
            ),
            Task(
                description="Based on the analysis of '{input}', reveal underlying cognitive patterns and create a structured mapping of connections.",
                agent=agents[1],
                expected_output="A clear, logical mapping of conceptual relationships and patterns"
            ),
            Task(
                description="For '{input}', synthesize the pattern-identified features into a comprehensive context and explain their interactions.",
                agent=agents[2],
                expected_output="A holistic contextual framework explaining interconnections"
            ),
            Task(
                description="Evaluate implications and limitations in understanding '{input}'.",
                agent=agents[3],
                expected_output="A detailed analysis of potential risks and limitations"
            ),
            Task(
                description="Provide sophisticated insights and recommendations for '{input}'.",
                agent=agents[4],
                expected_output="Sophisticated insights with precise, actionable recommendations"
            ),
            Task(
                description="Apply domain expertise to analyze '{input}'.",
                agent=agents[5],
                expected_output="Expert-level insights specific to the input's domain"
            ),
            Task(
                description="Synthesize all insights about '{input}' into a final response.",
                agent=agents[6],
                expected_output="A crisp, clear, and immediately actionable final response"
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
            result = self.crew_instance.kickoff(inputs={'input': input_data})
            
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
    # Define test programming problems
    test_problems = [
        # 1. Simple arithmetic calculator
        ("""
        Write a function that takes two numbers and an operator (+, -, *, /) 
        and returns the result of the operation.

        Example:
        calculate(4, 2, '+') should return 6
        calculate(4, 2, '-') should return 2
        calculate(4, 2, '*') should return 8
        calculate(4, 2, '/') should return 2
        """, "programming"),

        # 2. FizzBuzz implementation
        ("""
        Write a function that takes a number n and prints:
        - 'Fizz' if the number is divisible by 3
        - 'Buzz' if the number is divisible by 5
        - 'FizzBuzz' if the number is divisible by both 3 and 5
        - The number itself if none of the above conditions are true

        Example:
        fizzbuzz(15) should print numbers from 1 to 15 with appropriate substitutions
        """, "programming"),

        # 3. Array manipulation
        ("""
        Write a function that finds the second largest number in an array.
        If there is no second largest number, return the largest number.

        Example:
        find_second_largest([1, 3, 4, 5, 0, 2]) should return 4
        find_second_largest([1, 1, 1]) should return 1
        """, "programming")
    ]

    # Initialize Cognitive Crew with verbose output
    cognitive_crew = CognitiveCrew(verbose=True)
    
    # Process each problem
    for problem, domain in test_problems:
        print("\n" + "="*50)
        print(f"Processing Problem:\n{problem}")
        print("="*50)
        
        result = cognitive_crew.process_input(problem, domain)

if __name__ == "__main__":
    main()