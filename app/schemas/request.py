from pydantic import BaseModel
from app.models.request import RequestStatus
from typing import Optional

class MaterialRequestCreate(BaseModel):
    fabric_type: str
    quantity_needed: str
    purpose: Optional[str] = None

class MaterialRequestOut(BaseModel):
    id: int
    requester_id: int
    fabric_type: str
    quantity_needed: str
    purpose: Optional[str]
    status: RequestStatus

    class Config:
        from_attributes = True