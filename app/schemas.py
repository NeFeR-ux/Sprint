from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models import StatusEnum

class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int

class LevelSchema(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

class ImageSchema(BaseModel):
    data: str
    title: Optional[str] = None

class UserSchema(BaseModel):
    email: str
    phone: str
    full_name: str

class PerevalCreateSchema(BaseModel):
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: List[ImageSchema]

class PerevalResponseSchema(BaseModel):
    id: int
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    status: StatusEnum
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: List[ImageSchema]

class SubmitDataResponse(BaseModel):
    status: int
    message: str
    id: Optional[int] = None