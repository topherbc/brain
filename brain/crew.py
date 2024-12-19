from typing import List
from crewai import Agent, Task, Crew
from .agents.sensory import SensoryProcessor
from .agents.memory import MemoryManager
from .agents.analytical import AnalyticalEvaluator
from .agents.pattern import PatternRecognizer
from .agents.risk import RiskAssessor
from .agents.executive import ExecutiveController
from .agents.specialist import SpecialistSynthesizer

class CognitiveCrew:
    def __init__(self):
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()
    
    def _create_agents(self) -> dict:
        """Initialize cognitive agents"""
        return {
            'sensory': SensoryProcessor.create(),
            'memory': MemoryManager.create(),
            'analytical': AnalyticalEvaluator.create(),
            'pattern': PatternRecognizer.create(),
            'risk': RiskAssessor.create(),
            'executive': ExecutiveController.create(),
            'specialist': SpecialistSynthesizer.create()
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
                description="Assess analytical confidence and validity",
                agent=self.agents['analytical'],
                context="Evaluate analytical robustness and certainty levels",
                expected_output="Analytical confidence assessment"
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
                description="Coordinate cognitive processes",
                agent=self.agents['executive'],
                context="Guide attention and maintain focus on relevant aspects",
                expected_output="Coordinated cognitive state and attention focus"
            ),
            Task(
                description="Synthesize final decision",
                agent=self.agents['specialist'],
                context="Integrate all cognitive inputs into final decision",
                expected_output="Final synthesized decision with rationale"
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
                'decision': result[-1],  # Specialist's final decision
                'analysis': {
                    'sensory': result[0],
                    'memory': result[1],
                    'analytical': result[2],
                    'pattern': result[3],
                    'risk': result[4],
                    'executive': result[5]  # Executive's coordination notes
                }
            }
        except Exception as e:
            return {
                'error': f"Error processing input: {str(e)}",
                'raw_result': result
            }