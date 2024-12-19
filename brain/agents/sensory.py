from crewai import Agent
from ..tools import text_cleaner, tokenizer, DataFormatter

class SensoryProcessor:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Sensory Processor",
            role="Preprocess incoming sensory data",
            tools=[text_cleaner, tokenizer, DataFormatter()],
            goal="Prepare data for downstream tasks",
            backstory="An AI agent designed to clean and format raw sensory input for further processing.",
            verbose=True
        )