import os
import logging
from typing import List, Optional
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

class ThinkingProcess:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Create individual crews
        self.thinking_crew = self._create_thinking_crew()
        self.expert_crew = self._create_expert_crew()
        self.collaboration_crew = self._create_collaboration_crew()

    def _create_thinking_agents(self) -> List[Agent]:
        perception_agent = Agent(
            role="Core Pattern Analyzer",
            goal="Extract and analyze fundamental patterns from input",
            backstory="""You are specialized in identifying core patterns and 
            relationships in complex information. Your focus is on finding the 
            essential elements that will matter to expert analysis.""",
            verbose=self.verbose
        )

        context_agent = Agent(
            role="Context Integration Specialist",
            goal="Build comprehensive context around identified patterns",
            backstory="""You excel at building rich context around identified 
            patterns, ensuring all relevant factors are considered and properly 
            framed for expert analysis.""",
            verbose=self.verbose
        )

        return [perception_agent, context_agent]

    def _create_expert_agents(self) -> List[Agent]:
        expert1 = Agent(
            role="Primary Domain Expert",
            goal="Provide deep domain-specific analysis and solutions",
            backstory="""You are a leading expert in your field with decades of 
            experience. You approach problems with both theoretical depth and 
            practical wisdom.""",
            verbose=self.verbose
        )

        expert2 = Agent(
            role="Secondary Domain Expert",
            goal="Provide complementary expertise and alternative perspectives",
            backstory="""You bring extensive expertise from a related but distinct 
            domain, offering crucial alternative perspectives and cross-domain 
            insights.""",
            verbose=self.verbose
        )

        return [expert1, expert2]

    def _create_director_agent(self) -> Agent:
        return Agent(
            role="Strategic Director",
            goal="Synthesize expert insights and guide final decisions",
            backstory="""You are an experienced director with a track record of 
            synthesizing complex expert opinions into actionable strategies. 
            You excel at seeing the big picture while appreciating technical details.""",
            verbose=self.verbose
        )

    def _create_thinking_crew(self) -> Crew:
        agents = self._create_thinking_agents()
        tasks = [
            Task(
                description="""Analyze the input for fundamental patterns, 
                relationships, and key elements requiring expert attention.""",
                agent=agents[0]
            ),
            Task(
                description="""Build comprehensive context around identified patterns,
                preparing them for expert analysis.""",
                agent=agents[1]
            )
        ]
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def _create_expert_crew(self) -> Crew:
        agents = self._create_expert_agents()
        tasks = [
            Task(
                description="""Analyze the prepared context from primary domain 
                perspective, identifying key insights and potential solutions.""",
                agent=agents[0]
            ),
            Task(
                description="""Provide analysis from secondary domain perspective,
                highlighting additional insights and considerations.""",
                agent=agents[1]
            )
        ]
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def _create_collaboration_crew(self) -> Crew:
        director = self._create_director_agent()
        experts = self._create_expert_agents()
        
        tasks = [
            Task(
                description="""Review expert analyses and synthesize into coherent
                strategy and recommendations.""",
                agent=director
            )
        ]
        
        return Crew(
            agents=[director, *experts],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def process(self, input_data: str) -> str:
        """
        Process input through the complete thinking and expert analysis pipeline.
        """
        # Initial thinking process
        thinking_result = self.thinking_crew.kickoff(
            inputs={'input': input_data}
        )
        
        # Expert analysis
        expert_result = self.expert_crew.kickoff(
            inputs={
                'input': input_data,
                'thinking_context': thinking_result
            }
        )
        
        # Final synthesis
        final_result = self.collaboration_crew.kickoff(
            inputs={
                'input': input_data,
                'expert_analysis': expert_result
            }
        )
        
        return final_result

def main():
    # Test the thinking process
    test_inputs = [
        "What are the implications of quantum computing on current cryptography systems?",
        "How can we optimize supply chain resilience while maintaining cost efficiency?",
        "What are the ethical considerations in developing autonomous AI systems?"
    ]

    process = ThinkingProcess(verbose=True)
    
    for input_text in test_inputs:
        print("\n" + "="*50)
        print(f"Processing Question:\n{input_text}")
        print("="*50)
        
        result = process.process(input_text)
        print(f"\nResult:\n{result}")

if __name__ == "__main__":
    main()