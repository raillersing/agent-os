"""OpenAI Responses API adapter.

This module is the only D2 location that imports the OpenAI SDK.  It exposes
only provider-neutral dataclasses to the rest of Agent OS and never enables
OpenAI built-in tools for the first real-provider slice.
"""

import json
import time
from typing import Any

from openai import AsyncOpenAI

from ..config import settings
from .contracts import (
    ModelInvocationRequest,
    ModelInvocationResult,
    ModelProviderError,
    UsageObservation,
)

ADAPTER_ID = "openai.responses"
ADAPTER_VERSION = "1"


def _error_code(error: Any) -> str | None:
    """Extract a stable provider error code without exposing SDK objects."""
    direct = getattr(error, "code", None)
    if isinstance(direct, str):
        return direct
    body = getattr(error, "body", None)
    if isinstance(body, dict):
        nested = body.get("error", body)
        if isinstance(nested, dict) and isinstance(nested.get("code"), str):
            return nested["code"]
    return None


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _usage(response: Any) -> UsageObservation:
    usage = _value(response, "usage")
    if usage is None:
        return UsageObservation()
    input_tokens = _value(usage, "input_tokens")
    output_tokens = _value(usage, "output_tokens")
    total_tokens = _value(usage, "total_tokens")
    details = _value(usage, "input_tokens_details", {}) or {}
    cached = _value(details, "cached_tokens")
    values = [input_tokens, output_tokens, total_tokens]
    completeness = (
        "complete" if all(value is not None for value in values) else "partial"
    )
    return UsageObservation(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cached_input_tokens=cached,
        source="provider_reported",
        completeness=completeness,
        raw={
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cached_input_tokens": cached,
        },
    )


class OpenAIResponsesAdapter:
    """Bounded text-only OpenAI Responses invocation."""

    provider_id = "openai"

    def __init__(self, client: Any | None = None):
        if client is not None:
            self.client = client
        elif settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=settings.OPENAI_TIMEOUT_SECONDS,
                max_retries=0,
            )
        else:
            self.client = None

    async def invoke(self, request: ModelInvocationRequest) -> ModelInvocationResult:
        if not settings.OPENAI_EXECUTION_ENABLED:
            raise ModelProviderError(
                "MODEL_EXECUTION_DISABLED",
                "OpenAI execution is disabled until explicitly enabled",
                retryable=False,
            )
        if self.client is None:
            raise ModelProviderError(
                "MODEL_AUTHENTICATION_FAILED",
                "OpenAI is not configured; no provider fallback is permitted",
                retryable=False,
            )
        started = time.monotonic()
        input_items = [
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": request.system_instructions}
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": request.input_text}],
            },
        ]
        kwargs: dict[str, Any] = {
            "model": request.configured_model,
            "input": input_items,
            "tools": [],
            "store": False,
            "max_output_tokens": request.max_output_tokens,
            "extra_headers": {"X-Client-Request-Id": request.request_id},
        }
        if request.output_schema is not None:
            kwargs["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "agent_os_result",
                    "strict": True,
                    "schema": dict(request.output_schema),
                }
            }
        try:
            response = await self.client.responses.create(**kwargs)
        except Exception as error:  # SDK-specific errors stay behind this boundary.
            status = getattr(error, "status_code", None)
            is_timeout = isinstance(error, TimeoutError)
            provider_code = _error_code(error)
            if is_timeout:
                code = "MODEL_TIMEOUT"
            elif status == 429:
                code = (
                    "MODEL_PROVIDER_QUOTA_EXHAUSTED"
                    if provider_code == "insufficient_quota"
                    else "MODEL_RATE_LIMITED"
                )
            else:
                code = "MODEL_PROVIDER_ERROR"
            retryable = (
                False
                if code == "MODEL_PROVIDER_QUOTA_EXHAUSTED"
                else is_timeout or status == 429 or status is None or status >= 500
            )
            raise ModelProviderError(
                code, "OpenAI request failed", retryable=retryable
            ) from error
        output_text = _value(response, "output_text", "") or ""
        structured = None
        if request.output_schema is not None:
            try:
                structured = json.loads(output_text)
            except (TypeError, ValueError) as error:
                raise ModelProviderError(
                    "MODEL_RESPONSE_INVALID",
                    "OpenAI structured output was not valid JSON",
                    retryable=False,
                ) from error
            if (
                not isinstance(structured, dict)
                or not isinstance(structured.get("answer"), str)
                or not isinstance(structured.get("uncertainty"), str)
                or set(structured) != {"answer", "uncertainty"}
            ):
                raise ModelProviderError(
                    "MODEL_RESPONSE_INVALID",
                    "OpenAI structured output failed Agent OS schema validation",
                    retryable=False,
                )
        actual_model = _value(response, "model")
        reported_provider = _value(response, "provider")
        actual_provider = reported_provider or (
            self.provider_id if actual_model else None
        )
        identity_state = "provider_reported" if actual_model else "unavailable"
        if reported_provider and reported_provider != self.provider_id:
            identity_state = "unexpected"
        request_id = _value(response, "_request_id") or _value(response, "request_id")
        return ModelInvocationResult(
            output_text=output_text,
            structured_result=structured,
            adapter_id=ADAPTER_ID,
            adapter_version=ADAPTER_VERSION,
            configured_provider=self.provider_id,
            configured_model=request.configured_model,
            actual_provider=actual_provider,
            actual_model=actual_model,
            identity_state=identity_state,
            provider_request_id=request_id,
            response_id=_value(response, "id"),
            usage=_usage(response),
            stop_reason=_value(_value(response, "status", None), "value", None)
            or _value(response, "status", "unknown"),
            refusal_state="unknown",
            latency_ms=int((time.monotonic() - started) * 1000),
        )
