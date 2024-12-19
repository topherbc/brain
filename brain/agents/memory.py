from crewai import Agent
from ..tools import memory_store, memory_retrieve, memory_update, memory_delete

class MemoryManager:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Memory Manager",
            role="Store and retrieve contextual information",
            tools=[memory_store, memory_retrieve, memory_update, memory_delete],
            goal="Manage and recall relevant data",
            backstory="An AI agent responsible for maintaining and retrieving contextual knowledge.",
            verbose=True
        )