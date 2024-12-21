# Brain - Cognitive Architecture with CrewAI

A sophisticated cognitive architecture implementing brain-inspired AI agents using CrewAI. This system simulates different aspects of cognitive processing through specialized agents working in coordination.

## Features

- Multiple specialized cognitive agents (sensory, pattern recognition, memory, etc.)
- Persistent memory system with short-term and long-term storage
- Enhanced error handling and validation
- Detailed logging system
- Domain-specific processing capabilities
- Tool integration for advanced analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/topherbc/brain.git
cd brain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your configuration:
```env
OPENAI_API_KEY=your_api_key_here
VERBOSE=True
```

## Usage

Basic usage:
```python
from src.brain import CognitiveCrew

# Initialize the cognitive system
crew = CognitiveCrew(verbose=True)

# Process input
result = crew.process_input(
    "Your input text here",
    domain="optional domain specification"
)

# Handle results
if result['status'] == 'success':
    print(result['result'])
else:
    print(f"Error: {result['error']}")
```

## Examples

Check the `examples` directory for more detailed usage examples:

- `basic_decision.py`: Simple decision-making example
- `complex_analysis.py`: Complex analysis with domain expertise
- `memory_test.py`: Memory system integration testing

## Architecture

The system implements a brain-inspired architecture with the following components:

1. Sensory Processing
   - Initial input processing
   - Feature extraction
   - Semantic signal detection

2. Pattern Recognition
   - Pattern identification
   - Structural analysis
   - Relationship mapping

3. Memory Integration
   - Context management
   - Information persistence
   - Memory consolidation

4. Risk Assessment
   - Uncertainty evaluation
   - Edge case analysis
   - Limitation identification

5. Analytical Processing
   - Deep analysis
   - Insight generation
   - Complex reasoning

6. Domain Expertise
   - Specialized knowledge application
   - Context-specific processing

7. Executive Function
   - Final synthesis
   - Output generation
   - Decision implementation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
