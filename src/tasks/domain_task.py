from crewai import Task
from src.agents.director import DomainDirector

class DomainTaskHandler:
    @staticmethod
    def create_explanation_task(query, domain):
        """
        Create a specialized task for generating domain-specific explanations
        
        Args:
            query (str): The specific question or topic to explain
            domain (str): The domain of the explanation
        
        Returns:
            Task: A CrewAI task tailored to the specific domain
        """
        # Create a domain-specialized director
        director_agent = DomainDirector.create_specialized_director(domain)
        
        # Create a task with domain-specific context
        task = Task(
            description=f"""
            Provide a comprehensive and nuanced explanation for the following query:
            Query: {query}
            Domain: {domain}
            
            Requirements:
            - Craft a detailed, accurate explanation
            - Contextualize the answer within the specific domain
            - Use appropriate technical depth for the query
            - Ensure clarity and accessibility of the explanation
            - Incorporate interdisciplinary insights if relevant
            """,
            agent=director_agent,
            expected_output="A well-structured, insightful explanation that addresses the query comprehensively."
        )
        
        return task

    @staticmethod
    def handle_query(query, domain='default'):
        """
        Main method to handle queries across different domains
        
        Args:
            query (str): The input query
            domain (str, optional): The specific domain. Defaults to 'default'.
        
        Returns:
            str: A generated explanation
        """
        # Create the task
        explanation_task = DomainTaskHandler.create_explanation_task(query, domain)
        
        # Setup the crew (to be implemented in crew configuration)
        # This is a placeholder for the actual crew setup
        # crew = Crew(agents=[director_agent], tasks=[explanation_task])
        # result = crew.kickoff()
        
        # Temporary direct method (to be replaced with CrewAI workflow)
        # result = explanation_task.agent.run(explanation_task.description)
        
        return f"Domain-specific explanation for '{query}' in {domain} domain would be generated here."

# Example usage
# explanation = DomainTaskHandler.handle_query("Why is the sky blue?", "science")