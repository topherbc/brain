from typing import List, Optional, Any, Dict
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
        self.memory: List[Dict[str, Any]] = []

    def process_input(self, input_data: Any) -> Dict[str, Any]:
        """Process input through cognitive pipeline
        
        Args:
            input_data: Input data to be processed
            
        Returns:
            Dict containing processed results including:
            - analysis: Initial analysis results
            - context: Updated context
            - actions: Recommended actions
            - memory_updates: Any updates to memory
        """
        # Initialize response structure
        response = {
            'analysis': {},
            'context': [],
            'actions': [],
            'memory_updates': []
        }
        
        # Step 1: Initial Analysis
        try:
            # Analyze input and context
            analysis = self._analyze_input(input_data)
            response['analysis'] = analysis
            
            # Update context based on analysis
            context_updates = self._extract_context(analysis)
            self.context.extend(context_updates)
            response['context'] = self.context.copy()
            
            # Determine required actions
            actions = self._determine_actions(analysis)
            response['actions'] = actions
            
            # Update memory
            memory_update = {
                'input': input_data,
                'analysis': analysis,
                'timestamp': 'current_timestamp',  # TODO: Implement proper timestamp
            }
            self.memory.append(memory_update)
            response['memory_updates'] = [memory_update]
            
        except Exception as e:
            response['error'] = str(e)
            
        return response

    def _analyze_input(self, input_data: Any) -> Dict[str, Any]:
        """Analyze input data considering current context"""
        # TODO: Implement more sophisticated analysis
        return {
            'type': str(type(input_data)),
            'content': str(input_data),
            'context_relevance': self._check_context_relevance(input_data)
        }

    def _check_context_relevance(self, input_data: Any) -> List[str]:
        """Check input relevance against current context"""
        relevant_context = []
        for ctx in self.context:
            if str(ctx).lower() in str(input_data).lower():
                relevant_context.append(ctx)
        return relevant_context

    def _extract_context(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract new context from analysis results"""
        # TODO: Implement more sophisticated context extraction
        new_context = []
        if isinstance(analysis.get('content'), str):
            # Simple example: extract key phrases
            content = analysis['content'].lower()
            key_indicators = ['priority', 'urgent', 'important', 'deadline', 'critical']
            new_context.extend([indicator for indicator in key_indicators if indicator in content])
        return new_context

    def _determine_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine required actions based on analysis"""
        actions = []
        
        # Create tasks based on analysis
        if analysis.get('content'):
            task = Task(
                description=f"Process: {analysis['content'][:100]}",  # First 100 chars
                context=analysis.get('context_relevance', []),
                priority=self._determine_priority(analysis)
            )
            self.add_task(task)
            actions.append({
                'type': 'task_created',
                'task_id': len(self.tasks) - 1
            })
            
        return actions

    def _determine_priority(self, analysis: Dict[str, Any]) -> int:
        """Determine priority level based on analysis"""
        # TODO: Implement more sophisticated priority determination
        content = analysis.get('content', '').lower()
        if 'urgent' in content or 'critical' in content:
            return 5
        elif 'important' in content:
            return 4
        elif 'soon' in content:
            return 3
        elif 'when possible' in content:
            return 2
        return 1

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
