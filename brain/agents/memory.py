from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import sqlite3
import json
import os

class MemorySystem:
    def __init__(self, db_path: str = 'brain/data/memory.db'):
        self.db_path = db_path
        self._ensure_db_dir()
        self._initialize_db()
        self.working_memory: Dict[str, Any] = {}
        self.working_memory_limit = 100

    def _ensure_db_dir(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _initialize_db(self):
        """Initialize the SQLite database with necessary tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create memories table for long-term storage
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    context TEXT,
                    timestamp TEXT NOT NULL,
                    importance REAL DEFAULT 0.5,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            """)
            
            # Create context table for efficient context-based retrieval
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS context_index (
                    memory_id INTEGER,
                    context_key TEXT,
                    context_value TEXT,
                    FOREIGN KEY(memory_id) REFERENCES memories(id),
                    PRIMARY KEY(memory_id, context_key)
                )
            """)
            
            # Create associations table for related memories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS associations (
                    source_id INTEGER,
                    target_id INTEGER,
                    strength REAL DEFAULT 0.5,
                    FOREIGN KEY(source_id) REFERENCES memories(id),
                    FOREIGN KEY(target_id) REFERENCES memories(id),
                    PRIMARY KEY(source_id, target_id)
                )
            """)
            
            conn.commit()

    def store(self, content: Any, context: Optional[Dict[str, str]] = None) -> int:
        """Store new information in long-term memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convert content to JSON if it's not a string
            if not isinstance(content, str):
                content = json.dumps(content)
            
            # Store the main memory entry
            cursor.execute("""
                INSERT INTO memories (content, context, timestamp)
                VALUES (?, ?, ?)
            """, (content, json.dumps(context or {}), datetime.now().isoformat()))
            
            memory_id = cursor.lastrowid
            
            # Index context for efficient retrieval
            if context:
                for key, value in context.items():
                    cursor.execute("""
                        INSERT INTO context_index (memory_id, context_key, context_value)
                        VALUES (?, ?, ?)
                    """, (memory_id, key, value))
            
            conn.commit()
            return memory_id

    def retrieve_by_context(self, context: Dict[str, str], limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve memories based on context"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build query based on context keys
            query = """
                SELECT DISTINCT m.* FROM memories m
                JOIN context_index ci ON m.id = ci.memory_id
                WHERE
            """
            conditions = []
            params = []
            
            for key, value in context.items():
                conditions.append("(ci.context_key = ? AND ci.context_value = ?)")
                params.extend([key, value])
            
            query += " OR ".join(conditions)
            query += " ORDER BY m.importance DESC, m.access_count DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            memories = cursor.fetchall()
            
            # Update access statistics
            for memory in memories:
                cursor.execute("""
                    UPDATE memories
                    SET access_count = access_count + 1,
                        last_accessed = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), memory[0]))
            
            conn.commit()
            
            return [{
                'id': m[0],
                'content': json.loads(m[1]) if self._is_json(m[1]) else m[1],
                'context': json.loads(m[2]),
                'timestamp': m[3],
                'importance': m[4],
                'access_count': m[5],
                'last_accessed': m[6]
            } for m in memories]

    def update_working_memory(self, key: str, value: Any):
        """Update working memory with new information"""
        self.working_memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
        # Prune working memory if it exceeds limit
        if len(self.working_memory) > self.working_memory_limit:
            self._prune_working_memory()

    def get_from_working_memory(self, key: str) -> Optional[Any]:
        """Retrieve information from working memory"""
        if key in self.working_memory:
            return self.working_memory[key]['value']
        return None

    def _prune_working_memory(self):
        """Remove oldest items from working memory"""
        # Sort by timestamp and keep only the most recent items
        sorted_items = sorted(
            self.working_memory.items(),
            key=lambda x: x[1]['timestamp'],
            reverse=True
        )
        
        # Keep only the most recent items within the limit
        self.working_memory = dict(sorted_items[:self.working_memory_limit])

    def create_association(self, source_id: int, target_id: int, strength: float = 0.5):
        """Create an association between two memories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO associations (source_id, target_id, strength)
                VALUES (?, ?, ?)
            """, (source_id, target_id, strength))
            conn.commit()

    def get_associated_memories(self, memory_id: int, min_strength: float = 0.3) -> List[Dict[str, Any]]:
        """Retrieve memories associated with a given memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, a.strength
                FROM memories m
                JOIN associations a ON m.id = a.target_id
                WHERE a.source_id = ? AND a.strength >= ?
                ORDER BY a.strength DESC
            """, (memory_id, min_strength))
            
            return [{
                'id': m[0],
                'content': json.loads(m[1]) if self._is_json(m[1]) else m[1],
                'context': json.loads(m[2]),
                'timestamp': m[3],
                'importance': m[4],
                'access_count': m[5],
                'last_accessed': m[6],
                'association_strength': m[7]
            } for m in cursor.fetchall()]

    @staticmethod
    def _is_json(string: str) -> bool:
        """Check if a string is JSON formatted"""
        try:
            json.loads(string)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def cleanup(self, min_importance: float = 0.2, min_access_count: int = 5):
        """Remove low-importance, rarely accessed memories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Find memories to remove
            cursor.execute("""
                SELECT id FROM memories
                WHERE importance < ? AND access_count < ?
            """, (min_importance, min_access_count))
            
            memories_to_remove = [row[0] for row in cursor.fetchall()]
            
            # Remove associated data
            for memory_id in memories_to_remove:
                cursor.execute("DELETE FROM context_index WHERE memory_id = ?", (memory_id,))
                cursor.execute("DELETE FROM associations WHERE source_id = ? OR target_id = ?", 
                              (memory_id, memory_id))
                cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            
            conn.commit()
            
            return len(memories_to_remove)
