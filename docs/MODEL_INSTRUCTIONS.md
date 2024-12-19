# Model Instructions: Brain-Inspired Cognitive System

## System Overview
You are part of a brain-inspired cognitive system implementing multiple specialized agents for information processing and decision making. The system is designed to mimic human cognitive processes, with each agent handling specific aspects of cognition.

## Current State
- Repository: https://github.com/topherbc/brain
- Main branch contains complete project structure
- Implementation uses CrewAI for agent management
- Memory system implemented with SQLite backend

## Knowledge Graph Access
To understand the current state:
```python
# Read current graph state
read_graph()

# Search for specific components
search_nodes("cognitive_agents")  # For agent information
search_nodes("memory_system")    # For memory system details
search_nodes("implementation_status")  # For current state
```

## Key Components

### Cognitive Agents
1. Perception Processor
   - Initial information processing
   - Pattern identification
   - Input structuring

2. Working Memory Manager
   - Active information maintenance
   - Temporary storage
   - Data manipulation

3. Pattern Analysis Specialist
   - Complex pattern recognition
   - Relationship identification
   - Abstract feature processing

4. Attention Controller
   - Information filtering
   - Priority management
   - Focus direction

5. Logical Reasoning Processor
   - Problem-solving
   - Logical analysis
   - Solution generation

6. Knowledge Integration Agent
   - Information connection
   - Knowledge synthesis
   - Learning integration

7. Decision Synthesis Agent
   - Final decision making
   - Response generation
   - Process integration

### Memory System
- Location: brain/agents/memory.py
- Features:
  - Working memory (temporary storage)
  - Long-term storage (SQLite)
  - Context-based retrieval
  - Association tracking
  - Automatic cleanup

## Configuration
- Agent configurations: brain/config/agents.yaml
- Task configurations: brain/config/tasks.yaml
- Example tasks: examples/tasks/

## Processing Pipeline
1. Input received through process_input()
2. Perception processing
3. Working memory update
4. Pattern analysis
5. Attention filtering
6. Logical reasoning
7. Knowledge integration
8. Decision synthesis

## Memory Usage
```python
# Store new information
memory_system.store(
    content=data,
    context={"type": "task_result"}
)

# Retrieve by context
memory_system.retrieve_by_context(
    context={"type": "task_result"}
)

# Update working memory
memory_system.update_working_memory(
    key="current_task",
    value=task_data
)
```

## Task Processing
1. Tasks are defined in YAML configuration
2. Sequential processing through agents
3. Results stored in memory system
4. Output formatted for human readability

## Example Usage
```python
from brain.crew import CognitiveCrew
from brain.agents.memory import MemorySystem

# Initialize systems
memory = MemorySystem()
crew = CognitiveCrew()

# Process a task
result = crew.process_input("Analyze the pattern: 2, 3, 5, 8, 13")

# Store result in memory
memory.store(result, context={"type": "pattern_analysis"})
```

## Important Considerations
1. Always check the knowledge graph for current state
2. Use memory system for persistent storage
3. Follow the sequential processing pipeline
4. Maintain context throughout processing
5. Store results for future reference

## Future Development Areas
1. Enhanced pattern recognition capabilities
2. Improved memory association mechanisms
3. Advanced cognitive task handling
4. Integration with external knowledge sources