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
            goal="Extract and organize fundamental patterns from input, preparing them for contextual integration",
            backstory="""You are specialized in identifying foundational patterns in information, 
            similar to how the brain's sensory regions detect key features. Your process mirrors 
            how the brain transforms raw input into meaningful patterns, enabling deeper analysis. 
            You break down complex inputs into essential components and relationships.""",
            verbose=self.verbose
        )

        context_agent = Agent(
            role="Context Integration Specialist",
            goal="Transform pattern analysis into contextually-rich frameworks",
            backstory="""You excel at weaving individual patterns into rich contextual frameworks, 
            similar to how the brain's associative regions create meaning from separate elements. 
            You build comprehensive understanding by connecting current patterns with relevant 
            background knowledge, creating complete contextual pictures for expert analysis.""",
            verbose=self.verbose
        )

        return [perception_agent, context_agent]

    def _create_expert_agents(self) -> List[Agent]:
        expert1 = Agent(
            role="Primary Domain Expert",
            goal="Provide focused, domain-specific insights based on contextual patterns",
            backstory="""You represent deep specialized processing capability, similar to how 
            dedicated brain regions develop expertise in specific types of information processing. 
            Your analysis draws from extensive domain knowledge to evaluate patterns within their 
            specific context, highlighting critical factors and potential implications.""",
            verbose=self.verbose
        )

        expert2 = Agent(
            role="Secondary Domain Expert",
            goal="Enrich primary analysis with complementary domain insights",
            backstory="""You provide essential alternative perspectives, similar to how the brain 
            processes information through complementary pathways. Your expertise offers different 
            but related viewpoints that enrich the primary analysis, identifying additional factors 
            and alternative interpretations.""",
            verbose=self.verbose
        )

        return [expert1, expert2]

    def _create_director_agent(self) -> Agent:
        return Agent(
            role="Strategic Director",
            goal="Synthesize analyses into coherent, actionable insights",
            backstory="""You function like the brain's executive regions, integrating diverse 
            analyses into coherent understanding. Your role is to synthesize expert insights 
            into clear, actionable conclusions while maintaining awareness of broader implications, 
            similar to how the prefrontal cortex coordinates and integrates information for 
            decision-making.""",
            verbose=self.verbose
        )

    def _create_thinking_crew(self) -> Crew:
        agents = self._create_thinking_agents()
        tasks = [
            Task(
                description="For the question: '{input}', identify and analyze fundamental patterns. 
                             Break down the input into essential components and relationships, 
                             extracting key elements that will form the basis for higher-level processing.",
                agent=agents[0],
                expected_output="A structured analysis of core patterns and their relationships, 
                               organized to facilitate contextual integration"
            ),
            Task(
                description="Using the identified patterns from '{input}', construct a comprehensive 
                             contextual framework. Integrate historical knowledge, current implications, 
                             and relevant background information to create a complete picture for expert analysis.",
                agent=agents[1],
                expected_output="Rich contextual framework that connects identified patterns with 
                               broader understanding and implications"
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
                description="Analyze '{input}' and the provided context through your primary domain 
                             expertise. Focus on critical factors, potential implications, and 
                             domain-specific insights based on the contextual patterns.",
                agent=agents[0],
                expected_output="Detailed primary domain analysis highlighting key insights, 
                               critical factors, and specific implications"
            ),
            Task(
                description="Examine '{input}' from your complementary domain perspective, 
                             considering the primary analysis. Identify additional factors, 
                             alternative interpretations, and enriching viewpoints.",
                agent=agents[1],
                expected_output="Complementary analysis providing alternative perspectives and 
                               additional considerations that enrich understanding"
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
                description="For the question '{input}', evaluate and integrate all expert analyses. 
                             Synthesize the insights into clear, actionable recommendations while 
                             maintaining awareness of broader implications.",
                agent=director,
                expected_output="Coherent synthesis of expert insights with clear, actionable 
                               recommendations and consideration of broader context"
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