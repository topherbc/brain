from crewai import Agent
from ..tools import ConfidenceAnalyzer

class AnalyticalEvaluator:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Analytical Evaluator",
            role="Assess confidence levels and analytical validity",
            tools=[ConfidenceAnalyzer()],
            goal="Evaluate analytical robustness and certainty levels",
            backstory="Validates analytical processes through statistical and logical assessment.",
            verbose=True
        )