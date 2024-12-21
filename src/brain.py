"""Brain-inspired cognitive architecture using CrewAI."""

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew, Process
from .tools.analysis import TextAnalysisTool, DataAnalysisTool

class CognitiveCrew:
    """Brain-inspired cognitive architecture implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the cognitive architecture.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.tools = self._initialize_tools()
        self.agents = self._initialize_agents()
        self.crew = self._create_crew()
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize analysis tools.
        
        Returns:
            Dictionary of initialized tools
        """
        return {
            'text_analysis': TextAnalysisTool(),
            'data_analysis': DataAnalysisTool()
        }
    
    def _initialize_agents(self) -> Dict[str, Agent]:
        """Initialize cognitive agents.
        
        Returns:
            Dictionary of initialized agents
        """
        agents = {}
        
        # Sensory Processing Agent
        agents['sensory'] = Agent(
            name="Sensory Processing",
            goal="Process and extract features from input data",
            backstory="Specialized in initial data processing and feature extraction",
            tools=[self.tools['text_analysis']],
            allow_delegation=True
        )
        
        # Pattern Recognition Agent
        agents['pattern'] = Agent(
            name="Pattern Recognition",
            goal="Identify patterns and relationships in processed data",
            backstory="Expert at recognizing complex patterns and structures",
            tools=[self.tools['data_analysis']],
            allow_delegation=True
        )
        
        # Integration Agent
        agents['integration'] = Agent(
            name="Integration",
            goal="Synthesize information and coordinate responses",
            backstory="Specialized in combining multiple sources of information",
            tools=[self.tools['text_analysis'], self.tools['data_analysis']],
            allow_delegation=True
        )
        
        return agents
    
    def _create_crew(self) -> Crew:
        """Create the cognitive crew.
        
        Returns:
            Initialized CrewAI Crew
        """
        return Crew(
            agents=list(self.agents.values()),
            tasks=[],
            process=Process.sequential
        )
    
    def process(self, input_data: Any) -> Any:
        """Process input through the cognitive architecture.
        
        Args:
            input_data: Input data to be processed
            
        Returns:
            Results from cognitive processing
        """
        # Create task sequence
        tasks = [
            Task(
                description="Extract features and process initial input",
                agent=self.agents['sensory'],
                context={"input_data": input_data}
            ),
            Task(
                description="Identify patterns and relationships",
                agent=self.agents['pattern']
            ),
            Task(
                description="Integrate and synthesize results",
                agent=self.agents['integration']
            )
        ]
        
        # Update crew tasks
        self.crew.tasks = tasks
        
        # Execute cognitive pipeline
        return self.crew.kickoff()
    
    def add_agent(self, name: str, agent: Agent):
        """Add a new agent to the crew.
        
        Args:
            name: Identifier for the agent
            agent: Agent instance to add
        """
        self.agents[name] = agent
        self.crew = self._create_crew()  # Recreate crew with new agent
    
    def add_tool(self, name: str, tool: Any):
        """Add a new tool for agents to use.
        
        Args:
            name: Identifier for the tool
            tool: Tool instance to add
        """
        self.tools[name] = tool
        # Recreate agents with updated tools if needed
        self._initialize_agents()
        self.crew = self._create_crew()