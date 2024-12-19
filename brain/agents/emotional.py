from crewai import Agent
from ..tools import EmotionalAnalyzer

class EmotionalEvaluator:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Emotional Evaluator",
            role="Assess emotional impact and social consequences",
            tools=[EmotionalAnalyzer()],
            goal="Evaluate emotional context and social implications",
            backstory="Represents the limbic system's role in emotional processing and social cognition.",
            verbose=True
        )