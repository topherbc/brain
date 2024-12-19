from crewai import Agent
from ..tools import risk_evaluator

class RiskAssessor:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Risk Assessor",
            role="Evaluate potential risks and rewards",
            tools=[risk_evaluator],
            goal="Identify and assess potential risks and benefits",
            backstory="Models the amygdala's role in threat detection and risk assessment.",
            verbose=True
        )