from bson import ObjectId
from pydantic import BaseModel, Field

from .constants import IN_PROGRESS_STATUS


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TaskCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: str = Field(IN_PROGRESS_STATUS)
    file: bytes = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TaskUpdate(BaseModel):
    status: str = Field(...)
    result: dict
    file: bytes = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TaskInDB(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    status: str
    result: dict = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Task(TaskInDB):
    pass
