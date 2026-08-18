"""Workspace-scoped persistent control-plane endpoints."""

import asyncio
import hashlib
import json
from datetime import datetime
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client
from temporalio.exceptions import CancelledError as TemporalCancelledError
from temporalio.exceptions import WorkflowAlreadyStartedError

from ..config import settings
from ..core.database import get_db
from ..core.security import require_authenticated_user
from ..models.control_plane import Approval as ApprovalModel
from ..models.control_plane import AuditEvent as AuditEventModel
from ..models.control_plane import Automation as AutomationModel
from ..models.control_plane import ContextManifest as ContextManifestModel
from ..models.control_plane import ExecutionReceipt as ExecutionReceiptModel
from ..models.control_plane import ExecutionRun as ExecutionRunModel
from ..models.control_plane import Mission as MissionModel
from ..models.control_plane import ModelInvocation as ModelInvocationModel
from ..models.control_plane import Project as ProjectModel
from ..models.control_plane import RunAttempt as RunAttemptModel
from ..models.control_plane import Task as TaskModel
from ..models.control_plane import TaskSnapshot as TaskSnapshotModel
from ..models.control_plane import UsageRecord as UsageRecordModel
from ..models.control_plane import Workspace as WorkspaceModel
from ..schemas.control_plane import (
    Approval,
    ApprovalCreate,
    ApprovalDecision,
    AuditEvent,
    Automation,
    AutomationCreate,
    ExecutionRun,
    ExecutionRunCreate,
    Mission,
    MissionCreate,
    Project,
    ProjectCreate,
    ProjectUpdate,
    Task,
    TaskCreate,
    Workspace,
    WorkspaceCreate,
)
from ..temporal.reconciliation import (
    dispatch_recoverable_filter,
    is_dispatch_recoverable,
)
from ..temporal.workflows import D1SimulatorRunInput, D1SimulatorRunWorkflow

router = APIRouter()


def _is_temporal_cancellation(error: BaseException) -> bool:
    """Recognize direct and wrapped Temporal cancellation failures."""
    seen: set[int] = set()
    current: BaseException | None = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, (TemporalCancelledError, asyncio.CancelledError)):
            return True
        current = getattr(current, "cause", None) or current.__cause__
    return False


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


async def dispatch_durable_run(
    db: AsyncSession,
    run_id: UUID,
    input_text: str,
    simulator_profile: str,
    execution_mode: str = "simulator",
    model_profile: str = "model.general.balanced",
    *,
    recovery: bool = False,
) -> bool:
    """Start a stable Temporal workflow and record one durable dispatch edge."""
    run = await db.get(ExecutionRunModel, run_id)
    if run is None:
        return False
    if not is_dispatch_recoverable(run):
        return False
    client = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
    )
    try:
        await client.start_workflow(
            D1SimulatorRunWorkflow.run,
            D1SimulatorRunInput(
                str(run.id),
                str(run.workspace_id),
                input_text,
                simulator_profile,
                execution_mode,
                model_profile,
            ),
            id=run.workflow_id,
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )
    except WorkflowAlreadyStartedError:
        pass
    except Exception:
        await db.rollback()
        run = await db.get(ExecutionRunModel, run_id)
        if run is not None and is_dispatch_recoverable(run):
            run.state, run.state_reason, run.version = (
                "unknown",
                "temporal_dispatch_unconfirmed",
                run.version + 1,
            )
            record_event(
                db,
                run.workspace_id,
                "run.dispatch_unknown",
                "execution_run",
                run.id,
                {},
            )
            await db.commit()
        return False

    transitioned = await db.execute(
        update(ExecutionRunModel)
        .where(
            ExecutionRunModel.id == run_id,
            dispatch_recoverable_filter(ExecutionRunModel),
        )
        .values(
            state="queued",
            state_reason=None,
            version=ExecutionRunModel.version + 1,
        )
    )
    if transitioned.rowcount:
        record_event(
            db,
            run.workspace_id,
            "run.dispatched",
            "execution_run",
            run.id,
            {
                "workflow_id": run.workflow_id,
                "idempotent_recovery": recovery,
            },
        )
    await db.commit()
    return True


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


@router.get("/projects", response_model=list[Project])
async def list_projects(
    workspace_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    await require_workspace(db, workspace_id)
    query = (
        select(ProjectModel)
        .where(ProjectModel.workspace_id == workspace_id)
        .order_by(ProjectModel.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/projects", response_model=Project, status_code=201)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_authenticated_user),
):
    await require_workspace(db, payload.workspace_id)
    project = ProjectModel(
        **payload.model_dump(),
        created_by=uuid5(NAMESPACE_URL, f"agent-os:{current_user['sub']}"),
    )
    db.add(project)
    await db.flush()
    record_event(
        db,
        project.workspace_id,
        "project.created",
        "project",
        project.project_id,
        {"name": project.name, "purpose": project.purpose, "version": project.version},
    )
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=Project)
async def get_project(
    project_id: UUID,
    workspace_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    project = await db.get(ProjectModel, project_id)
    if project is None or project.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Project not found in workspace")
    return project


@router.patch("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    workspace_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    project = await db.get(ProjectModel, project_id)
    if project is None or project.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Project not found in workspace")
    if project.version != payload.expected_version:
        raise HTTPException(status_code=409, detail="Project version is stale")
    for field, value in payload.model_dump(
        exclude={"expected_version"}, exclude_none=True
    ).items():
        setattr(project, field, value)
    project.version += 1
    project.updated_at = datetime.utcnow()
    record_event(
        db,
        project.workspace_id,
        "project.updated",
        "project",
        project.project_id,
        {"state": project.state, "version": project.version},
    )
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/missions", response_model=list[Mission])
async def list_missions(
    workspace_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    await require_workspace(db, workspace_id)
    query = (
        select(MissionModel)
        .where(MissionModel.workspace_id == workspace_id)
        .order_by(MissionModel.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/missions", response_model=Mission, status_code=201)
async def create_mission(payload: MissionCreate, db: AsyncSession = Depends(get_db)):
    await require_workspace(db, payload.workspace_id)
    project = await db.get(ProjectModel, payload.project_id)
    if (
        project is None
        or project.workspace_id != payload.workspace_id
        or project.state == "archived"
    ):
        raise HTTPException(status_code=404, detail="Project not found in workspace")
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


@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_authenticated_user),
):
    await require_workspace(db, payload.workspace_id)
    mission = await db.get(MissionModel, payload.mission_id)
    project = await db.get(ProjectModel, payload.project_id)
    if (
        mission is None
        or project is None
        or mission.workspace_id != payload.workspace_id
        or mission.project_id != payload.project_id
        or project.workspace_id != payload.workspace_id
    ):
        raise HTTPException(
            status_code=404, detail="Mission not found in project workspace"
        )
    task = TaskModel(
        **payload.model_dump(),
        created_by=uuid5(NAMESPACE_URL, f"agent-os:{current_user['sub']}"),
    )
    db.add(task)
    await db.flush()
    record_event(
        db,
        task.workspace_id,
        "task.created",
        "task",
        task.id,
        {"mission_id": str(task.mission_id)},
    )
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/tasks", response_model=list[Task])
async def list_tasks(
    workspace_id: UUID = Query(...),
    mission_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    await require_workspace(db, workspace_id)
    query = select(TaskModel).where(TaskModel.workspace_id == workspace_id)
    if mission_id:
        query = query.where(TaskModel.mission_id == mission_id)
    return (
        (await db.execute(query.order_by(TaskModel.created_at.desc()))).scalars().all()
    )


@router.post("/tasks/{task_id}/runs", response_model=ExecutionRun, status_code=202)
async def start_execution_run(
    task_id: UUID, payload: ExecutionRunCreate, db: AsyncSession = Depends(get_db)
):
    task = await db.get(TaskModel, task_id)
    if task is None or task.workspace_id != payload.workspace_id:
        raise HTTPException(status_code=404, detail="Task not found in workspace")
    request_hash = hashlib.sha256(
        json.dumps(
            {
                "input_text": payload.input_text,
                "simulator_profile": payload.simulator_profile,
                "execution_mode": payload.execution_mode,
                "model_profile": payload.model_profile,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    existing = (
        await db.execute(
            select(ExecutionRunModel).where(
                ExecutionRunModel.workspace_id == payload.workspace_id,
                ExecutionRunModel.idempotency_key == payload.idempotency_key,
            )
        )
    ).scalar_one_or_none()
    if existing:
        if existing.request_hash != request_hash:
            raise HTTPException(
                status_code=409, detail="Idempotency key conflicts with another request"
            )
        if is_dispatch_recoverable(existing):
            await dispatch_durable_run(
                db,
                existing.id,
                payload.input_text,
                payload.simulator_profile,
                payload.execution_mode,
                payload.model_profile,
                recovery=True,
            )
            await db.refresh(existing)
        return await execution_run_response(db, existing)
    snapshot = TaskSnapshotModel(
        task_id=task.id,
        workspace_id=task.workspace_id,
        input_text=payload.input_text,
        simulator_profile=payload.simulator_profile,
        execution_mode=payload.execution_mode,
        model_profile=payload.model_profile,
        content_hash=hashlib.sha256(payload.input_text.encode()).hexdigest(),
    )
    db.add(snapshot)
    await db.flush()
    run = ExecutionRunModel(
        workspace_id=task.workspace_id,
        project_id=task.project_id,
        mission_id=task.mission_id,
        task_id=task.id,
        task_snapshot_id=snapshot.id,
        idempotency_key=payload.idempotency_key,
        request_hash=request_hash,
        correlation_id=payload.correlation_id or uuid4(),
        workflow_id=f"d1-run-{hashlib.sha256(f'{task.workspace_id}:{task.id}:{payload.idempotency_key}'.encode()).hexdigest()}",
    )
    db.add(run)
    try:
        await db.flush()
    except IntegrityError:
        # The database uniqueness constraint closes the race between two
        # simultaneous requests that passed the read-before-write lookup.
        await db.rollback()
        existing = (
            await db.execute(
                select(ExecutionRunModel).where(
                    ExecutionRunModel.workspace_id == payload.workspace_id,
                    ExecutionRunModel.idempotency_key == payload.idempotency_key,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            raise
        if existing.request_hash != request_hash:
            raise HTTPException(
                status_code=409, detail="Idempotency key conflicts with another request"
            )
        return await execution_run_response(db, existing)
    record_event(
        db,
        run.workspace_id,
        "run.accepted",
        "execution_run",
        run.id,
        {"task_id": str(task.id), "correlation_id": str(run.correlation_id)},
    )
    await db.commit()
    await db.refresh(run)
    await dispatch_durable_run(
        db,
        run.id,
        payload.input_text,
        payload.simulator_profile,
        payload.execution_mode,
        payload.model_profile,
    )
    await db.refresh(run)
    return await execution_run_response(db, run)


async def execution_run_response(db: AsyncSession, run: ExecutionRunModel) -> dict:
    from ..models.control_plane import Artifact, ExecutionReceipt, RunAttempt

    attempts = (
        (
            await db.execute(
                select(RunAttempt)
                .where(RunAttempt.run_id == run.id)
                .order_by(RunAttempt.attempt_number)
            )
        )
        .scalars()
        .all()
    )
    artifacts = (
        (await db.execute(select(Artifact).where(Artifact.run_id == run.id)))
        .scalars()
        .all()
    )
    receipt = (
        await db.execute(
            select(ExecutionReceipt).where(ExecutionReceipt.run_id == run.id)
        )
    ).scalar_one_or_none()
    snapshot = await db.get(TaskSnapshotModel, run.task_snapshot_id)
    return {
        **{column.name: getattr(run, column.name) for column in run.__table__.columns},
        "execution_mode": snapshot.execution_mode if snapshot else "simulator",
        "model_profile": snapshot.model_profile if snapshot else "unknown",
        "retry_count": max(len(attempts) - 1, 0),
        "attempts": attempts,
        "artifacts": artifacts,
        "receipt": receipt,
    }


@router.get("/execution-runs/{run_id}", response_model=ExecutionRun)
async def get_execution_run(
    run_id: UUID, workspace_id: UUID = Query(...), db: AsyncSession = Depends(get_db)
):
    run = await db.get(ExecutionRunModel, run_id)
    if run is None or run.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Run not found in workspace")
    return await execution_run_response(db, run)


@router.get("/execution-runs/{run_id}/evidence")
async def get_execution_run_evidence(
    run_id: UUID, workspace_id: UUID = Query(...), db: AsyncSession = Depends(get_db)
):
    """Return authorized D2 provenance without raw prompt or secret content."""
    run = await db.get(ExecutionRunModel, run_id)
    if run is None or run.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Run not found in workspace")
    manifests = (
        (
            await db.execute(
                select(ContextManifestModel)
                .where(ContextManifestModel.run_id == run.id)
                .order_by(ContextManifestModel.created_at)
            )
        )
        .scalars()
        .all()
    )
    invocations = (
        (
            await db.execute(
                select(ModelInvocationModel)
                .where(ModelInvocationModel.run_id == run.id)
                .order_by(ModelInvocationModel.created_at)
            )
        )
        .scalars()
        .all()
    )
    usage = (
        (
            await db.execute(
                select(UsageRecordModel)
                .where(UsageRecordModel.run_id == run.id)
                .order_by(UsageRecordModel.created_at)
            )
        )
        .scalars()
        .all()
    )
    snapshot = await db.get(TaskSnapshotModel, run.task_snapshot_id)
    return {
        "run_id": str(run.id),
        "execution_mode": snapshot.execution_mode if snapshot else "simulator",
        "model_profile": snapshot.model_profile if snapshot else "unknown",
        "retry_count": max(len(invocations) - 1, 0),
        "context_manifests": [
            {
                "id": str(item.id),
                "manifest_hash": item.manifest_hash,
                "context_profile_id": item.context_profile_id,
                "context_profile_version": item.context_profile_version,
                "segments": item.segments,
                "disclosure_state": item.disclosure_state,
                "token_budget": item.token_budget,
                "transformations": item.transformations,
            }
            for item in manifests
        ],
        "invocations": [
            {
                "id": str(item.id),
                "attempt_id": str(item.attempt_id),
                "adapter_id": item.adapter_id,
                "adapter_version": item.adapter_version,
                "logical_model_profile": item.logical_model_profile,
                "configured_provider": item.configured_provider,
                "configured_model": item.configured_model,
                "actual_provider": item.actual_provider,
                "actual_model": item.actual_model,
                "identity_state": item.identity_state,
                "invocation_state": item.invocation_state,
                "error_code": item.error_code,
                "provider_request_id": item.provider_request_id,
                "response_id": item.response_id,
                "prompt_hash": item.prompt_hash,
                "stop_reason": item.stop_reason,
                "refusal_state": item.refusal_state,
                "tools_enabled": bool(item.tools_enabled),
                "latency_ms": item.latency_ms,
            }
            for item in invocations
        ],
        "usage": [
            {
                "id": str(item.id),
                "attempt_id": str(item.attempt_id),
                "source": item.source,
                "completeness": item.completeness,
                "input_tokens": item.input_tokens,
                "output_tokens": item.output_tokens,
                "total_tokens": item.total_tokens,
                "cached_input_tokens": item.cached_input_tokens,
                "pricing_profile_version": item.pricing_profile_version,
                "currency": item.currency,
                "cost_state": item.cost_state,
                "estimated_cost": item.estimated_cost,
                "measured_cost": item.measured_cost,
                "provider_reported_cost": item.provider_reported_cost,
            }
            for item in usage
        ],
    }


@router.get("/execution-runs", response_model=list[ExecutionRun])
async def list_execution_runs(
    workspace_id: UUID = Query(...), db: AsyncSession = Depends(get_db)
):
    await require_workspace(db, workspace_id)
    runs = (
        (
            await db.execute(
                select(ExecutionRunModel)
                .where(ExecutionRunModel.workspace_id == workspace_id)
                .order_by(ExecutionRunModel.created_at.desc())
            )
        )
        .scalars()
        .all()
    )
    return [await execution_run_response(db, run) for run in runs]


@router.post("/execution-runs/{run_id}/cancel", response_model=ExecutionRun)
async def cancel_execution_run(
    run_id: UUID, workspace_id: UUID = Query(...), db: AsyncSession = Depends(get_db)
):
    run = await db.get(ExecutionRunModel, run_id)
    if run is None or run.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Run not found in workspace")
    if run.state in {"completed", "failed", "cancelled"}:
        raise HTTPException(status_code=409, detail="Run is already terminal")
    run.state, run.cancellation_state, run.version = (
        "cancelling",
        "requested",
        run.version + 1,
    )
    record_event(
        db,
        run.workspace_id,
        "run.cancellation_requested",
        "execution_run",
        run.id,
        {"workflow_id": run.workflow_id},
    )
    await db.commit()
    cancellation_confirmed = False
    try:
        client = await Client.connect(
            settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
        )
        handle = client.get_workflow_handle(run.workflow_id)
        await handle.cancel()
        # The cancellation request is not terminal evidence by itself. Wait
        # until Temporal closes the workflow before recording the business
        # terminal state, so a late activity completion cannot overwrite it.
        try:
            await handle.result()
        except TemporalCancelledError:
            cancellation_confirmed = True
        except asyncio.CancelledError:
            cancellation_confirmed = True
        except Exception as error:
            # A failed workflow is reconciled from the durable business row.
            cancellation_confirmed = _is_temporal_cancellation(error)
        await db.refresh(run)
        if run.state in {"completed", "failed", "cancelled"}:
            await db.commit()
            await db.refresh(run)
            return await execution_run_response(db, run)
        existing_receipt = (
            await db.execute(
                select(ExecutionReceiptModel).where(
                    ExecutionReceiptModel.run_id == run.id
                )
            )
        ).scalar_one_or_none()
        if existing_receipt and existing_receipt.terminal_state in {
            "completed",
            "failed",
            "cancelled",
        }:
            run.state = existing_receipt.terminal_state
            run.cancellation_state = (
                "confirmed"
                if existing_receipt.terminal_state == "cancelled"
                else run.cancellation_state
            )
            run.receipt_state = "available"
            run.ended_at = run.ended_at or datetime.utcnow()
            await db.commit()
            await db.refresh(run)
            return await execution_run_response(db, run)
        if not cancellation_confirmed:
            run.state, run.cancellation_state, run.state_reason, run.version = (
                "unknown",
                "unconfirmed",
                "cancellation_unconfirmed",
                run.version + 1,
            )
            record_event(
                db,
                run.workspace_id,
                "run.cancellation_unknown",
                "execution_run",
                run.id,
                {},
            )
            await db.commit()
            await db.refresh(run)
            return await execution_run_response(db, run)
        run.state, run.cancellation_state, run.ended_at, run.version = (
            "cancelled",
            "confirmed",
            datetime.utcnow(),
            run.version + 1,
        )
        attempt = (
            (
                await db.execute(
                    select(RunAttemptModel)
                    .where(RunAttemptModel.run_id == run.id)
                    .order_by(RunAttemptModel.attempt_number.desc())
                )
            )
            .scalars()
            .first()
        )
        if attempt and attempt.state == "running":
            attempt.state, attempt.ended_at = "cancelled", datetime.utcnow()
        snapshot = await db.get(TaskSnapshotModel, run.task_snapshot_id)
        run.receipt_state = "available"
        existing_receipt = (
            await db.execute(
                select(ExecutionReceiptModel).where(
                    ExecutionReceiptModel.run_id == run.id
                )
            )
        ).scalar_one_or_none()
        if existing_receipt is None:
            db.add(
                ExecutionReceiptModel(
                    workspace_id=run.workspace_id,
                    run_id=run.id,
                    attempt_id=attempt.id if attempt else None,
                    terminal_state="cancelled",
                    reason_code="cancelled_by_request",
                    simulator_identity="simulator/d0",
                    input_hash=snapshot.content_hash if snapshot else "unknown",
                )
            )
        record_event(db, run.workspace_id, "run.cancelled", "execution_run", run.id, {})
    except Exception:
        await db.refresh(run)
        if run.state in {"completed", "failed", "cancelled"}:
            await db.commit()
            await db.refresh(run)
            return await execution_run_response(db, run)
        run.state, run.cancellation_state, run.state_reason, run.version = (
            "unknown",
            "unconfirmed",
            "cancellation_unconfirmed",
            run.version + 1,
        )
        record_event(
            db,
            run.workspace_id,
            "run.cancellation_unknown",
            "execution_run",
            run.id,
            {},
        )
    await db.commit()
    await db.refresh(run)
    return await execution_run_response(db, run)


@router.patch("/missions/{mission_id}/status", response_model=Mission)
async def update_mission_status(
    mission_id: UUID,
    status: str,
    progress: int = Query(default=0, ge=0, le=100),
    workspace_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    mission = await db.get(MissionModel, mission_id)
    if mission is None or mission.workspace_id != workspace_id:
        raise HTTPException(status_code=404, detail="Mission not found in workspace")
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
