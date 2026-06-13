from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base
import enum


class FabricType(str, enum.Enum):
    cotton = "cotton"
    silk = "silk"
    linen = "linen"
    polyester = "polyester"
    denim = "denim"
    wool = "wool"
    nylon = "nylon"
    lycra = "lycra"
    chiffon = "chiffon"
    velvet = "velvet"
    other = "other"


class DonationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    collected = "collected"
    redistributed = "redistributed"


class DonationCategory(str, enum.Enum):
    redistribution = "redistribution"
    upcycling = "upcycling"
    pickup = "pickup"


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fabric_type = Column(Enum(FabricType), nullable=False)
    quantity = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(Enum(DonationStatus), default=DonationStatus.pending)
    category = Column(Enum(DonationCategory), nullable=True)
    location = Column(String, nullable=False)