from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from src.common.db.connection import get_db
from sqlalchemy.orm import Session
from typing import List
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_servicesv2 import TaskServices


router = APIRouter(
    tags=["Tasks for V2"],
    prefix="/V2"
)


@router.get('/', response_model=List[TaskResponse])
async def list_tasks(offset: int = Query(0, ge=0), limit: int = Query(100, ge=1), session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.list_task(offset=offset, limit=limit)


@router.post('/add_task', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.task_create(data)


@router.get('/sorted-tasks', response_model=List[TaskResponse])
async def list_sorted(session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.list_sorted()


@router.get('/tasks', response_model=List[TaskResponse], description="Get a list of tasks with optional filtering by done status, sorting, and pagination")
async def list_task_v2(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort_by: str = Query("priority"),
    sort_order: str = Query("desc"),
    done: Optional[bool] = None,
    session: Session = Depends(get_db)
):
    service = TaskServices(session)
    return service.list_task_v2(offset, limit, sort_by, sort_order, done)


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.get_task(task_id)


@router.patch('/{task_id}', response_model=TaskResponse)
async def update_task(task_id: int, data: TaskUpdate, session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.task_update(task_id, data)


@router.post('/{task_id}/done', response_model=TaskResponse)
async def mark_done(task_id: int, session: Session = Depends(get_db)):
    service = TaskServices(session)
    return service.mark_task_done(task_id)


@router.delete('/{task_id}')
async def delete_task(task_id: int, session: Session = Depends(get_db)):
    service = TaskServices(session)
    service.delete_task(task_id)
    return {"detail": "Task deleted"}


