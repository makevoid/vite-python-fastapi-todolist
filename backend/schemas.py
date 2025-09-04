from pydantic import BaseModel, ConfigDict
from typing import Optional

class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    completed: bool

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ''

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
