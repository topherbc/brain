import re
from typing import Dict, Any
from crewai import Agent
from langchain_openai import ChatOpenAI

class DomainDirector:
    @staticmethod
    def detect_domain(query: str) -> str:
        """
        Intelligently detect the domain of a given query
        
        Args:
            query (str): The input query to analyze
        
        Returns:
            str: Detected domain
        """
        # Comprehensive domain detection logic
        domain_patterns = {
            'science': [
                r'\bphysics\b', r'\bchemistry\b', r'\bbiology\b', 
                r'\bscientific\b', r'\bexperiment\b', r'\bresearch\b',
                r'\bnatural phenomena\b'
            ],
            'technology': [
                r'\btech\b', r'\bcomputer\b', r'\balgorithm\b', 
                r'\bprogramming\b', r'\binnovation\b'
            ],
            'history': [
                r'\bhistorical\b', r'\bpast\b', r'\bevent\b', 
                r'\bcivilization\b', r'\bculture\b'
            ],
            'geography': [
                r'\bplanet\b', r'\bworld\b', r'\bcontinent\b', 
                r'\blandscape\b', r'\bmountain\b', r'\bocean\b'
            ]
        }
        
        # Check for domain-specific keywords
        for domain, patterns in domain_patterns.items():
            if any(re.search(pattern, query, re.IGNORECASE) for pattern in patterns):
                return domain
        
        return 'general'

    @staticmethod
    def _create_director_agent(query: str, domain: str) -> Agent:
        """
        Create a specialized director agent based on query and domain
        
        Args:
            query (str): The original query
            domain (str): The detected or specified domain
        
        Returns:
            Agent: A CrewAI agent specialized for the given domain and query
        """
        # Domain-specific role configurations
        domain_configs = {
            'science': {
                'role': 'Scientific Inquiry Specialist',
                'goal': f'Provide precise scientific explanation for: {query}',
                'backstory': 'An expert researcher dedicated to breaking down complex scientific concepts with clarity and depth.'
            },
            'technology': {
                'role': 'Technical Explanation Architect',
                'goal': f'Demystify technological aspects of: {query}',
                'backstory': 'A seasoned technology translator who converts complex tech concepts into understandable insights.'
            },
            'history': {
                'role': 'Historical Context Curator',
                'goal': f'Provide comprehensive historical context for: {query}',
                'backstory': 'A meticulous historian who weaves intricate narratives and provides deep contextual understanding.'
            },
            'general': {
                'role': 'Interdisciplinary Knowledge Synthesizer',
                'goal': f'Generate a comprehensive explanation for: {query}',
                'backstory': 'A versatile knowledge expert capable of drawing insights from multiple domains.'
            }
        }
        
        # Select configuration, defaulting to general
        config = domain_configs.get(domain, domain_configs['general'])
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            llm=ChatOpenAI(model="gpt-4-turbo")
        )

    @staticmethod
    def create_agent(query: str, specified_domain: str = None) -> Agent:
        """
        Main method to create a domain-specialized agent
        
        Args:
            query (str): The input query
            specified_domain (str, optional): Manually specified domain
        
        Returns:
            Agent: A specialized CrewAI agent
        """
        # Use specified domain or detect domain
        domain = specified_domain or DomainDirector.detect_domain(query)
        
        # Create and return specialized agent
        return DomainDirector._create_director_agent(query, domain)

# Example usage
# agent = DomainDirector.create_agent("Why is the sky blue?")