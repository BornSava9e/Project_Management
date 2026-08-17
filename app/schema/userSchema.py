from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict
from datetime  import datetime

class GetUser(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str | None = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"   # ignore fields not defined in schema

class CreateUser(BaseModel): 
    name: str
    email: EmailStr
    password: str