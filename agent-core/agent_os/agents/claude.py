"""
Claude Agent Implementation
"""

from typing import Any, Dict, List, Optional
import anthropic

from .base import BaseAgent


class ClaudeAgent(BaseAgent):
    """Agent powered by Claude API."""

    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            name=name,
            model="claude-3-5-sonnet-20241022",
            capabilities=capabilities or ["text-generation", "analysis", "coding"],
            config=config or {},
        )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []

    async def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a run with Claude."""
        self.status = "running"
        self.last_run_at = datetime.utcnow()

        try:
            # Build messages
            messages = [{"role": "user", "content": prompt}]

            # Add context if provided
            if context:
                system_prompt = self._build_system_prompt(context)
            else:
                system_prompt = "You are a helpful AI assistant."

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.config.get("max_tokens", 4096),
                temperature=self.config.get("temperature", 0.7),
                system=system_prompt,
                messages=messages,
            )

            # Extract response
            result = {
                "response": response.content[0].text,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "model": self.model,
                "stop_reason": response.stop_reason,
            }

            self.status = "idle"
            return result

        except Exception as e:
            self.status = "error"
            raise e

    async def stop(self) -> None:
        """Stop the current run."""
        self.status = "idle"

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt from context."""
        parts = ["You are a helpful AI assistant."]

        if "memory" in context:
            parts.append(f"\nMemory context:\n{context['memory']}")

        if "tools" in context:
            parts.append(f"\nAvailable tools:\n{context['tools']}")

        return "\n".join(parts)

    def add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
