"""
Base Agent Class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(
        self,
        name: str,
        model: str,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.model = model
        self.capabilities = capabilities or []
        self.config = config or {}
        self.status = "idle"
        self.created_at = datetime.utcnow()
        self.last_run_at = None

    @abstractmethod
    async def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a run with the given prompt."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the current run."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "status": self.status,
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat(),
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
        }

    def update_config(self, config: Dict[str, Any]) -> None:
        """Update agent configuration."""
        self.config.update(config)
