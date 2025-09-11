from sqlalchemy.orm import Session
from src.repositories.task_repositoryv2 import TaskRepository
from typing import List, Optional
from src.schemas.task import TaskCreate, TaskUpdate
from src.repositories.task_repositoryv2 import TaskRepository
from src.schemas.task import TaskCreate, TaskUpdate
from src.common.exceptions.http_exceptions import NotFoundException
from src.models.task import Task
from src.repositories.task_repositoryv2 import TaskRepository


class TaskServices:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)
        self.db = db


    def task_create(self, data: TaskCreate):
        task = self.repo.add(data)
        self.db.commit()
        self.db.refresh(task)
        return task


    def get_task(self, task_id: int):
        task = self.repo.get(task_id)
        if not task:
            raise NotFoundException(detail=f"Task {task_id} not found")
        return task


    def list_task(self, offset: int = 0, limit: int = 100):
        return self.repo.list(offset=offset, limit=limit)


    def delete_task(self, task_id: int):
        task = self.repo.get(task_id)
        if not task:
            raise NotFoundException(detail=f"Task {task_id} not found")
        self.repo.delete(task)
        self.db.commit()
        return True


    def task_update(self, task_id: int, data: TaskUpdate):
        task = self.repo.get(task_id)
        if not task:
            raise NotFoundException(detail=f"Task {task_id} not found")
        self.repo.update(task, data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task


    def  list_sorted(self):
        return self.repo.list_sorted_by_priority()


    def mark_task_done(self, task_id: int):
        tasks = self.repo.get(task_id)
        if not tasks:
            raise NotFoundException(detail=f"Task {task_id} not found")
        task = self.repo.mark_done(tasks)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    
    def list_task_v2(
        self,
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "priority",
        sort_order: str = "desc",
        done: Optional[bool] = None
    ) -> List[Task]:
        return self.repo.list_V2(offset, limit, sort_by, sort_order, done)