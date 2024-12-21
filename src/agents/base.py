from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from crewai import Agent

class BaseAgent(ABC):
    """Base class for all cognitive agents."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the base agent.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._crew_agent = None
        self._initialize_agent()
    
    @abstractmethod
    def _get_agent_config(self) -> Dict[str, Any]:
        """Get agent-specific configuration.
        
        Returns:
            Dictionary containing agent configuration
        """
        pass
    
    def _initialize_agent(self):
        """Initialize the CrewAI agent with configuration."""
        config = self._get_agent_config()
        self._crew_agent = Agent(**config)
    
    @property
    def crew_agent(self) -> Agent:
        """Get the underlying CrewAI agent.
        
        Returns:
            CrewAI Agent instance
        """
        return self._crew_agent