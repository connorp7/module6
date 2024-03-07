from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from data.generator import ImageGenerator
from data.image_repository import MySQLImageRepository, ImageRepositoryInterface

from service.image_service import ImageServiceInterface, ImageService

security = HTTPBasic()


def get_image_repository() -> ImageRepositoryInterface:
    return MySQLImageRepository()


def get_image_service(repo: ImageRepositoryInterface = Depends(get_image_repository)) -> ImageServiceInterface:
    return ImageService(repo, ImageGenerator())
