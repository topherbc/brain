from crewai import Agent

class ExecutiveController:
    @staticmethod
    def create() -> Agent:
        return Agent(
            name="Executive Controller",
            role="Coordinate cognitive processes and maintain focus",
            goal="Guide the cognitive process and maintain attention on relevant aspects",
            backstory="Inspired by the prefrontal cortex's role in executive function. Maintains focus, coordinates processes, but does not make final decisions.",
            verbose=True
        )