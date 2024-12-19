# Brain - Cognitive Architecture

A brain-inspired cognitive architecture implementing AI agents using CrewAI.

## Overview

This project implements a cognitive architecture that mirrors the brain's decision-making process using a team of specialized AI agents. Each agent represents different cognitive functions found in the human brain.

## Installation

```bash
# Clone the repository
git clone https://github.com/topherbc/brain.git
cd brain

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
brain/
├── brain/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── sensory.py
│   │   ├── memory.py
│   │   ├── emotional.py
│   │   ├── pattern.py
│   │   ├── risk.py
│   │   └── executive.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── text_cleaner.py
│   │   ├── data_formatter.py
│   │   └── analyzers.py
│   └── crew.py
├── tests/
│   └── __init__.py
├── examples/
│   ├── basic_decision.py
│   ├── test_flow.py
│   └── tasks/
│       ├── task1.txt
│       └── task2.txt
├── requirements.txt
└── README.md
```

## Testing and Execution

### Basic Usage

```python
from brain.crew import CognitiveCrew

# Initialize the cognitive crew
crew = CognitiveCrew()

# Process input and get decision
result = crew.process_input("Your input here")
```

### Testing with Task Files

You can test the system using predefined task files. The project includes example task files in the `examples/tasks/` directory.

1. Run the test flow script:
```bash
python examples/test_flow.py
```

This will process all example tasks and show the decision flow of each agent.

2. Create your own task file:
Task files should include:
- Clear task description
- Context information
- Specific requirements

Example task file format:
```text
[Task Description]

Context:
- Key context point 1
- Key context point 2

Requirements:
- Requirement 1
- Requirement 2
```

### Viewing Agent Decision Flow

To see detailed agent decision flows:

1. Enable verbose mode when initializing:
```python
crew = CognitiveCrew(verbose=True)
```

2. Watch the console output to see:
- Each agent's thought process
- Decision handoffs between agents
- Final consolidated results

### Creating Custom Tests

1. Create a new task file in `examples/tasks/`
2. Run the test flow script with your file:
```python
from examples.test_flow import process_task_file

results = process_task_file('path/to/your/task.txt')
print(results)
```

## License

MIT License
