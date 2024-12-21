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
        self.thinking_crew = None
        self.expert_crew = None
        self.collaboration_crew = None

    def _get_complexity_instructions(self, complexity: int) -> str:
        """Get specific instructions based on complexity level."""
        if complexity <= 2:
            return (
                "Provide an extremely concise response focused only on the core point. "
                "Use no more than 2-3 short sentences. "
                "Skip all context and supporting details unless absolutely crucial."
            )
        elif complexity <= 4:
            return (
                "Give a brief, focused response with just the key points. "
                "Limit to 3-4 sentences. "
                "Include only the most essential supporting details."
            )
        elif complexity <= 6:
            return (
                "Provide a balanced analysis with main insights and key supporting details. "
                "Aim for moderate length with clear structure."
            )
        elif complexity <= 8:
            return (
                "Deliver a comprehensive analysis with detailed explanations. "
                "Include broader context and multiple perspectives."
            )
        else:
            return (
                "Present an in-depth, exhaustive analysis. "
                "Include detailed explanations, nuanced considerations, broader implications, "
                "and thorough exploration of edge cases and alternative viewpoints."
            )

    def _create_thinking_agents(self) -> List[Agent]:
        perception_agent = Agent(
            role="Core Pattern Analyzer",
            goal="Extract and organize fundamental patterns from input, preparing them for contextual integration",
            backstory="You are specialized in identifying foundational patterns in information, \
            similar to how the brain's sensory regions detect key features. Your process mirrors \
            how the brain transforms raw input into meaningful patterns, enabling deeper analysis. \
            You break down complex inputs into essential components and relationships.",
            verbose=self.verbose
        )

        context_agent = Agent(
            role="Context Integration Specialist",
            goal="Transform pattern analysis into contextually-rich frameworks",
            backstory="You excel at weaving individual patterns into rich contextual frameworks, \
            similar to how the brain's associative regions create meaning from separate elements. \
            You build comprehensive understanding by connecting current patterns with relevant \
            background knowledge, creating complete contextual pictures for expert analysis.",
            verbose=self.verbose
        )

        return [perception_agent, context_agent]

    def _create_expert_agents(self, specialization: Optional[str] = None) -> List[Agent]:
        # Modify agent backstories based on specialization if provided
        specialization_context = f" with specific expertise in {specialization}" if specialization else ""
        
        expert1 = Agent(
            role=f"Primary Domain Expert{specialization_context}",
            goal="Provide focused, domain-specific insights based on contextual patterns",
            backstory=f"You represent deep specialized processing capability{specialization_context}, similar to how \
            dedicated brain regions develop expertise in specific types of information processing. \
            Your analysis draws from extensive domain knowledge to evaluate patterns within their \
            specific context, highlighting critical factors and potential implications.",
            verbose=self.verbose
        )

        expert2 = Agent(
            role=f"Secondary Domain Expert{specialization_context}",
            goal="Enrich primary analysis with complementary domain insights",
            backstory=f"You provide essential alternative perspectives{specialization_context}, similar to how the brain \
            processes information through complementary pathways. Your expertise offers different \
            but related viewpoints that enrich the primary analysis, identifying additional factors \
            and alternative interpretations.",
            verbose=self.verbose
        )

        return [expert1, expert2]

    def _create_director_agent(self, complexity: int = 5, specialization: Optional[str] = None) -> Agent:
        complexity_guidance = self._get_complexity_instructions(complexity)
        
        # Modify director backstory to include specialization context
        specialization_context = f" with {specialization} domain expertise" if specialization else ""
        
        return Agent(
            role=f"Strategic Director{f' ({str(specialization or "General")})' if specialization else ''}",
            goal=f"Synthesize analyses according to complexity level {complexity}/10: {complexity_guidance}",
            backstory=f"You function like the brain's executive regions{specialization_context}, integrating diverse \
            analyses into coherent understanding. Your role is to synthesize expert insights \
            into conclusions at the appropriate complexity level while maintaining accuracy. \
            Follow the complexity guidance strictly.",
            verbose=self.verbose
        )

    def _create_thinking_crew(self) -> Crew:
        agents = self._create_thinking_agents()
        tasks = [
            Task(
                description=(
                    "For the question: '{input}', identify and analyze fundamental patterns. "
                    "Break down the input into essential components and relationships, "
                    "extracting key elements that will form the basis for higher-level processing."
                ),
                agent=agents[0],
                expected_output=(
                    "A structured analysis of core patterns and their relationships, "
                    "organized to facilitate contextual integration"
                )
            ),
            Task(
                description=(
                    "Using the identified patterns from '{input}', construct a comprehensive "
                    "contextual framework. Integrate historical knowledge, current implications, "
                    "and relevant background information to create a complete picture for expert analysis."
                ),
                agent=agents[1],
                expected_output=(
                    "Rich contextual framework that connects identified patterns with "
                    "broader understanding and implications"
                )
            )
        ]
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def _create_expert_crew(self, specialization: Optional[str] = None) -> Crew:
        agents = self._create_expert_agents(specialization)
        tasks = [
            Task(
                description=(
                    "Analyze '{input}' and the provided context through your primary domain "
                    "expertise. Focus on critical factors, potential implications, and "
                    "domain-specific insights based on the contextual patterns."
                ),
                agent=agents[0],
                expected_output=(
                    "Detailed primary domain analysis highlighting key insights, "
                    "critical factors, and specific implications"
                )
            ),
            Task(
                description=(
                    "Examine '{input}' from your complementary domain perspective, "
                    "considering the primary analysis. Identify additional factors, "
                    "alternative interpretations, and enriching viewpoints."
                ),
                agent=agents[1],
                expected_output=(
                    "Complementary analysis providing alternative perspectives and "
                    "additional considerations that enrich understanding"
                )
            )
        ]
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def _create_collaboration_crew(self, specialization: Optional[str] = None, complexity: int = 5) -> Crew:
        director = self._create_director_agent(complexity, specialization)
        experts = self._create_expert_agents(specialization)
        
        complexity_guidance = self._get_complexity_instructions(complexity)
        
        tasks = [
            Task(
                description=(
                    f"For the question '{{input}}', evaluate and integrate all expert analyses. "
                    f"Your response MUST follow this complexity guidance: {complexity_guidance} "
                    f"This is complexity level {complexity}/10, so strictly maintain that level of detail."
                ),
                agent=director,
                expected_output=(
                    f"Response at complexity level {complexity}/10 with appropriate detail level and format"
                )
            )
        ]
        
        return Crew(
            agents=[director, *experts],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose
        )

    def process(self, input_data: str, domain: Optional[str] = None, 
                specialization: Optional[str] = None, complexity: int = 5) -> str:
        """
        Process input through the complete thinking and expert analysis pipeline.
        
        Args:
            input_data: The question or problem to analyze
            domain: Optional domain context to specialize the analysis
            specialization: Optional specific area of expertise
            complexity: Desired complexity level (1-10, where 1 is most concise)
        """
        try:
            if self.verbose:
                print(f"\n🧠 Starting analysis of: {input_data}")
                if domain:
                    print(f"Domain context: {domain}")
                if specialization:
                    print(f"Specialization: {specialization}")
                print(f"Complexity level: {complexity}")
            
            # Create crews with current parameters
            self.thinking_crew = self._create_thinking_crew()
            self.expert_crew = self._create_expert_crew(specialization)
            self.collaboration_crew = self._create_collaboration_crew(specialization, complexity)
            
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
            
            # Final synthesis with complexity guidance
            complexity_guidance = self._get_complexity_instructions(complexity)
            final_result = self.collaboration_crew.kickoff(
                inputs={
                    'input': input_data,
                    'expert_analysis': expert_result,
                    'complexity_guidance': complexity_guidance,
                    'complexity_level': complexity
                }
            )
            
            if self.verbose:
                print("\n✅ Analysis complete")
            
            return str(final_result)
        
        except Exception as e:
            error_msg = f"Processing error: {str(e)}"
            logger.error(error_msg)
            return error_msg