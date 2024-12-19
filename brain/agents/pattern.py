from crewai import Agent
from ..tools import PatternAnalyzer

class PatternRecognizer:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Pattern Recognizer",
            role="Identify patterns and predict outcomes",
            tools=[PatternAnalyzer()],
            goal="Detect patterns, anomalies, and make predictions",
            backstory="Similar to the brain's temporal lobe, specialized in recognizing patterns and making predictions.",
            verbose=True
        )