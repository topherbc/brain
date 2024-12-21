from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class MemoryEntry(BaseModel):
    """Individual memory entry in the store."""
    id: str = Field(description="Unique identifier for the memory")
    content: Any = Field(description="Memory content")
    type: str = Field(description="Type of memory (short_term, long_term)")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True

class MemoryStore(BaseModel):
    """Manages short-term and long-term memory storage."""
    short_term_capacity: int = Field(default=100, description="Max short-term memories")
    long_term_threshold: float = Field(
        default=0.7, 
        description="Confidence threshold for long-term storage"
    )
    
    _short_term: List[MemoryEntry] = []
    _long_term: Dict[str, MemoryEntry] = {}
    
    async def store(
        self, 
        content: Any, 
        memory_type: str = "short_term", 
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        entry = MemoryEntry(
            id=self._generate_id(),
            content=content,
            type=memory_type,
            metadata=metadata or {}
        )
        
        if memory_type == "short_term":
            if len(self._short_term) >= self.short_term_capacity:
                self._short_term.pop(0)  # Remove oldest
            self._short_term.append(entry)
        else:
            self._long_term[entry.id] = entry
            
        return entry.id
    
    async def retrieve(
        self, 
        memory_id: Optional[str] = None, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Union[MemoryEntry, List[MemoryEntry], None]:
        if memory_id:
            return (
                next((m for m in self._short_term if m.id == memory_id), None) or
                self._long_term.get(memory_id)
            )
        
        results = []
        for memory in self._short_term + list(self._long_term.values()):
            if self._matches_filters(memory, filters):
                results.append(memory)
                
        return results
    
    def _generate_id(self) -> str:
        from uuid import uuid4
        return str(uuid4())
    
    def _matches_filters(
        self, 
        memory: MemoryEntry, 
        filters: Optional[Dict[str, Any]]
    ) -> bool:
        if not filters:
            return True
            
        return all(
            memory.metadata.get(k) == v 
            for k, v in filters.items()
        )