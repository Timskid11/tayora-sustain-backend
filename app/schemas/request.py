from pydantic import BaseModel
from app.models.request import RequestStatus
from app.models.donation import FabricType
from typing import Optional


class MaterialRequestCreate(BaseModel):
    fabric_type: FabricType
    quantity_needed: str
    purpose: Optional[str] = None


class MaterialRequestUpdate(BaseModel):
    fabric_type: Optional[FabricType] = None
    quantity_needed: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[RequestStatus] = None


class MaterialRequestOut(BaseModel):
    id: int
    requester_id: int
    fabric_type: FabricType
    quantity_needed: str
    purpose: Optional[str]
    status: RequestStatus

    class Config:
        from_attributes = True