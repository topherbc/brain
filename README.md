# Brain - Cognitive Architecture with CrewAI

A sophisticated cognitive architecture implementing brain-inspired AI agents using CrewAI. This system simulates different aspects of cognitive processing through specialized agents working in coordination.

## Features

### Core Features
- Multiple specialized cognitive agents (sensory, pattern recognition, memory, etc.)
- Persistent memory system with short-term and long-term storage
- Enhanced error handling and validation
- Detailed logging system
- Domain-specific processing capabilities
- Tool integration for advanced analysis

### Web Interface
- Modern React-based user interface
- Real-time processing feedback
- Domain specification support
- Responsive design with Tailwind CSS
- Error handling and validation

### API
- RESTful API with FastAPI
- Async request processing
- Health monitoring endpoints
- Comprehensive error handling
- CORS support for development

## Quick Start

For detailed setup instructions, see [SETUP.md](SETUP.md).

1. Clone the repository:
```bash
git clone https://github.com/topherbc/brain.git
cd brain
```

2. Install backend dependencies:
```bash
pip install -r api_requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your configuration:
```env
OPENAI_API_KEY=your_api_key_here
VERBOSE=True
```

4. Install frontend dependencies:
```bash
cd web
npm install
```

5. Start the servers:
```bash
# Terminal 1 - Backend
cd api
python main.py

# Terminal 2 - Frontend
cd web
npm run dev
```

## Usage

### Web Interface
Access the web interface at http://localhost:5173

### API Endpoints

```bash
# Process input
POST http://localhost:8000/api/process
Content-Type: application/json

{
    "input": "Your input text here",
    "domain": "optional domain specification"
}

# Check health
GET http://localhost:8000/api/health
```

### Python Library
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

## Architecture

### Brain Architecture
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

### Technical Architecture

1. Frontend (React + Vite)
   - Modern component architecture
   - Real-time state management
   - Tailwind CSS styling
   - shadcn/ui components

2. Backend (FastAPI)
   - Asynchronous request handling
   - RESTful API design
   - Comprehensive error handling
   - Health monitoring

3. Core Processing (CrewAI)
   - Agent coordination
   - Task sequencing
   - Error recovery
   - Domain adaptation

## Examples

Check the `examples` directory for detailed usage examples:

- `basic_decision.py`: Simple decision-making example
- `complex_analysis.py`: Complex analysis with domain expertise
- `memory_test.py`: Memory system integration testing

## Development

### Frontend Development
```bash
cd web
npm run dev
```

### Backend Development
```bash
cd api
python main.py
```

### Core Library Development
```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
