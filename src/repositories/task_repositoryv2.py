from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from src.models.task import Task
from typing import Optional, List
from src.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        """
        Initialize the TaskRepository with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db
    
    
    def add(self, data: TaskCreate) -> Task:
        """
        Add a new task to the database.

        Returns:
            Task: The newly created Task object.
        """
        task = Task(
            title = data.title,
            description = data.description,
            priority = data.priority
        )
        self.db.add(task)
        self.db.flush()
        return task
    
    
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The Task object if found, otherwise None.
        """
        return self.db.query(Task).filter(Task.id == task_id).first()


    def list(self, offset: int = 0, limit: int = 100) -> List[Task]:
        """
        List tasks with optional pagination.

        Args:
            offset (int, optional): Number of tasks to skip. Defaults to 0.
            limit (int, optional): Maximum number of tasks to return. Defaults to 100.

        Returns:
            List[Task]: List of Task objects ordered by creation date descending.
        """
        return (
            self.db.query(Task)
            .order_by(Task.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    
    def delete(self, task: Task) -> None:
        """
        Delete a task from the database.

        Args:
            task (Task): The Task object to delete.
        """
        self.db.delete(task)


    def update(self, task: Task, data: TaskUpdate) -> Task:
        """
        Update the fields of an existing task.

        Args:
            task (Task): The Task object to update.
            data (TaskUpdate): Task update data.

        Returns:
            Task: The updated Task object.
        """
        if(data.title is not None):
            task.title = data.title
        if(data.description is not None):
            task.description = data.description
        if(data.priority is not None):
            task.priority = data.priority
        if(data.done is not None):
            task.done = data.done
        self.db.add(task)
        return task


    def list_sorted_by_priority(self) -> List[Task]:
        """
        List all tasks sorted by their priority in ascending order.

        Returns:
            List[Task]: List of Task objects sorted by priority.
        """
        return self.db.query(Task).order_by(Task.priority.asc()).all()
    
    
    def mark_done(self, task: Task) -> Task:
        """
        Mark a task as completed (done).

        Args:
            task (Task): The Task object to mark as done.

        Returns:
            Task: The updated Task object with done=True.
        """
        task.done = True
        self.db.add(task)
        return task
    
    
    def list_V2( 
        self,
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "priority",
        sort_order: str = "desc",
        done: Optional[bool] = None
    ) -> List[Task]:
        """
    List tasks with filtering, sorting, and pagination.

    Args:
        offset (int, optional): Number of tasks to skip. Defaults to 0.
        limit (int, optional): Maximum number of tasks to return. Defaults to 100.
        sort_by (str, optional): Column name to sort by (e.g., 'priority', 'created_at'). Defaults to "priority".
        sort_order (str, optional): Sort direction, "asc" for ascending or "desc" for descending. Defaults to "desc".
        done (Optional[bool], optional): Filter tasks by completion status. If None, no filtering is applied. Defaults to None.

    Returns:
        List[Task]: List of Task objects based on filters, sorted and paginated.
    """
        query = self.db.query(Task) #orderby create_at desc offset 10 limit 10
        if(done is not None):
            query = query.filter(Task.done == done)
        column = getattr(Task, sort_by, None)   
        if not column:
            column = Task.created_at
        if (sort_order.lower() == "desc"):
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

        return query.offset(offset=offset).limit(limit=limit).all()