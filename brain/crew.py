from typing import List, Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    description: str
    context: List[str] = Field(default_factory=list, description="List of context strings")
    priority: Optional[int] = Field(default=1, ge=1, le=5)
    status: str = Field(default="pending")

class CognitiveCrew:
    def __init__(self):
        self.tasks: List[Task] = []
        self.context: List[str] = []

    def add_task(self, task: Task) -> None:
        """Add a new task to the crew's queue"""
        self.tasks.append(task)

    def get_next_task(self) -> Optional[Task]:
        """Get the highest priority pending task"""
        pending_tasks = [t for t in self.tasks if t.status == "pending"]
        if not pending_tasks:
            return None
        return max(pending_tasks, key=lambda x: x.priority)

    def update_task_status(self, task: Task, new_status: str) -> None:
        """Update the status of a task"""
        if task in self.tasks:
            task.status = new_status

    def add_context(self, context_item: str) -> None:
        """Add a new context item to the crew's context"""
        self.context.append(context_item)

    def get_context(self) -> List[str]:
        """Get the current context"""
        return self.context.copy()
