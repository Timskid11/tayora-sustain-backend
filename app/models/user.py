from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    donor = "donor"
    requester = "requester"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.requester)
    is_verified = Column(Boolean, default=False)