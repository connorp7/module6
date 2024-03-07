from pydantic import BaseModel
from datetime import datetime


class ImageDetailCreate(BaseModel):
    prompt: str


class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str


