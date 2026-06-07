from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base
import enum

class RequestStatus(str, enum.Enum):
    open = "open"
    matched = "matched"
    fulfilled = "fulfilled"
    closed = "closed"

class MaterialRequest(Base):
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fabric_type = Column(String, nullable=False)
    quantity_needed = Column(String, nullable=False)
    purpose = Column(String, nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.open)