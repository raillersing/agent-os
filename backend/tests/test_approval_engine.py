"""Exact-action approval engine tests (APR-001 / AUT-001)."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.main import app
from app.models.control_plane import Approval as ApprovalModel
from app.services.approval_engine import (
    ApprovalError,
    compute_action_fingerprint,
    compute_request_hash,
    consume_approval,
    create_approval_request,
    get_consumption,
    record_decision,
)

from .conftest import auth_headers


@pytest_asyncio.fixture
async def db():
    """Provide an isolated async SQLAlchemy session for engine unit tests."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def exact_action_payload():
    workspace_id = uuid4()
    mission_id = uuid4()
    task_id = uuid4()
    run_id = uuid4()
    return {
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "task_id": task_id,
        "run_id": run_id,
        "action": "Write approved file",
        "scope": {"path": "/workspace/data.txt", "content_hash": "abc123"},
        "action_class": "controlled_write",
        "capability_code": "local.file.write",
        "risk_class": "r2_moderate",
        "normalized_target": "/workspace/data.txt",
        "expected_effects": "Creates or overwrites the target file",
        "reversibility_state": "partially_reversible",
        "data_classification": "internal",
        "policy_version": "AUT-001:0.2.0",
        "required_authority": "workspace_owner",
        "independence_level": "i1_requester_may_approve",
    }


def test_fingerprint_is_stable_and_sensitive_to_material_changes(
    exact_action_payload,
):
    base = exact_action_payload
    fp1 = compute_action_fingerprint(
        workspace_id=base["workspace_id"],
        task_id=base["task_id"],
        run_id=base["run_id"],
        action_class=base["action_class"],
        capability_code=base["capability_code"],
        normalized_target=base["normalized_target"],
        parameters=base["scope"],
        data_classification=base["data_classification"],
        policy_version=base["policy_version"],
    )
    fp2 = compute_action_fingerprint(
        workspace_id=base["workspace_id"],
        task_id=base["task_id"],
        run_id=base["run_id"],
        action_class=base["action_class"],
        capability_code=base["capability_code"],
        normalized_target=base["normalized_target"],
        parameters=base["scope"],
        data_classification=base["data_classification"],
        policy_version=base["policy_version"],
    )
    assert fp1 == fp2
    assert len(fp1) == 64  # SHA-256 hex

    changed_target = compute_action_fingerprint(
        workspace_id=base["workspace_id"],
        task_id=base["task_id"],
        run_id=base["run_id"],
        action_class=base["action_class"],
        capability_code=base["capability_code"],
        normalized_target="/workspace/other.txt",
        parameters=base["scope"],
        data_classification=base["data_classification"],
        policy_version=base["policy_version"],
    )
    assert changed_target != fp1

    changed_scope = compute_action_fingerprint(
        workspace_id=base["workspace_id"],
        task_id=base["task_id"],
        run_id=base["run_id"],
        action_class=base["action_class"],
        capability_code=base["capability_code"],
        normalized_target=base["normalized_target"],
        parameters={**base["scope"], "content_hash": "def456"},
        data_classification=base["data_classification"],
        policy_version=base["policy_version"],
    )
    assert changed_scope != fp1


def test_request_hash_stabilizes_logical_identity(exact_action_payload):
    base = exact_action_payload
    requester_identity_id = uuid4()
    h1 = compute_request_hash(
        workspace_id=base["workspace_id"],
        mission_id=base["mission_id"],
        run_id=base["run_id"],
        task_id=base["task_id"],
        action_fingerprint="fingerprint",
        requester_identity_id=requester_identity_id,
        policy_version=base["policy_version"],
    )
    h2 = compute_request_hash(
        workspace_id=base["workspace_id"],
        mission_id=base["mission_id"],
        run_id=base["run_id"],
        task_id=base["task_id"],
        action_fingerprint="fingerprint",
        requester_identity_id=requester_identity_id,
        policy_version=base["policy_version"],
    )
    assert h1 == h2
    # A different requester produces a different logical identity.
    h3 = compute_request_hash(
        workspace_id=base["workspace_id"],
        mission_id=base["mission_id"],
        run_id=base["run_id"],
        task_id=base["task_id"],
        action_fingerprint="fingerprint",
        requester_identity_id=uuid4(),
        policy_version=base["policy_version"],
    )
    assert h3 != h1


@pytest.mark.asyncio
async def test_create_approval_request_persists_fingerprint_and_hash(db: AsyncSession):
    workspace_id = uuid4()
    mission_id = uuid4()
    task_id = uuid4()
    run_id = uuid4()
    requester = uuid4()

    approval = await create_approval_request(
        db,
        workspace_id=workspace_id,
        mission_id=mission_id,
        action="Send external message",
        scope={"recipients": ["alice@example.com"]},
        requester_identity_id=requester,
        run_id=run_id,
        task_id=task_id,
        action_class="external_effect",
        capability_code="email.send",
        normalized_target="alice@example.com",
        risk_class="r3_high",
    )
    await db.commit()

    assert approval.status == "pending"
    assert approval.action_fingerprint
    assert approval.request_hash
    assert approval.workspace_id == workspace_id
    assert approval.run_id == run_id
    assert approval.task_id == task_id
    assert approval.requester_identity_id == requester


@pytest.mark.asyncio
async def test_decision_is_immutable_and_human_only(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={},
        requester_identity_id=uuid4(),
    )
    await db.commit()

    decider = uuid4()
    await record_decision(db, approval, status="approved", decided_by=decider)
    await db.commit()
    assert approval.status == "approved"
    assert approval.decided_by == decider

    with pytest.raises(ApprovalError, match="APPROVAL_REQUEST_ALREADY_DECIDED"):
        await record_decision(db, approval, status="rejected", decided_by=uuid4())


@pytest.mark.asyncio
async def test_consume_approval_atomic_one_time(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={"x": 1},
        requester_identity_id=uuid4(),
    )
    await record_decision(db, approval, status="approved", decided_by=uuid4())
    await db.commit()

    run_id = uuid4()
    attempt_id = uuid4()
    consumer = uuid4()
    consumption = await consume_approval(
        db,
        approval.id,
        run_id=run_id,
        attempt_id=attempt_id,
        action_fingerprint=approval.action_fingerprint,
        consumed_by=consumer,
    )
    await db.commit()

    assert consumption.approval_request_id == approval.id
    assert consumption.run_id == run_id
    assert consumption.attempt_id == attempt_id

    reloaded = await db.get(ApprovalModel, approval.id)
    assert reloaded.status == "consumed"

    with pytest.raises(ApprovalError, match="APPROVAL_REQUEST_CONSUMED"):
        await consume_approval(
            db,
            approval.id,
            run_id=run_id,
            attempt_id=uuid4(),
            action_fingerprint=approval.action_fingerprint,
            consumed_by=consumer,
        )


@pytest.mark.asyncio
async def test_consumption_rejects_fingerprint_mismatch(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={"x": 1},
        requester_identity_id=uuid4(),
    )
    await record_decision(db, approval, status="approved", decided_by=uuid4())
    await db.commit()

    with pytest.raises(ApprovalError, match="APPROVAL_FINGERPRINT_MISMATCH"):
        await consume_approval(
            db,
            approval.id,
            run_id=uuid4(),
            attempt_id=uuid4(),
            action_fingerprint="0" * 64,
            consumed_by=uuid4(),
        )


@pytest.mark.asyncio
async def test_consumption_rejects_expired_approval(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={"x": 1},
        requester_identity_id=uuid4(),
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    await record_decision(db, approval, status="approved", decided_by=uuid4())
    await db.commit()

    with pytest.raises(ApprovalError, match="APPROVAL_REQUEST_EXPIRED"):
        await consume_approval(
            db,
            approval.id,
            run_id=uuid4(),
            attempt_id=uuid4(),
            action_fingerprint=approval.action_fingerprint,
            consumed_by=uuid4(),
        )


@pytest.mark.asyncio
async def test_consumption_rejects_run_mismatch(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={"x": 1},
        requester_identity_id=uuid4(),
        run_id=uuid4(),
    )
    await record_decision(db, approval, status="approved", decided_by=uuid4())
    await db.commit()

    with pytest.raises(ApprovalError, match="APPROVAL_ATTEMPT_MISMATCH"):
        await consume_approval(
            db,
            approval.id,
            run_id=uuid4(),
            attempt_id=uuid4(),
            action_fingerprint=approval.action_fingerprint,
            consumed_by=uuid4(),
        )


@pytest.mark.asyncio
async def test_get_consumption_returns_record_or_none(db: AsyncSession):
    approval = await create_approval_request(
        db,
        workspace_id=uuid4(),
        mission_id=uuid4(),
        action="Test",
        scope={"x": 1},
        requester_identity_id=uuid4(),
    )
    await record_decision(db, approval, status="approved", decided_by=uuid4())
    await db.commit()

    assert await get_consumption(db, approval.id) is None

    run_id = uuid4()
    attempt_id = uuid4()
    await consume_approval(
        db,
        approval.id,
        run_id=run_id,
        attempt_id=attempt_id,
        action_fingerprint=approval.action_fingerprint,
        consumed_by=uuid4(),
    )
    await db.commit()

    consumption = await get_consumption(db, approval.id)
    assert consumption is not None
    assert consumption.run_id == run_id


def test_api_consumes_approved_exact_action():
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace = client.post(
            "/api/v1/workspaces",
            json={"name": f"Approval {suffix}", "budget": 100},
        ).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "Approval test",
            },
        ).json()
        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "Approval test",
            },
        ).json()
        approval = client.post(
            "/api/v1/approvals",
            params={"workspace_id": workspace["id"]},
            json={
                "mission_id": mission["id"],
                "action": "Exact action",
                "scope": {"target": "x"},
                "normalized_target": "x",
                "action_class": "external_effect",
                "risk_class": "r3_high",
            },
        ).json()
        assert approval["status"] == "pending"
        fingerprint = approval["action_fingerprint"]

        client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            params={"workspace_id": workspace["id"]},
            json={"status": "approved"},
        ).raise_for_status()

        run_id = str(uuid4())
        attempt_id = str(uuid4())
        consumed = client.post(
            f"/api/v1/approvals/{approval['id']}/consume",
            params={"workspace_id": workspace["id"]},
            json={
                "run_id": run_id,
                "attempt_id": attempt_id,
                "action_fingerprint": fingerprint,
            },
        )
        assert consumed.status_code == 200
        assert consumed.json()["status"] == "consumed"

        duplicate = client.post(
            f"/api/v1/approvals/{approval['id']}/consume",
            params={"workspace_id": workspace["id"]},
            json={
                "run_id": run_id,
                "attempt_id": str(uuid4()),
                "action_fingerprint": fingerprint,
            },
        )
        assert duplicate.status_code == 409


def test_api_rejects_consumption_with_changed_fingerprint():
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace = client.post(
            "/api/v1/workspaces",
            json={"name": f"Approval {suffix}", "budget": 100},
        ).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "Approval test",
            },
        ).json()
        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "Approval test",
            },
        ).json()
        approval = client.post(
            "/api/v1/approvals",
            params={"workspace_id": workspace["id"]},
            json={
                "mission_id": mission["id"],
                "action": "Exact action",
                "scope": {"target": "x"},
                "normalized_target": "x",
            },
        ).json()
        client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            params={"workspace_id": workspace["id"]},
            json={"status": "approved"},
        ).raise_for_status()

        response = client.post(
            f"/api/v1/approvals/{approval['id']}/consume",
            params={"workspace_id": workspace["id"]},
            json={
                "run_id": str(uuid4()),
                "attempt_id": str(uuid4()),
                "action_fingerprint": "0" * 64,
            },
        )
        assert response.status_code == 409
        assert "FINGERPRINT_MISMATCH" in response.json()["detail"]


def test_api_invalidates_pending_approval():
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace = client.post(
            "/api/v1/workspaces",
            json={"name": f"Approval {suffix}", "budget": 100},
        ).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "Approval test",
            },
        ).json()
        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "Approval test",
            },
        ).json()
        approval = client.post(
            "/api/v1/approvals",
            params={"workspace_id": workspace["id"]},
            json={
                "mission_id": mission["id"],
                "action": "Exact action",
                "scope": {"target": "x"},
                "normalized_target": "x",
            },
        ).json()

        invalidated = client.post(
            f"/api/v1/approvals/{approval['id']}/invalidate",
            params={"workspace_id": workspace["id"]},
            json={"reason_code": "TARGET_CHANGED"},
        )
        assert invalidated.status_code == 200
        assert invalidated.json()["status"] == "invalidated"

        approved = client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            params={"workspace_id": workspace["id"]},
            json={"status": "approved"},
        )
        assert approved.status_code == 409
