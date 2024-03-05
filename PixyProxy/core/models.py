from pydantic import BaseModel


class ImageDetailCreate(BaseModel):
    prompt: str


class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str
