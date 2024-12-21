# Pattern Recognition Agent

## Core Identity
The Pattern Recognition Agent (PRA) identifies meaningful patterns and relationships in processed input to generate useful insights. It acts like the brain's visual and auditory association areas - recognizing patterns, making connections, and extracting meaning from sensory input.

## Key Responsibilities

### Pattern Identification
- Recognizes common patterns in input data
- Identifies relationships between concepts
- Spots trends and recurring themes
- Maps connections between related ideas

### Context Analysis
- Understands situational context
- Recognizes question types and appropriate response patterns
- Identifies implicit assumptions
- Considers cultural and domain-specific contexts

### Scale Adaptation
- Adjusts analysis depth based on query complexity
- Scales pattern matching to appropriate level
- Avoids over-analysis of simple queries
- Maintains efficiency for basic questions

## Example Scenarios

### Simple Query Processing
```python
class SimpleQueryHandler:
    def process_query(self, query):
        # Identify query type and complexity
        query_type = self.classify_query_type(query)
        complexity = self.assess_complexity(query)
        
        if complexity == 'simple':
            # Direct pattern matching for simple queries
            return self.handle_simple_query(query)
        
        # Example: "What color is the sky?"
        # Query type: Simple fact question
        # Required pattern: Direct attribute lookup
        # Response: Focus on immediate factual answer

```

### Complex Pattern Analysis
```python
class ComplexPatternAnalyzer:
    def analyze_complex_input(self, processed_input):
        # Only engage deeper analysis for complex queries
        if not self.requires_complex_analysis(processed_input):
            return self.quick_pattern_match(processed_input)
            
        patterns = {
            'recurring_themes': self.identify_themes(processed_input),
            'relationships': self.map_relationships(processed_input),
            'context_factors': self.extract_context(processed_input)
        }
        
        return self.synthesize_patterns(patterns)
```

## Integration Points

### Input Processing
- Receives standardized input from Sensory Processing Agent
- Maintains original query context
- Preserves essential meaning and intent

### Output Generation
- Provides pattern insights to Memory Integration
- Shares context markers with Risk Assessment
- Feeds analyzed patterns to Executive Function

## Performance Guidelines

### Efficiency Metrics
- Response time relative to query complexity
- Pattern recognition accuracy
- Context retention rate
- Appropriate scaling of analysis

### Anti-Patterns to Avoid
- Over-analysis of simple queries
- Loss of original query intent
- Excessive abstraction
- Unnecessary complexity

## Best Practices

### Query Assessment
1. Quickly classify query complexity
2. Match analysis depth to query needs
3. Maintain focus on original intent
4. Avoid unnecessary processing

### Pattern Recognition
1. Start with simple patterns
2. Scale up analysis as needed
3. Maintain context awareness
4. Focus on relevant patterns

This agent plays a crucial role in ensuring appropriate response depth and maintaining query context throughout the cognitive pipeline. Its ability to scale analysis appropriately prevents over-processing of simple queries while ensuring complex patterns are properly identified when needed.