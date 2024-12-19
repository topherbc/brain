from brain.crew import CognitiveCrew
import logging

# Configure logging to show agent decision flow
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def process_task_file(file_path: str) -> dict:
    """Process a task from a file and return the results.

    Args:
        file_path: Path to the task file

    Returns:
        dict: Processing results including all agent decisions and final outcome
    """
    # Read task file
    with open(file_path, 'r') as f:
        task_content = f.read()

    # Initialize cognitive crew with verbose output
    crew = CognitiveCrew(verbose=True)

    # Process the task
    results = crew.process_input(task_content)

    return results

def main():
    # Process example tasks
    task_files = [
        'examples/tasks/task1.txt',
        'examples/tasks/task2.txt'
    ]

    for task_file in task_files:
        print(f"\nProcessing task from {task_file}\n{'='*50}")
        results = process_task_file(task_file)
        print(f"\nResults:\n{'-'*20}")
        print(results)

if __name__ == '__main__':
    main()