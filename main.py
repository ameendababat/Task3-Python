from fastapi import FastAPI
from src.routes.task_routes import router as tasks_router1
from src.routes.task_routesv2 import router as tasks_router2
from src.common.db.connection import engine
from src.models.base import Base


app = FastAPI(title="To-Do project MVC")

app.include_router(tasks_router1)
app.include_router(tasks_router2)


Base.metadata.create_all(bind=engine)

@app.get('/', tags=["Root"])
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {
        "message": "To-Do API is running",
        "status": "ok"
    }