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
│   └── basic_decision.py
├── requirements.txt
└── README.md
```

## Usage

```python
from brain.crew import CognitiveCrew

# Initialize the cognitive crew
crew = CognitiveCrew()

# Process input and get decision
result = crew.process_input("Your input here")
```

## License

MIT License
