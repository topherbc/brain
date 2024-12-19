from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import json

class Task(BaseModel):
    description: str
    context: List[str] = Field(default_factory=list, description="List of context strings")
    priority: Optional[int] = Field(default=1, ge=1, le=5)
    status: str = Field(default="pending")

class AgentResponse(BaseModel):
    agent_name: str
    response: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class CognitiveCrew:
    def __init__(self):
        self.tasks: List[Task] = []
        self.context: List[str] = []
        self.memory: List[Dict[str, Any]] = []
        self.agent_responses: List[AgentResponse] = []

    def _format_output(self, data: Dict[str, Any]) -> str:
        """Format output for human readability"""
        output = ["\n=== Cognitive Analysis Report ==="]
        
        # Format Analysis Section
        output.append("\n🔍 Analysis:")
        for key, value in data['analysis'].items():
            output.append(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Format Context Section
        output.append("\n📚 Current Context:")
        for ctx in data['context']:
            output.append(f"  • {ctx}")
        
        # Format Actions Section
        output.append("\n⚡ Actions Taken:")
        for action in data['actions']:
            output.append(f"  • {action['type'].replace('_', ' ').title()}: Task #{action.get('task_id')}")
        
        # Format Agent Responses
        output.append("\n🤖 Agent Responses:")
        for response in self.agent_responses:
            output.append(f"  • {response.agent_name} ({response.timestamp.split('T')[0]}):\n    {response.response}")
        
        # Format Memory Updates
        output.append("\n💾 Memory Updates:")
        for update in data['memory_updates']:
            output.append(f"  • Input: {update['input']}\n    Analysis: {json.dumps(update['analysis'], indent=2)}")
        
        output.append("\n=== End Report ===\n")
        
        return '\n'.join(output)

    def process_input(self, input_data: Any) -> str:
        """Process input through cognitive pipeline with formatted output"""
        # Initialize response structure
        response = {
            'analysis': {},
            'context': [],
            'actions': [],
            'memory_updates': []
        }
        
        try:
            # Step 1: Executive Controller Analysis
            exec_response = self._executive_controller_analysis(input_data)
            self.agent_responses.append(AgentResponse(
                agent_name="Executive Controller",
                response=exec_response
            ))
            
            # Step 2: Initial Analysis
            analysis = self._analyze_input(input_data)
            response['analysis'] = analysis
            
            # Step 3: Specialist Analysis
            specialist_response = self._specialist_analysis(analysis)
            self.agent_responses.append(AgentResponse(
                agent_name="Specialist Analyzer",
                response=specialist_response
            ))
            
            # Step 4: Context Processing
            context_updates = self._extract_context(analysis)
            self.context.extend(context_updates)
            response['context'] = self.context.copy()
            
            # Step 5: Action Determination
            actions = self._determine_actions(analysis)
            response['actions'] = actions
            
            # Step 6: Memory Update
            memory_update = {
                'input': input_data,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat(),
            }
            self.memory.append(memory_update)
            response['memory_updates'] = [memory_update]
            
            # Step 7: Synthesizer Summary
            synth_response = self._synthesizer_summary(response)
            self.agent_responses.append(AgentResponse(
                agent_name="Information Synthesizer",
                response=synth_response
            ))
            
        except Exception as e:
            response['error'] = str(e)
        
        # Return formatted output
        return self._format_output(response)

    def _executive_controller_analysis(self, input_data: Any) -> str:
        """Executive Controller's initial assessment"""
        return f"Received input for processing: {input_data}. Initiating cognitive analysis pipeline."

    def _specialist_analysis(self, analysis: Dict[str, Any]) -> str:
        """Specialist's detailed analysis"""
        relevance = len(analysis.get('context_relevance', []))
        return f"Detailed analysis complete. Found {relevance} relevant context items. Content type: {analysis.get('type', 'unknown')}"

    def _synthesizer_summary(self, response: Dict[str, Any]) -> str:
        """Information Synthesizer's summary"""
        num_actions = len(response['actions'])
        num_context = len(response['context'])
        return f"Processing complete. Generated {num_actions} actions and updated {num_context} context items."

    def _analyze_input(self, input_data: Any) -> Dict[str, Any]:
        """Analyze input data considering current context"""
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
        new_context = []
        if isinstance(analysis.get('content'), str):
            content = analysis['content'].lower()
            key_indicators = ['priority', 'urgent', 'important', 'deadline', 'critical']
            new_context.extend([indicator for indicator in key_indicators if indicator in content])
        return new_context

    def _determine_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine required actions based on analysis"""
        actions = []
        
        if analysis.get('content'):
            task = Task(
                description=f"Process: {analysis['content'][:100]}",
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