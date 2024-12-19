from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3
import json

class MemoryDatabase:
    """A SQLite-based memory storage system for the brain project."""

    def __init__(self, db_path: str = ':memory:'):
        """Initialize the memory database.

        Args:
            db_path: Path to SQLite database file. Defaults to in-memory database.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        cursor = self.conn.cursor()
        
        # Create memories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            importance REAL DEFAULT 0.5
        )
        """)

        # Create tags table for memory categorization
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            memory_id INTEGER,
            tag TEXT,
            FOREIGN KEY(memory_id) REFERENCES memories(id),
            PRIMARY KEY(memory_id, tag)
        )
        """)

        self.conn.commit()

    def store(self, memory_type: str, content: Any, 
              tags: List[str] = None, metadata: Dict = None,
              importance: float = 0.5) -> int:
        """Store a new memory.

        Args:
            memory_type: Type of memory (e.g., 'observation', 'decision', 'fact')
            content: The actual memory content
            tags: Optional list of tags for categorization
            metadata: Optional additional structured data
            importance: Memory importance score (0-1)

        Returns:
            int: ID of the stored memory
        """
        cursor = self.conn.cursor()
        
        # Store the memory
        cursor.execute(
            "INSERT INTO memories (type, content, metadata, importance) VALUES (?, ?, ?, ?)",
            (memory_type, json.dumps(content), 
             json.dumps(metadata) if metadata else None,
             importance)
        )
        memory_id = cursor.lastrowid

        # Store tags if provided
        if tags:
            cursor.executemany(
                "INSERT INTO tags (memory_id, tag) VALUES (?, ?)",
                [(memory_id, tag) for tag in tags]
            )

        self.conn.commit()
        return memory_id

    def retrieve(self, query: Dict[str, Any] = None,
                limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve memories based on search criteria.

        Args:
            query: Search parameters (type, tags, time range, etc.)
            limit: Maximum number of memories to return

        Returns:
            List of matching memories with their metadata
        """
        cursor = self.conn.cursor()
        
        base_query = "SELECT DISTINCT m.* FROM memories m"
        params = []
        where_clauses = []

        if query:
            if 'type' in query:
                where_clauses.append("m.type = ?")
                params.append(query['type'])
            
            if 'tags' in query:
                base_query += " LEFT JOIN tags t ON m.id = t.memory_id"
                placeholders = ','.join(['?' for _ in query['tags']])
                where_clauses.append(f"t.tag IN ({placeholders})")
                params.extend(query['tags'])

            if 'min_importance' in query:
                where_clauses.append("m.importance >= ?")
                params.append(query['min_importance'])

        where_clause = " AND ".join(where_clauses)
        if where_clause:
            base_query += f" WHERE {where_clause}"

        base_query += " ORDER BY m.importance DESC, m.timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(base_query, params)
        rows = cursor.fetchall()

        # Format results
        memories = []
        for row in rows:
            memory = {
                'id': row[0],
                'timestamp': row[1],
                'type': row[2],
                'content': json.loads(row[3]),
                'metadata': json.loads(row[4]) if row[4] else None,
                'importance': row[5]
            }
            
            # Fetch associated tags
            cursor.execute("SELECT tag FROM tags WHERE memory_id = ?", (row[0],))
            memory['tags'] = [tag[0] for tag in cursor.fetchall()]
            
            memories.append(memory)

        return memories

    def update(self, memory_id: int, updates: Dict[str, Any]) -> bool:
        """Update an existing memory.

        Args:
            memory_id: ID of the memory to update
            updates: Dictionary of fields to update

        Returns:
            bool: Success status
        """
        cursor = self.conn.cursor()
        
        update_clauses = []
        params = []

        for field, value in updates.items():
            if field in ['type', 'content', 'metadata', 'importance']:
                update_clauses.append(f"{field} = ?")
                if field in ['content', 'metadata']:
                    params.append(json.dumps(value))
                else:
                    params.append(value)

        if not update_clauses:
            return False

        query = f"UPDATE memories SET {', '.join(update_clauses)} WHERE id = ?"
        params.append(memory_id)

        cursor.execute(query, params)
        self.conn.commit()

        return cursor.rowcount > 0

    def delete(self, memory_id: int) -> bool:
        """Delete a memory and its associated tags.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            bool: Success status
        """
        cursor = self.conn.cursor()
        
        # Delete tags first due to foreign key constraint
        cursor.execute("DELETE FROM tags WHERE memory_id = ?", (memory_id,))
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        
        self.conn.commit()
        return cursor.rowcount > 0

    def __del__(self):
        """Ensure database connection is closed on cleanup."""
        if hasattr(self, 'conn'):
            self.conn.close()
