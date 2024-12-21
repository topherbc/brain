from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from crewai import Crew, Process
import asyncio

from .agents.sensory import SensoryProcessor
from .agents.pattern import PatternRecognizer
from .agents.risk import RiskAssessor
from .agents.analytical import AnalyticalProcessor
from .agents.domain import DomainSpecialist
from .agents.executive import ExecutiveFunction
from .memory.memory_store import MemoryStore
from .tools.analysis import TextAnalysisTool, DataAnalysisTool

class CognitiveCrew(BaseModel):
    """Main cognitive architecture implementation."""
    name: str = Field(default="cognitive_crew", description="Name of the cognitive crew")
    memory_store: MemoryStore = Field(default_factory=MemoryStore)
    
    # Initialize all specialized agents
    agents: Dict[str, Any] = Field(default_factory=lambda: {
        "sensory": SensoryProcessor(),
        "pattern": PatternRecognizer(),
        "risk": RiskAssessor(),
        "analytical": AnalyticalProcessor(),
        "domain": DomainSpecialist(),
        "executive": ExecutiveFunction()
    })
    
    process_order: List[str] = Field(
        default=[
            "sensory",
            "pattern",
            "risk",
            "analytical",
            "domain",
            "executive"
        ],
        description="Order of processing stages"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    async def process_input(self, input_data: Any) -> Dict[str, Any]:
        # Create processing crew
        crew = Crew(
            agents=list(self.agents.values()),
            process=Process.sequential
        )
        
        # Initialize results storage
        stage_results = {}
        stage_metadata = {}
        
        # Sequential processing through all agents
        current_input = input_data
        for stage in self.process_order:
            agent = self.agents[stage]
            
            # Process current stage
            stage_results[stage] = await agent.process(current_input)
            
            # Store stage results in memory
            memory_id = await self.memory_store.store(
                stage_results[stage],
                memory_type="short_term",
                metadata={"stage": stage}
            )
            
            stage_metadata[stage] = {
                "memory_id": memory_id,
                "timestamp": self.memory_store._generate_id()
            }
            
            # Update input for next stage with accumulated results
            current_input = {
                "current": stage_results[stage],
                "previous": stage_results,
                "metadata": stage_metadata
            }
        
        # Extract executive function results (final synthesis)
        final_results = stage_results["executive"]
        
        # Store final results in long-term memory
        final_memory_id = await self.memory_store.store(
            final_results,
            memory_type="long_term",
            metadata={
                "stage": "final_integration",
                "process_history": stage_metadata
            }
        )
        
        # Return complete processing results
        return {
            "result_id": final_memory_id,
            "stages": stage_results,
            "final_synthesis": final_results,
            "metadata": {
                "process_order": self.process_order,
                "stage_metadata": stage_metadata,
                "processing_complete": True
            }
        }
    
    async def retrieve_memory(
        self, 
        memory_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Any:
        return await self.memory_store.retrieve(memory_id, filters)
    
    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
            
        agent = self.agents[agent_name]
        return {
            "name": agent.name,
            "role": agent.role,
            "goal": agent.goal,
            "active": True,
            "configuration": {
                key: value for key, value in agent.__dict__.items()
                if not key.startswith('_')
            }
        }
    
    async def reconfigure_agent(
        self,
        agent_name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
            
        agent = self.agents[agent_name]
        
        # Update agent configuration
        for key, value in config.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
                
        return await self.get_agent_status(agent_name)
    
    async def process_batch(
        self,
        inputs: List[Any],
        batch_size: int = 10
    ) -> List[Dict[str, Any]]:
        results = []
        
        # Process inputs in batches
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.process_input(input_data) for input_data in batch]
            )
            results.extend(batch_results)
            
        return results