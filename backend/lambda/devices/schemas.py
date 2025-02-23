from datetime import datetime
from pydantic import BaseModel

class DeviceBase(BaseModel):
    name: str
    manufacturer: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 