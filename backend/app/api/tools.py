"""
Tools API Routes
"""

from typing import List

from fastapi import APIRouter

from ..schemas.tool import Tool, ToolExecution, ToolResult

router = APIRouter()

# In-memory tool registry for MVP
tools_db: dict[str, Tool] = {
    "tool_web_search": Tool(
        id="tool_web_search",
        name="Web Search",
        description="Search the web for information",
        category="research",
        requires_approval=False,
    ),
    "tool_code_execute": Tool(
        id="tool_code_execute",
        name="Execute Code",
        description="Execute Python code",
        category="development",
        requires_approval=True,
    ),
    "tool_file_read": Tool(
        id="tool_file_read",
        name="Read File",
        description="Read file contents",
        category="filesystem",
        requires_approval=False,
    ),
    "tool_file_write": Tool(
        id="tool_file_write",
        name="Write File",
        description="Write file contents",
        category="filesystem",
        requires_approval=True,
    ),
}


@router.get("", response_model=List[Tool])
async def list_tools():
    """List available tools."""
    return list(tools_db.values())


@router.post("/{tool_id}/execute", response_model=ToolResult)
async def execute_tool(tool_id: str, execution: ToolExecution):
    """Execute a tool."""
    if tool_id not in tools_db:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Tool not found")

    tool = tools_db[tool_id]
    if tool.requires_approval:
        return ToolResult(
            success=False,
            output=None,
            error=f"Tool {tool_id} requires explicit approval and is not yet enabled",
        )

    # MVP: Return mock result
    return ToolResult(
        success=True,
        output={"message": f"Tool {tool_id} executed successfully"},
        error=None,
    )
