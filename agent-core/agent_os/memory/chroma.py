"""
ChromaDB Memory Implementation
"""

from typing import Any, Dict, List, Optional
import chromadb
from chromadb.config import Settings


class ChromaMemory:
    """Memory system using ChromaDB for vector storage."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False,
        ))
        self.collection = self.client.get_or_create_collection(
            name="agent_memory",
            metadata={"hnsw:space": "cosine"}
        )

    def add(
        self,
        key: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add memory entry."""
        self.collection.upsert(
            ids=[key],
            documents=[content],
            metadatas=[metadata or {}],
        )
        return key

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get memory entry by key."""
        result = self.collection.get(ids=[key])
        if result["ids"]:
            return {
                "key": result["ids"][0],
                "content": result["documents"][0],
                "metadata": result["metadatas"][0] if result["metadatas"] else {},
            }
        return None

    def search(
        self,
        query: str,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search memory by semantic similarity."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
        )
        memories = []
        for i in range(len(results["ids"][0])):
            memories.append({
                "key": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
        return memories

    def delete(self, key: str) -> bool:
        """Delete memory entry."""
        try:
            self.collection.delete(ids=[key])
            return True
        except Exception:
            return False

    def count(self) -> int:
        """Get total number of memory entries."""
        return self.collection.count()

    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all memory entries."""
        results = self.collection.get(limit=limit)
        memories = []
        for i in range(len(results["ids"])):
            memories.append({
                "key": results["ids"][i],
                "content": results["documents"][i],
                "metadata": results["metadatas"][i] if results["metadatas"] else {},
            })
        return memories
