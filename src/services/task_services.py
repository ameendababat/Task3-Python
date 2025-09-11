from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.schemas.task import TaskCreate, TaskUpdate
from src.services.task_services import TaskRepository
from src.schemas.task import TaskCreate, TaskUpdate
from src.common.exceptions.http_exceptions import NotFoundException


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