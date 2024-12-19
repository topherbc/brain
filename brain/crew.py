from typing import List
from crewai import Agent, Task, Crew
from .agents.sensory import SensoryProcessor
from .agents.memory import MemoryManager
from .agents.emotional import EmotionalEvaluator
from .agents.pattern import PatternRecognizer
from .agents.risk import RiskAssessor
from .agents.executive import ExecutiveController

class CognitiveCrew:
    def __init__(self):
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()
    
    def _create_agents(self) -> dict:
        """Initialize all cognitive agents"""
        return {
            'sensory': SensoryProcessor.create(),
            'memory': MemoryManager.create(),
            'emotional': EmotionalEvaluator.create(),
            'pattern': PatternRecognizer.create(),
            'risk': RiskAssessor.create(),
            'executive': ExecutiveController.create()
        }
    
    def _create_tasks(self) -> List[Task]:
        """Create the sequence of cognitive processing tasks"""
        tasks = [
            Task(
                description="Process and clean incoming sensory data",
                agent=self.agents['sensory'],
                context="Clean and format the raw input for further processing",
                expected_output="Preprocessed data ready for analysis"
            ),
            Task(
                description="Retrieve relevant memories and context",
                agent=self.agents['memory'],
                context="Access and provide relevant historical context",
                expected_output="Contextual information from memory"
            ),
            Task(
                description="Analyze emotional content and implications",
                agent=self.agents['emotional'],
                context="Evaluate emotional aspects and social impact",
                expected_output="Emotional analysis results"
            ),
            Task(
                description="Identify patterns and make predictions",
                agent=self.agents['pattern'],
                context="Detect patterns and predict potential outcomes",
                expected_output="Pattern analysis and predictions"
            ),
            Task(
                description="Assess risks and benefits",
                agent=self.agents['risk'],
                context="Evaluate potential risks and rewards",
                expected_output="Risk assessment report"
            ),
            Task(
                description="Make executive decision",
                agent=self.agents['executive'],
                context="Synthesize all analyses into final decision",
                expected_output="Final decision and rationale"
            )
        ]
        
        # Set up task dependencies
        for i in range(1, len(tasks)):
            tasks[i].context += f"\nUse output from previous task: {tasks[i-1].expected_output}"
        
        return tasks
    
    def _create_crew(self) -> Crew:
        """Create the cognitive crew with all agents and tasks"""
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True
        )
    
    def process_input(self, input_data: str) -> dict:
        """Process input through the cognitive pipeline
        
        Args:
            input_data: The input data to process
            
        Returns:
            dict: The final decision and supporting analysis
        """
        # Set initial context for first task
        self.tasks[0].context = f"Input data to process: {input_data}"
        
        # Process all tasks in sequence
        result = self.crew.kickoff()
        
        # Parse and return final result
        try:
            return {
                'decision': result[-1],  # Final executive decision
                'analysis': {
                    'sensory': result[0],
                    'memory': result[1],
                    'emotional': result[2],
                    'pattern': result[3],
                    'risk': result[4]
                }
            }
        except Exception as e:
            return {
                'error': f"Error processing input: {str(e)}",
                'raw_result': result
            }