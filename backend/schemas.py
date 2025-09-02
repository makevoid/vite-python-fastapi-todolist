from pydantic import BaseModel
from typing import Optional

class CounterResponse(BaseModel):
    id: int
    name: str
    value: int

    class Config:
        from_attributes = True

class CounterCreate(BaseModel):
    name: str
    initial_value: Optional[int] = 0

class CounterUpdate(BaseModel):
    value: int

class IncrementRequest(BaseModel):
    amount: Optional[int] = 1
