#!/usr/bin/env python3

import sys
import os
import logging
from brain.crew import CognitiveCrew
from brain.agents.memory import MemorySystem
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

# Setup rich console for better output formatting
console = Console()

# Configure logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("brain")

def setup_environment():
    """Setup necessary environment and directories"""
    try:
        # Ensure config directory exists
        os.makedirs('brain/config', exist_ok=True)
        os.makedirs('examples/tasks', exist_ok=True)
        os.makedirs('brain/data', exist_ok=True)

        # Initialize memory system
        memory = MemorySystem()
        return memory
    except Exception as e:
        console.print(f"[bold red]Error setting up environment: {str(e)}[/bold red]")
        sys.exit(1)

def display_agent_header(agent_name: str):
    """Display a formatted header for agent outputs"""
    console.print(f"\n[bold blue]{'='*20} {agent_name} {'='*20}[/bold blue]")

def display_thinking_process(message: str):
    """Display agent thinking process with animation"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)

def get_example_tasks():
    """Get list of available example tasks"""
    tasks_dir = Path('examples/tasks')
    if not tasks_dir.exists():
        return []
    return [f.name for f in tasks_dir.glob('*.txt')]

def process_task_file(file_path: str, memory: MemorySystem) -> dict:
    """Process a task from a file with rich output formatting."""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            available_tasks = get_example_tasks()
            if available_tasks:
                console.print("[yellow]Available example tasks:[/yellow]")
                for task in available_tasks:
                    console.print(f"  - {task}")
            raise FileNotFoundError(f"File '{file_path}' not found")

        # Read task file
        with open(file_path, 'r') as f:
            task_content = f.read()

        # Display task content
        console.print(Panel(task_content, title="[bold green]Task Input[/bold green]", 
                           border_style="green"))

        # Initialize cognitive crew
        crew = CognitiveCrew()

        console.print("\n[bold yellow]Initiating Cognitive Analysis[/bold yellow]")

        # Process the task
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Processing...", total=None)
            results = crew.process_input(task_content)

        # Store results in memory
        memory.store(
            content=results,
            context={"task_file": file_path, "type": "task_result"}
        )

        # Display results
        console.print("\n[bold green]Analysis Complete[/bold green]")
        console.print(Panel(str(results), title="[bold green]Results[/bold green]", 
                           border_style="green"))

        return results

    except FileNotFoundError as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        console.print_exception()
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        console.print("[bold yellow]Usage: python run_brain.py <path_to_task_file>[/bold yellow]")
        console.print("\n[bold cyan]Example tasks available in examples/tasks/:[/bold cyan]")
        for task in get_example_tasks():
            console.print(f"  - {task}")
        sys.exit(1)

    # Setup environment and memory system
    memory = setup_environment()

    # Process the task
    task_file = sys.argv[1]
    process_task_file(task_file, memory)

if __name__ == '__main__':
    main()