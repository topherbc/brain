import os
import logging
from typing import List, Optional, Any, Dict
from crewai import Crew, Task, Process, Agent
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv

from .agents.sensory import SensoryAgent
from .memory.memory_store import MemoryStore
from .tools.text_analysis import TextAnalysisTool
from .tools.analysis import AnalysisTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CognitiveCrew(BaseModel):
    """Enhanced cognitive processing system with memory and tools"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.memory = MemoryStore()
        self.crew = self._initialize_crew()
    
    def _initialize_crew(self) -> Crew:
        """Initialize the cognitive processing crew with enhanced capabilities"""
        # Initialize agents with tools
        agents = self._create_agents()
        
        # Create tasks with memory integration
        tasks = self._create_tasks(agents)
        
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
    
    def _create_agents(self) -> List[Agent]:
        """Create enhanced agents with tools and memory integration"""
        # Create text analysis tools
        text_tools = [
            TextAnalysisTool.create_keyword_extraction_tool(),
            TextAnalysisTool.create_intent_recognition_tool()
        ]
        
        # Create analysis tools
        analysis_tools = [
            AnalysisTool.create_pattern_analysis_tool(),
            AnalysisTool.create_risk_assessment_tool()
        ]
        
        # Initialize agents with appropriate tools
        sensory_agent = SensoryAgent(verbose=self.verbose)
        pattern_agent = self._create_pattern_recognition_agent(analysis_tools)
        memory_agent = self._create_memory_agent()
        risk_agent = self._create_risk_assessment_agent(analysis_tools)
        analytical_agent = self._create_analytical_agent()
        specialist_agent = self._create_specialist_agent()
        executive_agent = self._create_executive_agent()
        
        return [
            sensory_agent.create(),
            pattern_agent,
            memory_agent,
            risk_agent,
            analytical_agent,
            specialist_agent,
            executive_agent
        ]
    
    def _create_pattern_recognition_agent(self, tools: List[Tool]) -> Agent:
        """Create pattern recognition agent with analysis tools"""
        return Agent(
            role="Cognitive Pattern Analyst",
            goal="Identify complex patterns and relationships in processed data",
            backstory=(
                "Expert in recognizing complex patterns and relationships in data. "
                "Uses advanced analytical tools to uncover hidden connections and "
                "structural patterns that inform higher-level cognitive processing."
            ),
            tools=tools,
            verbose=self.verbose
        )
    
    def _create_memory_agent(self) -> Agent:
        """Create memory agent with enhanced context management"""
        return Agent(
            role="Memory Integration Specialist",
            goal="Manage and integrate information across different memory systems",
            backstory=(
                "Specialist in memory management and context integration. Coordinates "
                "between working memory, short-term, and long-term storage to maintain "
                "coherent and accessible cognitive context."
            ),
            tools=[],
            verbose=self.verbose
        )
    
    def _create_risk_assessment_agent(self, tools: List[Tool]) -> Agent:
        """Create risk assessment agent with analytical tools"""
        return Agent(
            role="Risk Analysis Specialist",
            goal="Evaluate potential risks and uncertainties in cognitive processing",
            backstory=(
                "Expert in identifying and assessing potential risks and uncertainties "
                "in cognitive processing. Uses specialized tools to analyze edge cases "
                "and potential failure modes in understanding and reasoning."
            ),
            tools=tools,
            verbose=self.verbose
        )
    
    def _create_analytical_agent(self) -> Agent:
        """Create analytical agent for high-level reasoning"""
        return Agent(
            role="Advanced Reasoning Specialist",
            goal="Perform sophisticated analysis and generate nuanced insights",
            backstory=(
                "High-level cognitive specialist focusing on complex reasoning and "
                "insight generation. Integrates multiple streams of processed information "
                "to develop sophisticated understanding and actionable conclusions."
            ),
            tools=[],
            verbose=self.verbose
        )
    
    def _create_specialist_agent(self) -> Agent:
        """Create domain specialist agent"""
        return Agent(
            role="Domain Expert",
            goal="Provide domain-specific expertise and contextual understanding",
            backstory=(
                "Domain specialist capable of applying specific expertise to enhance "
                "cognitive processing. Provides crucial domain context and specialized "
                "knowledge to improve understanding and decision-making."
            ),
            tools=[],
            verbose=self.verbose
        )
    
    def _create_executive_agent(self) -> Agent:
        """Create executive agent for final synthesis"""
        return Agent(
            role="Executive Integration Specialist",
            goal="Synthesize all processed information into coherent final output",
            backstory=(
                "Executive-level specialist responsible for final integration and "
                "synthesis of all processed information. Ensures coherent, actionable "
                "output that effectively addresses the original input requirements."
            ),
            tools=[],
            verbose=self.verbose
        )
    
    def _create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Create enhanced tasks with memory integration and error handling"""
        return [
            Task(
                description=(
                    "Process raw input through sensory analysis. Extract key features, "
                    "intent, and semantic signals. Store results in working memory."
                ),
                agent=agents[0]
            ),
            Task(
                description=(
                    "Analyze extracted features for patterns and relationships. "
                    "Use pattern analysis tools to identify structural connections. "
                    "Update working memory with identified patterns."
                ),
                agent=agents[1]
            ),
            Task(
                description=(
                    "Integrate current processing with historical context. "
                    "Manage memory systems and maintain cognitive context. "
                    "Ensure relevant past information informs current processing."
                ),
                agent=agents[2]
            ),
            Task(
                description=(
                    "Assess risks and uncertainties in current understanding. "
                    "Use risk assessment tools to identify potential issues. "
                    "Update working memory with risk analysis results."
                ),
                agent=agents[3]
            ),
            Task(
                description=(
                    "Perform high-level analysis of integrated information. "
                    "Generate sophisticated insights and understanding. "
                    "Store analytical results in working memory."
                ),
                agent=agents[4]
            ),
            Task(
                description=(
                    "Apply domain-specific expertise to enhance understanding. "
                    "Provide specialized context and knowledge. "
                    "Update working memory with expert insights."
                ),
                agent=agents[5]
            ),
            Task(
                description=(
                    "Synthesize all processed information into final output. "
                    "Ensure coherent and actionable conclusions. "
                    "Store final results in long-term memory."
                ),
                agent=agents[6]
            )
        ]
    
    def process_input(self, input_data: Any, domain: Optional[str] = None) -> Dict:
        """Process input through enhanced cognitive pipeline with error handling"""
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            # Store input in short-term memory
            self.memory.store_short_term('current_input', input_data)
            
            if domain:
                # Update specialist agent with domain context
                self.crew.agents[5].backstory = (
                    f"Domain expert specialized in {domain}. Provides deep expertise "
                    f"and contextual understanding specific to {domain} to enhance "
                    "cognitive processing and decision-making."
                )
            
            # Process input through crew
            result = self.crew.kickoff(
                inputs={
                    'input': input_data,
                    'domain': domain,
                    'context': self.memory.get_working_memory('current_context')
                }
            )
            
            # Store results in memory
            self.memory.store_long_term(
                f'result_{datetime.now().isoformat()}',
                {
                    'input': input_data,
                    'domain': domain,
                    'result': result
                }
            )
            
            return {
                'status': 'success',
                'result': result,
                'context': self.memory.get_working_memory('current_context')
            }
            
        except Exception as e:
            error_msg = f"Cognitive processing error: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'error': error_msg,
                'context': self.memory.get_working_memory('current_context')
            }

def main():
    """Main function for testing the enhanced cognitive system"""
    cognitive_crew = CognitiveCrew(verbose=True)
    
    test_inputs = [
        ("Analyze the implications of artificial general intelligence", "AI and ethics"),
        ("What are the best practices for sustainable urban development?", "urban planning"),
        ("How can we improve healthcare accessibility?", "healthcare policy")
    ]
    
    for input_text, domain in test_inputs:
        print(f"\nProcessing: {input_text}")
        result = cognitive_crew.process_input(input_text, domain)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()