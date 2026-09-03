from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"

class Priortity(str, Enum):
    low ="low"
    medium ="medium"
    high= "high"
    critical= "critical"

class CreateTask(BaseModel):
    title: str
    description: str | None = None
    assigned_to: str | None = None
    status: Status = Status.todo
    priority: Priortity = Priortity.medium
    due_date: datetime | None = None
    tags: list[str] | None = None




