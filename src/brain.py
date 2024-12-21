import os
from typing import Optional, Any
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.crew = self._create_crew()

    def _create_input_processor(self) -> Agent:
        """Input processing and understanding"""
        return Agent(
            role="Input Processor",
            goal="Understand input and determine appropriate processing depth",
            backstory=(
                "You are the initial processor that determines how to handle input. "
                "For simple questions, provide direct answers. For complex queries, "
                "coordinate deeper analysis. Always maintain focus on the original question."
            ),
            verbose=self.verbose
        )

    def _create_knowledge_agent(self) -> Agent:
        """Knowledge retrieval and context integration"""
        return Agent(
            role="Knowledge Integrator",
            goal="Retrieve relevant information and integrate necessary context",
            backstory=(
                "You retrieve and integrate relevant knowledge based on query needs. "
                "For simple questions, provide straightforward facts. For complex ones, "
                "add necessary context and relationships. Avoid over-complication."
            ),
            verbose=self.verbose
        )

    def _create_response_agent(self) -> Agent:
        """Final response synthesis"""
        return Agent(
            role="Response Synthesizer",
            goal="Create clear, appropriate responses scaled to query complexity",
            backstory=(
                "You create final responses that match query complexity. "
                "Simple questions get direct answers. Complex queries get "
                "detailed analysis. Always maintain clarity and relevance."
            ),
            verbose=self.verbose
        )

    def _create_crew(self) -> Crew:
        """Create the cognitive processing crew"""
        agents = [
            self._create_input_processor(),
            self._create_knowledge_agent(),
            self._create_response_agent()
        ]

        tasks = [
            Task(
                description=(
                    "Analyze the input and determine appropriate processing level. "
                    "For simple queries like 'What color is the sky?', flag for basic processing. "
                    "For complex queries, identify aspects needing deeper analysis."
                ),
                agent=agents[0]
            ),
            Task(
                description=(
                    "Based on processing level, retrieve and integrate relevant information. "
                    "For basic queries, provide direct facts. For complex queries, "
                    "add necessary context and relationships."
                ),
                agent=agents[1]
            ),
            Task(
                description=(
                    "Create a clear, appropriate response matching query complexity. "
                    "Simple questions get straightforward answers. Complex queries "
                    "get appropriately detailed responses."
                ),
                agent=agents[2]
            )
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def process_input(self, input_data: Any) -> str:
        """Process input through the cognitive pipeline"""
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            if self.verbose:
                print(f"\n🧠 Processing Input: '{input_data}'")
            
            result = self.crew.kickoff(inputs={'input': input_data})
            
            if self.verbose:
                print("\n🔬 Output:")
                print(result)
            
            return str(result)
        
        except Exception as e:
            error_msg = f"Processing error: {e}"
            print(error_msg)
            return error_msg

def main():
    # Test the crew with different complexity queries
    crew = CognitiveCrew(verbose=True)
    
    # Test cases
    test_inputs = [
        "What color is the sky?",  # Simple query
        "How does quantum computing work?",  # Complex query
        "What's 2+2?",  # Simple math
        "What are the implications of AI on society?"  # Complex analysis
    ]
    
    for input_text in test_inputs:
        print("\n" + "="*50)
        print(f"Processing: {input_text}")
        print("="*50)
        
        result = crew.process_input(input_text)

if __name__ == "__main__":
    main()