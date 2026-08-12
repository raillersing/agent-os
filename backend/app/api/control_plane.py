"""Workspace-scoped persistent control-plane endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..models.control_plane import Approval as ApprovalModel
from ..models.control_plane import AuditEvent as AuditEventModel
from ..models.control_plane import Automation as AutomationModel
from ..models.control_plane import Mission as MissionModel
from ..models.control_plane import Workspace as WorkspaceModel
from ..schemas.control_plane import (
    Approval,
    ApprovalCreate,
    ApprovalDecision,
    AuditEvent,
    Automation,
    AutomationCreate,
    Mission,
    MissionCreate,
    Workspace,
    WorkspaceCreate,
)

router = APIRouter()


def record_event(
    db: AsyncSession,
    workspace_id: UUID,
    event_type: str,
    resource_type: str,
    resource_id: UUID,
    details: dict,
) -> None:
    """Queue an append-only audit record in the same transaction as the mutation."""
    db.add(
        AuditEventModel(
            workspace_id=workspace_id,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
        )
    )


async def require_workspace(db: AsyncSession, workspace_id: UUID) -> WorkspaceModel:
    workspace = await db.get(WorkspaceModel, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace


@router.get("/workspaces", response_model=list[Workspace])
async def list_workspaces(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WorkspaceModel).order_by(WorkspaceModel.created_at)
    )
    return result.scalars().all()


@router.post("/workspaces", response_model=Workspace, status_code=201)
async def create_workspace(
    payload: WorkspaceCreate, db: AsyncSession = Depends(get_db)
):
    workspace = WorkspaceModel(**payload.model_dump())
    db.add(workspace)
    await db.flush()
    record_event(
        db,
        workspace.id,
        "workspace.created",
        "workspace",
        workspace.id,
        {"name": workspace.name},
    )
    await db.commit()
    await db.refresh(workspace)
    return workspace


@router.get("/missions", response_model=list[Mission])
async def list_missions(
    workspace_id: UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(MissionModel).order_by(MissionModel.created_at.desc())
    if workspace_id:
        query = query.where(MissionModel.workspace_id == workspace_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/missions", response_model=Mission, status_code=201)
async def create_mission(payload: MissionCreate, db: AsyncSession = Depends(get_db)):
    await require_workspace(db, payload.workspace_id)
    mission = MissionModel(**payload.model_dump())
    db.add(mission)
    await db.flush()
    record_event(
        db,
        mission.workspace_id,
        "mission.created",
        "mission",
        mission.id,
        {"title": mission.title},
    )
    await db.commit()
    await db.refresh(mission)
    return mission


@router.patch("/missions/{mission_id}/status", response_model=Mission)
async def update_mission_status(
    mission_id: UUID,
    status: str,
    progress: int = Query(default=0, ge=0, le=100),
    db: AsyncSession = Depends(get_db),
):
    mission = await db.get(MissionModel, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    allowed = {
        "draft",
        "planned",
        "running",
        "waiting_approval",
        "completed",
        "failed",
        "cancelled",
    }
    if status not in allowed:
        raise HTTPException(status_code=422, detail="Unsupported mission status")
    mission.status = status
    mission.progress = progress
    mission.updated_at = datetime.utcnow()
    record_event(
        db,
        mission.workspace_id,
        "mission.status_updated",
        "mission",
        mission.id,
        {"status": status, "progress": progress},
    )
    await db.commit()
    await db.refresh(mission)
    return mission


@router.get("/automations", response_model=list[Automation])
async def list_automations(
    workspace_id: UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(AutomationModel).order_by(AutomationModel.created_at.desc())
    if workspace_id:
        query = query.where(AutomationModel.workspace_id == workspace_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/automations", response_model=Automation, status_code=201)
async def create_automation(
    payload: AutomationCreate, db: AsyncSession = Depends(get_db)
):
    await require_workspace(db, payload.workspace_id)
    automation = AutomationModel(**payload.model_dump())
    db.add(automation)
    await db.flush()
    record_event(
        db,
        automation.workspace_id,
        "automation.created",
        "automation",
        automation.id,
        {"name": automation.name, "trigger_type": automation.trigger_type},
    )
    await db.commit()
    await db.refresh(automation)
    return automation


@router.get("/approvals", response_model=list[Approval])
async def list_approvals(
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(ApprovalModel).order_by(ApprovalModel.created_at.desc())
    if status:
        query = query.where(ApprovalModel.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/audit-events", response_model=list[AuditEvent])
async def list_audit_events(
    workspace_id: UUID = Query(...),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    await require_workspace(db, workspace_id)
    result = await db.execute(
        select(AuditEventModel)
        .where(AuditEventModel.workspace_id == workspace_id)
        .order_by(AuditEventModel.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/approvals", response_model=Approval, status_code=201)
async def create_approval(payload: ApprovalCreate, db: AsyncSession = Depends(get_db)):
    mission = await db.get(MissionModel, payload.mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    approval = ApprovalModel(**payload.model_dump())
    mission.status = "waiting_approval"
    db.add(approval)
    await db.flush()
    record_event(
        db,
        mission.workspace_id,
        "approval.requested",
        "approval",
        approval.id,
        {"mission_id": str(mission.id), "action": approval.action},
    )
    await db.commit()
    await db.refresh(approval)
    return approval


@router.post("/approvals/{approval_id}/decision", response_model=Approval)
async def decide_approval(
    approval_id: UUID,
    payload: ApprovalDecision,
    db: AsyncSession = Depends(get_db),
):
    approval = await db.get(ApprovalModel, approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    if approval.status != "pending":
        raise HTTPException(status_code=409, detail="Approval already decided")
    approval.status = payload.status
    approval.decision_note = payload.decision_note
    approval.decided_at = datetime.utcnow()
    mission = await db.get(MissionModel, approval.mission_id)
    if mission is None:
        raise HTTPException(status_code=409, detail="Approval has no mission record")
    record_event(
        db,
        mission.workspace_id,
        f"approval.{payload.status}",
        "approval",
        approval.id,
        {"mission_id": str(mission.id), "decision_note": payload.decision_note},
    )
    await db.commit()
    await db.refresh(approval)
    return approval
