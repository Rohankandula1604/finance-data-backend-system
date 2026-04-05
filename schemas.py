from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    name: str
    email: str
    role: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str | None = None


class RecordCreate(RecordBase):
    created_by: int


class RecordResponse(RecordBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True