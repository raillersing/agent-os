"""
Tool Schemas
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class Tool(BaseModel):
    """Tool schema."""

    id: str
    name: str
    description: str
    category: str
    requires_approval: bool = False


class ToolExecution(BaseModel):
    """Tool execution request."""

    parameters: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = None


class ToolResult(BaseModel):
    """Tool execution result."""

    success: bool
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
