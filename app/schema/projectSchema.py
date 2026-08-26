from pydantic import BaseModel
from typing import Optional
from datetime import datetime 


class CreateProject(BaseModel):
        name: str
        description: str | None = None
        owner_id: str | None = None
        members: list
        status: str | None = None
        created_at: datetime | None = None
        updated_at: datetime | None = None
