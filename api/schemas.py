from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NodeBase(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class VMBase(BaseModel):
    id: int
    name: str
    nodes: List[NodeBase] = [] 
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    vm_id: int
    node_id: Optional[int] = None
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    id: int
    user_id: int
    username: str 
    vm_name: str
    node_name: Optional[str] = None
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True