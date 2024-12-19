from crewai import Agent
from ..tools import MemoryDatabase

class MemoryManager:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Memory Manager",
            role="Store and retrieve contextual information",
            tools=[MemoryDatabase()],
            goal="Manage and recall relevant data",
            backstory="An AI agent responsible for maintaining and retrieving contextual knowledge.",
            verbose=True
        )