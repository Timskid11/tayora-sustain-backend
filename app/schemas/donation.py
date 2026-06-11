from pydantic import BaseModel
from app.models.donation import DonationStatus, FabricType
from typing import Optional


class DonationCreate(BaseModel):
    fabric_type: FabricType
    quantity: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    location: str


class DonationUpdate(BaseModel):
    fabric_type: Optional[FabricType] = None
    quantity: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    status: Optional[DonationStatus] = None


class DonationOut(BaseModel):
    id: int
    donor_id: int
    fabric_type: FabricType
    quantity: str
    description: Optional[str]
    image_url: Optional[str]
    status: DonationStatus
    location: str

    class Config:
        from_attributes = True