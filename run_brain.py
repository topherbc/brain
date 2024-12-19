#!/usr/bin/env python3

import sys
import os
import logging
from brain.crew import CognitiveCrew
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Setup rich console for better output formatting
console = Console()

# Configure logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("brain")

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

def process_task_file(file_path: str) -> dict:
    """Process a task from a file with rich output formatting."""
    try:
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

        # Display results
        console.print("\n[bold green]Analysis Complete[/bold green]")
        console.print(Panel(str(results), title="[bold green]Results[/bold green]", 
                           border_style="green"))

        return results

    except FileNotFoundError:
        console.print(f"[bold red]Error: File '{file_path}' not found[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        console.print("[bold red]Usage: python run_brain.py <path_to_task_file>[/bold red]")
        sys.exit(1)

    task_file = sys.argv[1]
    process_task_file(task_file)

if __name__ == '__main__':
    main()