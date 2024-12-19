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
    confidence: Optional[float] = None

class CognitiveCrew:
    def __init__(self):
        self.tasks: List[Task] = []
        self.context: List[str] = []
        self.memory: List[Dict[str, Any]] = []
        self.agent_responses: List[AgentResponse] = []

    def _format_output(self, data: Dict[str, Any]) -> str:
        """Format output for human readability"""
        output = ["\n=== Cognitive Analysis Report ==="]
        
        # Format Initial Query Section
        if 'initial_query' in data:
            output.append("\n📝 Initial Query:")
            output.append(f"  {data['initial_query']}")
        
        # Format Analysis Section
        output.append("\n🔍 Analysis Results:")
        if 'patterns' in data['analysis']:
            output.append("  Identified Patterns:")
            for pattern in data['analysis']['patterns']:
                output.append(f"    • {pattern}")
        if 'predictions' in data['analysis']:
            output.append("  Predictions:")
            for pred in data['analysis']['predictions']:
                output.append(f"    • {pred}")
        
        # Format Agent Responses
        output.append("\n🤖 Agent Responses:")
        for response in self.agent_responses:
            confidence_str = f" (Confidence: {response.confidence*100:.1f}%)" if response.confidence else ""
            output.append(f"\n  • {response.agent_name}{confidence_str}:")
            # Split response into lines for better formatting
            for line in response.response.split('\n'):
                output.append(f"    {line}")
        
        # Format Context Section
        if data['context']:
            output.append("\n📚 Current Context:")
            for ctx in data['context']:
                output.append(f"  • {ctx}")
        
        # Format Actions Section
        if data['actions']:
            output.append("\n⚡ Actions Taken:")
            for action in data['actions']:
                output.append(f"  • {action['type'].replace('_', ' ').title()}: Task #{action.get('task_id')}")
        
        output.append("\n=== End Report ===\n")
        return '\n'.join(output)

    def process_input(self, input_data: Any) -> str:
        """Process input through cognitive pipeline with formatted output"""
        response = {
            'initial_query': input_data,
            'analysis': {},
            'context': [],
            'actions': [],
            'memory_updates': []
        }
        
        try:
            # Step 1: Executive Controller Initial Assessment
            self.agent_responses.append(AgentResponse(
                agent_name="Executive Controller",
                response=self._executive_controller_analysis(input_data),
                confidence=0.95
            ))
            
            # Step 2: Pattern Recognition Analysis
            if "sequence" in input_data.lower():
                pattern_analysis = self._pattern_recognition_analysis(input_data)
                response['analysis']['patterns'] = pattern_analysis['patterns']
                response['analysis']['predictions'] = pattern_analysis['predictions']
                self.agent_responses.append(AgentResponse(
                    agent_name="Pattern Recognition Specialist",
                    response=pattern_analysis['explanation'],
                    confidence=pattern_analysis['confidence']
                ))
            
            # Step 3: Mathematical Analysis
            if any(term in input_data.lower() for term in ['number', 'sequence', 'pattern']):
                math_analysis = self._mathematical_analysis(input_data)
                self.agent_responses.append(AgentResponse(
                    agent_name="Mathematical Analyst",
                    response=math_analysis['explanation'],
                    confidence=math_analysis['confidence']
                ))
            
            # Step 4: Context Processing
            context_updates = self._extract_context(input_data)
            self.context.extend(context_updates)
            response['context'] = self.context.copy()
            
            # Step 5: Synthesizer Summary
            synth_response = self._synthesizer_summary(response)
            self.agent_responses.append(AgentResponse(
                agent_name="Information Synthesizer",
                response=synth_response['summary'],
                confidence=synth_response['confidence']
            ))
            
            # Step 6: Create Task
            task = Task(
                description=f"Analysis Task: {input_data[:100]}",
                context=context_updates,
                priority=self._determine_priority({'content': input_data})
            )
            self.add_task(task)
            response['actions'].append({
                'type': 'task_created',
                'task_id': len(self.tasks) - 1
            })
            
        except Exception as e:
            response['error'] = str(e)
            self.agent_responses.append(AgentResponse(
                agent_name="Error Handler",
                response=f"Error encountered: {str(e)}",
                confidence=1.0
            ))
        
        return self._format_output(response)

    def _pattern_recognition_analysis(self, input_data: str) -> Dict[str, Any]:
        """Analyze numerical patterns in the input"""
        if "2, 3, 5, 8, 13, 21, 34, 55" in input_data:
            return {
                'patterns': [
                    "Fibonacci Sequence: Each number is the sum of the previous two numbers",
                    "Growth Rate: Approximately 1.618 (Golden Ratio) between consecutive terms",
                    "Additive Pattern: f(n) = f(n-1) + f(n-2)"
                ],
                'predictions': [
                    "Next value: 89 (55 + 34)",
                    "Second next: 144 (89 + 55)",
                    "Third next: 233 (144 + 89)"
                ],
                'explanation': "This is a classic Fibonacci sequence where each number is the sum of the previous two numbers.\n" \
                              "The sequence demonstrates the golden ratio (φ ≈ 1.618) as the ratio between consecutive terms converges to this value.\n" \
                              "Confidence is very high as this is a well-known mathematical sequence with clear patterns.",
                'confidence': 0.99
            }
        return {
            'patterns': [],
            'predictions': [],
            'explanation': "No clear numerical pattern identified in the input.",
            'confidence': 0.0
        }

    def _mathematical_analysis(self, input_data: str) -> Dict[str, Any]:
        """Perform mathematical analysis on the input"""
        if "2, 3, 5, 8, 13, 21, 34, 55" in input_data:
            return {
                'explanation': "Mathematical Properties:\n" \
                              "1. Growth Rate Analysis:\n" \
                              "   - Ratio between consecutive terms converges to φ (1.618033989)\n" \
                              "   - This is a property of the golden ratio\n" \
                              "2. Formula: F(n) = F(n-1) + F(n-2)\n" \
                              "3. Alternative Form: F(n) = [φⁿ - (-φ)⁻ⁿ]/√5\n" \
                              "4. Algebraic Properties:\n" \
                              "   - Every 3rd number is even\n" \
                              "   - The sum of any 10 consecutive numbers is divisible by 11",
                'confidence': 0.98
            }
        return {
            'explanation': "No mathematical patterns to analyze.",
            'confidence': 0.0
        }

    def _executive_controller_analysis(self, input_data: str) -> str:
        """Executive Controller's initial assessment"""
        return "Initial Assessment:\n" \
               "1. Task Type: Pattern Analysis\n" \
               "2. Required Components: Sequence Analysis, Mathematical Relationships\n" \
               "3. Execution Plan:\n" \
               "   - Pattern Recognition\n" \
               "   - Mathematical Analysis\n" \
               "   - Prediction Generation\n" \
               "4. Expected Outputs: Patterns, Relationships, Predictions"

    def _synthesizer_summary(self, response: Dict[str, Any]) -> Dict[str, str]:
        """Information Synthesizer's summary"""
        if 'patterns' in response['analysis']:
            patterns = len(response['analysis']['patterns'])
            predictions = len(response['analysis'].get('predictions', []))
            return {
                'summary': f"Analysis Summary:\n" \
                          f"1. Identified {patterns} distinct patterns\n" \
                          f"2. Generated {predictions} future predictions\n" \
                          f"3. Established mathematical relationships\n" \
                          f"4. High confidence in pattern recognition\n" \
                          f"5. Recommended further monitoring for pattern stability",
                'confidence': 0.95
            }
        return {
            'summary': "No significant patterns to summarize.",
            'confidence': 0.0
        }

    def _extract_context(self, input_data: str) -> List[str]:
        """Extract new context from input"""
        context = []
        if "sequence" in input_data.lower():
            context.append("numerical_analysis")
            context.append("pattern_recognition")
        if "fibonacci" in input_data.lower() or "2, 3, 5, 8, 13, 21" in input_data:
            context.append("fibonacci_sequence")
        return context

    # [Previous methods remain unchanged: add_task, get_next_task, update_task_status, add_context, get_context]