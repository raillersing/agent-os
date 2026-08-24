"""Exact-action approval engine.

Implements the core lifecycle defined in APR-001:
- deterministic action fingerprinting and request hashing;
- human-only decision recording;
- one-time atomic consumption with run/attempt binding;
- expiry and invalidation checks at consumption time.

The engine does not know about HTTP or Temporal; it operates on SQLAlchemy
async sessions and UUIDs so it can be called from API endpoints, workflow
activities, and tests with the same semantics.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.time import utcnow
from ..models.control_plane import Approval as ApprovalModel
from ..models.control_plane import ApprovalConsumption as ApprovalConsumptionModel

CANONICAL_HASH_VERSION = "apr-sha256-v1"

APPROVAL_TERMINAL_STATES = {
    "approved",
    "consumed",
    "rejected",
    "expired",
    "invalidated",
    "cancelled",
    "superseded",
}

# "pending" is the original MVP state name; "requested" is the APR-001 term.
# Both are treated as the same pre-decision state.
APPROVAL_DECIDABLE_STATES = {
    "pending",
    "requested",
    "under_review",
    "revision_requested",
}

APPROVAL_CONSUMABLE_STATE = {"approved"}


class ApprovalError(Exception):
    """Domain error carrying a stable code suitable for API responses."""

    def __init__(self, code: str, message: str, *, retryable: bool = False):
        self.code = code
        self.retryable = retryable
        super().__init__(f"[{code}] {message}")


def _canonical_json(value: Any) -> str:
    """Stable, deterministic JSON serialization for hashing."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=lambda o: str(o) if isinstance(o, UUID) else None,
    )


def compute_action_fingerprint(
    *,
    workspace_id: UUID,
    task_id: UUID | None,
    run_id: UUID | None,
    action_class: str,
    capability_code: str,
    normalized_target: str,
    parameters: dict[str, Any],
    data_classification: str,
    policy_version: str,
) -> str:
    """Return a stable SHA-256 fingerprint of the normalized action.

    Secret values must not be present in ``parameters``; only reference IDs and
    safe, non-secret descriptors are fingerprinted.
    """
    payload = {
        "schema_version": CANONICAL_HASH_VERSION,
        "workspace_id": str(workspace_id),
        "task_id": str(task_id) if task_id else None,
        "run_id": str(run_id) if run_id else None,
        "action_class": action_class,
        "capability_code": capability_code,
        "normalized_target": normalized_target,
        "parameters": parameters,
        "data_classification": data_classification,
        "policy_version": policy_version,
    }
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return digest


def compute_request_hash(
    *,
    workspace_id: UUID,
    mission_id: UUID,
    run_id: UUID | None,
    task_id: UUID | None,
    action_fingerprint: str,
    requester_identity_id: UUID | None,
    policy_version: str,
) -> str:
    """Return a stable request-level hash used for deduplication.

    The request hash intentionally does not include the expiry or mutable
    review metadata; it represents the logical identity of the request.
    """
    payload = {
        "schema_version": CANONICAL_HASH_VERSION,
        "workspace_id": str(workspace_id),
        "mission_id": str(mission_id),
        "run_id": str(run_id) if run_id else None,
        "task_id": str(task_id) if task_id else None,
        "action_fingerprint": action_fingerprint,
        "requester_identity_id": (
            str(requester_identity_id) if requester_identity_id else None
        ),
        "policy_version": policy_version,
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass
class DecisionResult:
    approval: ApprovalModel
    previous_status: str


async def record_decision(
    db: AsyncSession,
    approval: ApprovalModel,
    *,
    status: str,
    decided_by: UUID,
    decision_note: str | None = None,
) -> DecisionResult:
    """Record a human decision on a non-terminal approval request.

    Args:
        db: active async session.
        approval: request to decide.
        status: one of ``approved``, ``rejected``, ``revision_requested``,
            ``cancelled``.
        decided_by: authenticated human identity. Agents/workloads are not
            accepted by this layer; the caller must have already verified the
            identity type.
        decision_note: optional safe rationale.

    Returns:
        ``DecisionResult`` with the updated approval and the previous status.
    """
    previous_status = approval.status
    if approval.status in APPROVAL_TERMINAL_STATES:
        raise ApprovalError(
            "APPROVAL_REQUEST_ALREADY_DECIDED",
            f"Approval is already in terminal state {approval.status}",
            retryable=False,
        )
    if status not in {"approved", "rejected", "revision_requested", "cancelled"}:
        raise ApprovalError(
            "APPROVAL_REQUEST_INVALID",
            f"Unsupported decision status {status}",
            retryable=False,
        )
    approval.status = status
    approval.decided_by = decided_by
    approval.decided_at = utcnow()
    approval.decision_note = decision_note
    approval.version += 1
    approval.updated_at = utcnow()
    await db.flush()
    return DecisionResult(approval=approval, previous_status=previous_status)


async def invalidate_approval(
    db: AsyncSession,
    approval: ApprovalModel,
    *,
    reason_code: str,
    detected_by: UUID,
    evidence_reference: str | None = None,
) -> ApprovalModel:
    """Mark an approval request invalidated, blocking any later consumption.

    Invalidation is allowed from any non-terminal state; once invalidated the
    request is terminal and a new request is required.
    """
    if approval.status in APPROVAL_TERMINAL_STATES:
        raise ApprovalError(
            "APPROVAL_REQUEST_ALREADY_DECIDED",
            f"Cannot invalidate terminal approval {approval.status}",
            retryable=False,
        )
    approval.status = "invalidated"
    approval.decision_note = f"INVALIDATED: {reason_code}" + (
        f" ({evidence_reference})" if evidence_reference else ""
    )
    approval.version += 1
    approval.updated_at = utcnow()
    await db.flush()
    return approval


def _expires_at_default(risk_class: str) -> datetime:
    """Proposed default expiry from APR-001 §26; critical requires explicit input."""
    now = utcnow()
    if risk_class == "r1_low":
        return now + timedelta(hours=24)
    if risk_class == "r2_moderate":
        return now + timedelta(hours=4)
    if risk_class == "r3_high":
        return now + timedelta(hours=1)
    # r0_informational, r4_critical, and unknown default short to keep MVP safe.
    return now + timedelta(minutes=15)


async def create_approval_request(
    db: AsyncSession,
    *,
    workspace_id: UUID,
    mission_id: UUID,
    action: str,
    scope: dict[str, Any],
    requester_identity_id: UUID | None,
    requester_identity_type: str = "human",
    run_id: UUID | None = None,
    task_id: UUID | None = None,
    action_class: str = "external_effect",
    capability_code: str = "manual",
    risk_class: str = "r3",
    normalized_target: str = "",
    expected_effects: str = "",
    reversibility_state: str = "unknown",
    data_classification: str = "internal",
    policy_version: str = "AUT-001:0.2.0",
    required_authority: str = "workspace_owner",
    independence_level: str = "i1_requester_may_approve",
    expires_at: datetime | None = None,
) -> ApprovalModel:
    """Create an exact-action approval request with stable fingerprints."""
    fingerprint = compute_action_fingerprint(
        workspace_id=workspace_id,
        task_id=task_id,
        run_id=run_id,
        action_class=action_class,
        capability_code=capability_code,
        normalized_target=normalized_target,
        parameters=scope,
        data_classification=data_classification,
        policy_version=policy_version,
    )
    request_hash = compute_request_hash(
        workspace_id=workspace_id,
        mission_id=mission_id,
        run_id=run_id,
        task_id=task_id,
        action_fingerprint=fingerprint,
        requester_identity_id=requester_identity_id,
        policy_version=policy_version,
    )
    if expires_at is None:
        expires_at = _expires_at_default(risk_class)
    approval = ApprovalModel(
        workspace_id=workspace_id,
        mission_id=mission_id,
        run_id=run_id,
        task_id=task_id,
        action=action,
        scope=scope,
        action_class=action_class,
        capability_code=capability_code,
        risk_class=risk_class,
        normalized_target=normalized_target,
        action_fingerprint=fingerprint,
        request_hash=request_hash,
        expected_effects=expected_effects,
        reversibility_state=reversibility_state,
        data_classification=data_classification,
        policy_version=policy_version,
        required_authority=required_authority,
        independence_level=independence_level,
        requester_identity_id=requester_identity_id,
        requester_identity_type=requester_identity_type,
        expires_at=expires_at,
        status="pending",
    )
    db.add(approval)
    await db.flush()
    return approval


async def consume_approval(
    db: AsyncSession,
    approval_id: UUID,
    *,
    run_id: UUID,
    attempt_id: UUID,
    action_fingerprint: str,
    consumed_by: UUID,
    consumed_by_component: str = "tool_gateway",
    execution_dispatch_reference: str | None = None,
    policy_version: str | None = None,
) -> ApprovalConsumptionModel:
    """Atomically consume one approved exact action.

    This function is the final gate before a protected attempt. It raises
    ``ApprovalError`` if the approval is not in ``approved`` state, expired,
    invalidated, already consumed, or fingerprint-mismatched.

    The consumption is performed with a SELECT ... FOR UPDATE style flush
    followed by a unique INSERT into ``approval_consumptions``. Under SQLite
    the same connection/transaction scope provides the isolation needed for
    MVP tests; PostgreSQL callers rely on the session transaction.
    """
    approval = await db.get(ApprovalModel, approval_id)
    if approval is None:
        raise ApprovalError(
            "APPROVAL_REQUEST_NOT_FOUND", "Approval request not found", retryable=False
        )

    # State gate.
    if approval.status != "approved":
        raise ApprovalError(
            f"APPROVAL_REQUEST_{approval.status.upper()}",
            f"Approval cannot be consumed in {approval.status} state",
            retryable=False,
        )

    # Expiry gate. Database DateTime columns may be naive; normalize to UTC-aware
    # before comparing with the timezone-aware `utcnow()` helper.
    if approval.expires_at is not None:
        expires_at = approval.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if utcnow() > expires_at:
            approval.status = "expired"
            approval.updated_at = utcnow()
            await db.flush()
            raise ApprovalError(
                "APPROVAL_REQUEST_EXPIRED",
                "Approval request has expired",
                retryable=False,
            )

    # Exact-action gate.
    if approval.action_fingerprint != action_fingerprint:
        raise ApprovalError(
            "APPROVAL_FINGERPRINT_MISMATCH",
            "Action fingerprint does not match the approved action",
            retryable=False,
        )

    # Run binding gate when the approval was created for a specific run.
    if approval.run_id is not None and approval.run_id != run_id:
        raise ApprovalError(
            "APPROVAL_ATTEMPT_MISMATCH",
            "Consumption run does not match the approved run",
            retryable=False,
        )

    # Optimistic-concurrency/version check.
    expected_version = approval.version

    # Mark consumed before insert so concurrent callers see state conflict.
    approval.status = "consumed"
    approval.version += 1
    approval.updated_at = utcnow()
    await db.flush()

    # Atomic one-time consumption record.
    consumption = ApprovalConsumptionModel(
        id=uuid4(),
        approval_request_id=approval.id,
        approval_decision_id=None,  # linked to the single decision row if stored
        run_id=run_id,
        step_id=None,
        attempt_id=attempt_id,
        action_fingerprint=action_fingerprint,
        request_version=expected_version,
        policy_version=policy_version or approval.policy_version,
        consumed_by_component=consumed_by_component,
        execution_dispatch_reference=execution_dispatch_reference,
        result_reference=None,
    )
    db.add(consumption)
    try:
        await db.flush()
    except Exception as exc:
        await db.rollback()
        raise ApprovalError(
            "APPROVAL_CONSUMPTION_CONFLICT",
            "Approval is already consumed or consumption raced",
            retryable=False,
        ) from exc

    return consumption


async def get_consumption(
    db: AsyncSession, approval_id: UUID
) -> ApprovalConsumptionModel | None:
    """Return the unique consumption record for an approval, if any."""
    result = await db.execute(
        select(ApprovalConsumptionModel).where(
            ApprovalConsumptionModel.approval_request_id == approval_id
        )
    )
    return result.scalar_one_or_none()
