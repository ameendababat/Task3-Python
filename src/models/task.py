from sqlalchemy import String, Integer, Boolean, DateTime, Column, func
from datetime import datetime
from src.models.base import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000),  nullable=True)
    priority = Column(Integer, default=0)
    done = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"Task id={self.id} title={self.title}  priority={self.priority}  is_done={self.done}"