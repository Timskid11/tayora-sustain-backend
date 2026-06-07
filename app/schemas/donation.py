from pydantic import BaseModel
from app.models.donation import DonationStatus
from typing import Optional

class DonationCreate(BaseModel):
    fabric_type: str
    quantity: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    location: str

class DonationOut(BaseModel):
    id: int
    donor_id: int
    fabric_type: str
    quantity: str
    description: Optional[str]
    image_url: Optional[str]
    status: DonationStatus
    location: str

    class Config:
        from_attributes = True