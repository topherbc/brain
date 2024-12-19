from crewai import Agent
from ..tools import RiskEvaluator

class RiskAssessor:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Risk Assessor",
            role="Evaluate potential risks and rewards",
            tools=[RiskEvaluator()],
            goal="Identify and assess potential risks and benefits",
            backstory="Models the amygdala's role in threat detection and risk assessment.",
            verbose=True
        )