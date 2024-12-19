# Brain - Cognitive Architecture

A brain-inspired cognitive architecture implementing AI agents using CrewAI.

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/topherbc/brain.git
cd brain
```

2. Create and activate a virtual environment:
```bash
# On Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
# On Linux/Mac:
export OPENAI_API_KEY='your-api-key-here'

# On Windows (Command Prompt):
set OPENAI_API_KEY=your-api-key-here

# On Windows (PowerShell):
$env:OPENAI_API_KEY='your-api-key-here'
```

Alternatively, create a `.env` file in the project root:
```plaintext
OPENAI_API_KEY=your-api-key-here
```

### Running Cognitive Tasks

The project includes several analytical cognitive tasks you can run:

1. Pattern Analysis:
```bash
python run_brain.py examples/tasks/cognitive_pattern_task.txt
```
- Analyzes number sequences
- Identifies patterns
- Predicts next values

2. Decision Analysis:
```bash
python run_brain.py examples/tasks/decision_analysis_task.txt
```
- Evaluates decision paths
- Performs risk assessment
- Provides optimal solutions

3. Logic Puzzle:
```bash
python run_brain.py examples/tasks/logic_puzzle_task.txt
```
- Solves constraint-based puzzles
- Shows logical deduction steps
- Validates solutions

### Understanding the Output

When you run a task, you'll see:
1. Task description in a green panel
2. Agent thinking process with progress indicators
3. Intermediate analysis steps from each agent
4. Final results in a formatted panel

### Creating Your Own Tasks

1. Create a new text file in `examples/tasks/` with the following structure:
```plaintext
[Task Description]
Describe the main task or problem to solve.

Constraints:
- List any constraints
- Add relevant limitations

Requirements:
- Specify what analysis is needed
- List expected outputs
```

2. Run your task:
```bash
python run_brain.py path/to/your/task.txt
```

## Project Structure

```
brain/
├── brain/              # Core implementation
│   ├── agents/         # Specialized AI agents
│   ├── tools/          # Analysis tools
│   └── crew.py         # Agent coordination
├── examples/
│   ├── tasks/          # Example cognitive tasks
│   └── test_flow.py    # Task processing script
├── run_brain.py        # CLI runner
├── requirements.txt
└── README.md
```

## Troubleshooting

1. If you see an error about missing OPENAI_API_KEY:
   - Ensure you've set the environment variable
   - Check that your API key is valid

2. If you see import errors:
   - Ensure you're in the virtual environment
   - Try reinstalling requirements:
     ```bash
     pip install -r requirements.txt --upgrade
     ```

3. For rich output formatting issues:
   - Ensure your terminal supports Unicode
   - Try updating rich:
     ```bash
     pip install rich --upgrade
     ```

## License

MIT License