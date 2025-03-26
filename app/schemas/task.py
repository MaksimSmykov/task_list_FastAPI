from pydantic import BaseModel
from datetime import time, date


class Task(BaseModel):
    id: int
    title: str
    priority: str
    completed: bool = False
    add_info: str
    time: time
    date: date

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    priority: str
    completed: bool = False
    add_info: str
    time: time
    date: date