from pydantic import BaseModel


class TaskIDSchema(BaseModel):
    task_id: str
    status: str = "queued"
    message: str = "Task accepted"
