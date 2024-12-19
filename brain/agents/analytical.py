from crewai import Agent
from ..tools import confidence_evaluator, confidence_level

class AnalyticalEvaluator:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Analytical Evaluator",
            role="Assess confidence levels and analytical validity",
            tools=[confidence_evaluator, confidence_level],
            goal="Evaluate analytical robustness and certainty levels",
            backstory="Validates analytical processes through statistical and logical assessment.",
            verbose=True
        )