from crewai import Agent
from langchain_openai import ChatOpenAI

class DomainDirector:
    @staticmethod
    def create_specialized_director(domain):
        """
        Create a specialized director agent based on the input domain.
        
        Args:
            domain (str): The specific domain of inquiry
        
        Returns:
            Agent: A specialized CrewAI agent for the given domain
        """
        domain_specializations = {
            'science': {
                'role': 'Scientific Domain Expert and Research Coordinator',
                'goal': 'Provide comprehensive and accurate scientific explanations by coordinating research and analysis',
                'backstory': 'A seasoned research director with extensive experience in translating complex scientific concepts into clear, understandable narratives. Skilled at breaking down intricate scientific phenomena and guiding interdisciplinary research teams.'
            },
            'technology': {
                'role': 'Technology Innovation and Explanation Strategist',
                'goal': 'Demystify technological concepts and provide in-depth, contextual understanding',
                'backstory': 'A veteran technology consultant who has worked across multiple tech domains, specializing in translating complex technological innovations into accessible insights for diverse audiences.'
            },
            'history': {
                'role': 'Historical Context and Narrative Curator',
                'goal': 'Provide nuanced, well-researched historical explanations with rich contextual understanding',
                'backstory': 'A distinguished historian with expertise in connecting historical events, understanding cultural contexts, and presenting comprehensive historical narratives.'
            },
            'default': {
                'role': 'Interdisciplinary Knowledge Director',
                'goal': 'Provide comprehensive and accurate explanations across various domains',
                'backstory': 'A versatile knowledge coordinator with broad expertise, capable of navigating complex information landscapes and synthesizing insights from multiple perspectives.'
            }
        }

        # Select domain-specific or default configuration
        domain_config = domain_specializations.get(domain.lower(), domain_specializations['default'])

        return Agent(
            role=domain_config['role'],
            goal=domain_config['goal'],
            backstory=domain_config['backstory'],
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            llm=ChatOpenAI(model="gpt-4-turbo")
        )

# Example usage
# director = DomainDirector.create_specialized_director('science')