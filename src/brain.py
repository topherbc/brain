import os
import logging
from typing import List, Optional, Any, Dict
from crewai import Agent, Task, Crew, Process
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AttentionState:
    """Manages attention focus and priorities in cognitive processing"""
    def __init__(self):
        self.focus_areas = defaultdict(float)  # Key areas of current focus
        self.priorities = defaultdict(float)   # Priority weights
        self.salience = defaultdict(float)     # Bottom-up salience scores
        
    def update_salience(self, text: str):
        """Update bottom-up salience based on input text"""
        # Simple keyword-based salience
        words = text.lower().split()
        for word in words:
            self.salience[word] += 1
        
        # Normalize salience scores
        max_score = max(self.salience.values()) if self.salience else 1
        for word in self.salience:
            self.salience[word] /= max_score
    
    def update_priorities(self, focus_dict: Dict[str, float]):
        """Update top-down priority weights"""
        self.priorities.update(focus_dict)
        
    def get_focus_areas(self) -> Dict[str, float]:
        """Combine salience and priorities to determine focus areas"""
        self.focus_areas.clear()
        
        # Combine bottom-up and top-down signals
        for key in set(self.salience) | set(self.priorities):
            self.focus_areas[key] = (
                self.salience.get(key, 0) * 0.4 +  # Bottom-up weight
                self.priorities.get(key, 0) * 0.6   # Top-down weight
            )
        
        return dict(self.focus_areas)

class CognitiveCrew:
    def __init__(self, verbose: bool = False):
        """
        Initialize the Cognitive Crew with configurable verbosity
        
        :param verbose: Enables detailed logging and output
        """
        self.verbose = verbose
        self.attention = AttentionState()
        self.crew_instance = self._create_crew()

    def _create_sensory_agent(self) -> Agent:
        """
        Enhanced Sensory Processing Agent with attention mechanism
        """
        return Agent(
            role="Sensory Perception Specialist",
            goal="Extract and prioritize information based on attention focus",
            backstory=(
                "You are the initial filter of cognitive processing. Your role is to:\n"
                "1. Detect salient features in the input\n"
                "2. Apply current attention focus to enhance relevant information\n"
                "3. Suppress less relevant details\n"
                "4. Pass prioritized information to later stages\n\n"
                "Consider both inherent importance (bottom-up) and task relevance (top-down).\n"
                "Mark important elements with [FOCUS] tags and provide attention scores."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_pattern_recognition_agent(self) -> Agent:
        """Pattern Recognition Agent"""
        return Agent(
            role="Cognitive Pattern Analyst",
            goal="Identify patterns with emphasis on attended features",
            backstory=(
                "You specialize in uncovering hidden connections and structural patterns. "
                "Pay special attention to elements marked with [FOCUS] tags. "
                "Create a clear, logical mapping of how different elements interrelate. "
                "Your output should be a structured breakdown of conceptual connections."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    # ... [Other agent creation methods remain the same]

    def _create_executive_agent(self) -> Agent:
        """Enhanced Executive Agent with attention control"""
        return Agent(
            role="Executive Controller",
            goal="Guide attention and processing focus while synthesizing output",
            backstory=(
                "You coordinate attention allocation and synthesize results by:\n"
                "1. Setting processing priorities\n"
                "2. Identifying key areas for detailed analysis\n"
                "3. Adjusting focus based on intermediate results\n"
                "4. Providing feedback for attention modulation\n\n"
                "Tag priority shifts with [ATTENTION] markers and explain rationale."
            ),
            tools=[],
            allow_delegation=False,
            verbose=self.verbose
        )

    def _create_crew(self) -> Crew:
        """Create crew with attention-aware processing"""
        agents = [
            self._create_sensory_agent(),
            self._create_pattern_recognition_agent(),
            self._create_memory_agent(),
            self._create_risk_assessment_agent(),
            self._create_analytical_agent(),
            self._create_specialist_agent(),
            self._create_executive_agent()
        ]

        tasks = [
            Task(
                description=(
                    "Process input with attention focus:\n"
                    "Current focus areas: {attention_focus}\n\n"
                    "Input: '{input}'\n\n"
                    "Extract and prioritize based on attention state.\n"
                    "Mark key elements with [FOCUS] tags."
                ),
                agent=agents[0],
                expected_output="Prioritized features with attention markers"
            ),
            # ... [Other tasks remain the same but with attention context]
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
            model_kwargs={
                "temperature": 0.4,
                "max_tokens": 2000,
                "top_p": 0.8
            }
        )

    def process_input(self, input_data: Any, domain: Optional[str] = None) -> str:
        """Process input with attention mechanisms"""
        try:
            if input_data is None:
                raise ValueError("Input cannot be None")
            
            if self.verbose:
                print(f"\n🧠 Processing Input: '{input_data}'")
            
            # Update attention state
            self.attention.update_salience(str(input_data))
            if domain:
                self.attention.update_priorities({domain: 1.0})
            
            # Get current focus areas
            focus_areas = self.attention.get_focus_areas()
            
            # Process with attention context
            result = self.crew_instance.kickoff(
                inputs={
                    'input': input_data,
                    'attention_focus': focus_areas
                }
            )
            
            if self.verbose:
                print("\n🔍 Focus Areas:")
                for area, score in focus_areas.items():
                    print(f"  - {area}: {score:.2f}")
                print("\n🔬 Final Output:")
                print(result)
            
            return str(result)
        
        except Exception as e:
            error_msg = f"Processing error: {e}"
            logger.error(error_msg)
            return error_msg

def main():
    test_inputs = [
        ("Analyze the environmental impact of electric vehicles, focusing on battery production.", "environmental_science"),
        ("Explain how neural networks process visual information in object recognition.", "cognitive_science"),
        ("Describe the role of mitochondria in cellular energy production.", "cell_biology")
    ]

    crew = CognitiveCrew(verbose=True)
    for input_text, domain in test_inputs:
        print("\n" + "="*50)
        print(f"Processing: {input_text}")
        print("="*50)
        result = crew.process_input(input_text, domain)

if __name__ == "__main__":
    main()