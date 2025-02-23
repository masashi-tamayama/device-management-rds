from sqlalchemy import Column, String, DateTime, func
from .database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    manufacturer = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    ) 