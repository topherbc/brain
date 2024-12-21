import os
import logging
from typing import List, Optional
from crewai import Agent, Task, Crew, Process
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# [Previous imports and logging configuration remain the same]

class ThinkingProcess:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Create individual crews
        self.thinking_crew = None
        self.expert_crew = None
        self.collaboration_crew = None

    # [Previous methods remain the same]

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
            role=f"Strategic Director{f' ({specialization or 'General'})' if specialization else ''}",
            goal=f"Synthesize analyses according to complexity level {complexity}/10: {complexity_guidance}",
            backstory=f"You function like the brain's executive regions{specialization_context}, integrating diverse \
            analyses into coherent understanding. Your role is to synthesize expert insights \
            into conclusions at the appropriate complexity level while maintaining accuracy. \
            Follow the complexity guidance strictly.",
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

    # [Rest of the file remains the same]