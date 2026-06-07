from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base
import enum

class DonationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    collected = "collected"
    redistributed = "redistributed"

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fabric_type = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(Enum(DonationStatus), default=DonationStatus.pending)
    location = Column(String, nullable=False)