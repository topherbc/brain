from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from pydantic import BaseModel, Field
from typing import List, Optional
from textwrap import dedent

class SequenceInput(BaseModel):
    """Input model for sequence analysis"""
    sequence: List[int] = Field(..., description="The numerical sequence to analyze")
    context: Optional[str] = Field(None, description="Additional context about the sequence")
    requirements: Optional[List[str]] = Field(default_factory=list, description="Specific analysis requirements")

class SequenceAnalysis(BaseModel):
    """Output model for sequence analysis"""
    patterns: List[str] = Field(..., description="Identified patterns in the sequence")
    predictions: List[int] = Field(..., description="Predicted next values")
    mathematical_properties: List[str] = Field(..., description="Mathematical properties found")
    confidence: float = Field(..., ge=0, le=1, description="Confidence level in the analysis")
    applications: Optional[List[str]] = Field(default_factory=list, description="Potential applications or contexts")

def create_sequence_crew(sequence_input: SequenceInput) -> Crew:
    """Create a crew for sequence analysis"""
    
    # Pattern Recognition Specialist
    pattern_analyst = Agent(
        role="Pattern Recognition Specialist",
        goal="Identify numerical patterns and predict future values",
        backstory=dedent("""
            Expert in pattern recognition with deep experience in mathematical sequences.
            Skilled at identifying underlying patterns and making predictions.
            Focused on finding both obvious and subtle patterns in numerical sequences.
        """),
        allow_delegation=True
    )

    # Mathematical Analyst
    mathematician = Agent(
        role="Mathematical Analyst",
        goal="Analyze mathematical properties and relationships",
        backstory=dedent("""
            Mathematics expert specializing in sequence analysis and number theory.
            Identifies mathematical principles, formulas, and relationships within sequences.
            Provides rigorous mathematical analysis and proofs when possible.
        """),
        allow_delegation=True
    )

    # Research Analyst
    researcher = Agent(
        role="Research Analyst",
        goal="Research sequence origins and real-world applications",
        backstory=dedent("""
            Expert in mathematical research with vast knowledge of famous sequences.
            Connects patterns to known mathematical concepts and their applications.
            Provides historical context and practical uses of identified sequences.
        """),
        allow_delegation=True
    )

    # Information Synthesizer
    synthesizer = Agent(
        role="Information Synthesizer",
        goal="Integrate all findings into a comprehensive analysis",
        backstory=dedent("""
            Expert at combining multiple analytical perspectives into clear insights.
            Skilled at explaining complex mathematical concepts in accessible terms.
            Creates cohesive summaries that highlight key findings and implications.
        """),
        allow_delegation=False
    )

    # Create tasks
    pattern_task = Task(
        description=f"""
            Analyze this sequence: {sequence_input.sequence}
            1. Identify any recurring patterns
            2. Look for growth rates or ratios between terms
            3. Predict the next 3 values in the sequence
            4. Assign a confidence level to your predictions
            Context: {sequence_input.context if sequence_input.context else 'None provided'}
        """,
        agent=pattern_analyst
    )

    math_task = Task(
        description=f"""
            Perform mathematical analysis on: {sequence_input.sequence}
            1. Identify mathematical properties
            2. Find any mathematical formulas that generate this sequence
            3. Note any special mathematical relationships
            4. Document any interesting mathematical features
        """,
        agent=mathematician
    )

    research_task = Task(
        description=f"""
            Research this sequence: {sequence_input.sequence}
            1. Identify if this matches any known mathematical sequences
            2. Find potential real-world applications
            3. Note any historical significance
            4. Look for similar patterns in nature or science
        """,
        agent=researcher
    )

    synthesis_task = Task(
        description="""
            Create a comprehensive analysis combining all findings:
            1. Summarize key patterns and properties
            2. Evaluate confidence in predictions
            3. Highlight most significant discoveries
            4. Suggest practical applications
        """,
        agent=synthesizer
    )

    # Create crew with sequential process
    crew = Crew(
        agents=[pattern_analyst, mathematician, researcher, synthesizer],
        tasks=[pattern_task, math_task, research_task, synthesis_task],
        process=Process.sequential
    )

    return crew

def analyze_sequence(sequence: List[int], context: Optional[str] = None, requirements: Optional[List[str]] = None) -> SequenceAnalysis:
    """Analyze a numerical sequence using a crew of AI agents"""
    
    # Create input model
    sequence_input = SequenceInput(
        sequence=sequence,
        context=context,
        requirements=requirements or []
    )
    
    # Create and run crew
    crew = create_sequence_crew(sequence_input)
    result = crew.kickoff()
    
    # Parse results into output model
    # Note: This needs to be adapted based on the actual structure of crew results
    # This is a placeholder for demonstration
    analysis = SequenceAnalysis(
        patterns=["Pattern 1", "Pattern 2"],  # Parse from result
        predictions=[1, 2, 3],  # Parse from result
        mathematical_properties=["Property 1", "Property 2"],  # Parse from result
        confidence=0.95,  # Parse from result
        applications=["Application 1", "Application 2"]  # Parse from result
    )
    
    return analysis