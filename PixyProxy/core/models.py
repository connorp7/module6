from pydantic import BaseModel
from datetime import datetime


class ImageDetailCreate(BaseModel):
    prompt: str


class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str

class Image(ImageDetail):
    id: int
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    username: str
    password: str
    class_key: str