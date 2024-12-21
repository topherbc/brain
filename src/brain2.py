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
                description="For the question: '{input}', identify and analyze fundamental patterns, key relationships, and essential elements that require expert attention.",
                agent=agents[0],
                expected_output="A structured analysis of core patterns and relationships relevant to the input question"
            ),
            Task(
                description="Given the patterns identified from '{input}', build comprehensive context considering all relevant factors and prepare for expert analysis.",
                agent=agents[1],
                expected_output="Contextual framework that integrates identified patterns with relevant background and implications"
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
                description="Review '{input}' and the provided context. Analyze from your primary domain expertise, providing key insights and potential solutions.",
                agent=agents[0],
                expected_output="Primary domain analysis with specific insights and recommendations based on expertise"
            ),
            Task(
                description="Examine '{input}' from your complementary domain perspective, considering the primary analysis and adding crucial alternative viewpoints.",
                agent=agents[1],
                expected_output="Secondary domain analysis with alternative perspectives and additional considerations"
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
                description="For the question '{input}', review all expert analyses and synthesize into a coherent strategy with clear recommendations.",
                agent=director,
                expected_output="Final synthesized strategy incorporating expert insights with clear, actionable recommendations"
            )
        ]
        
        return Crew(
            agents=[director, *experts],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def process(self, input_data: str, domain: Optional[str] = None) -> str:
        """
        Process input through the complete thinking and expert analysis pipeline.
        
        Args:
            input_data: The question or problem to analyze
            domain: Optional domain context to specialize the analysis
        """
        try:
            if self.verbose:
                print(f"\n🧠 Starting analysis of: {input_data}")
                if domain:
                    print(f"Domain context: {domain}")
            
            # Initial thinking process
            thinking_result = self.thinking_crew.kickoff(
                inputs={'input': input_data}
            )
            
            if self.verbose:
                print("\n📋 Thinking analysis complete, starting expert review")
            
            # Expert analysis
            expert_result = self.expert_crew.kickoff(
                inputs={
                    'input': input_data,
                    'thinking_context': thinking_result
                }
            )
            
            if self.verbose:
                print("\n🔍 Expert analysis complete, synthesizing final results")
            
            # Final synthesis
            final_result = self.collaboration_crew.kickoff(
                inputs={
                    'input': input_data,
                    'expert_analysis': expert_result
                }
            )
            
            if self.verbose:
                print("\n✅ Analysis complete")
            
            return str(final_result)
        
        except Exception as e:
            error_msg = f"Processing error: {str(e)}"
            logger.error(error_msg)
            return error_msg

def main():
    # Test cases with domain contexts
    test_cases = [
        ("What are the implications of quantum computing on current cryptography systems?", "cryptography"),
        ("How can we optimize supply chain resilience while maintaining cost efficiency?", "supply_chain"),
        ("What are the ethical considerations in developing autonomous AI systems?", "ai_ethics")
    ]

    process = ThinkingProcess(verbose=True)
    
    for question, domain in test_cases:
        print("\n" + "="*50)
        print(f"Processing Question:\n{question}")
        print(f"Domain: {domain}")
        print("="*50)
        
        result = process.process(question, domain)
        print(f"\nFinal Result:\n{result}")

if __name__ == "__main__":
    main()