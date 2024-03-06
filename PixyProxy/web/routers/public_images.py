from fastapi import APIRouter, Depends, HTTPException
from core.exceptions import RecordNotFoundError
from core.models import ImageDetail, ImageDetailCreate, User
from service.image_service import ImageServiceInterface
from typing import List
from web.dependencies import get_image_service, require_admin_user
from urllib.parse import unquote_plus

router = APIRouter()

@router.post("/image/", status_code=201, summary="Add a new image. Requires an admin user.")
async def add_image(image: ImageDetailCreate,
                    service: ImageServiceInterface = Depends(get_image_service),
                    _user: User = Depends(require_admin_user)):
    return service.create_image(image)
    
   

@router.get("/image/{guid}", summary="Get an image by GUID.")
def get_image_by_guid(guid: str,
                    service: ImageServiceInterface = Depends(get_image_service),
                    _user: User = Depends(require_admin_user)):
    return service.get_image_by_guid(guid)

@router.get("/image/", summary="Get all images.")
def get_all_images(service: ImageServiceInterface = Depends(get_image_service),
                    _user: User = Depends(require_admin_user)):
    return service.get_all_images()

@router.get("/image/{guid}/content", summary="Get image file by GUID.")
def get_image_file(guid: str, service: ImageServiceInterface = Depends(get_image_service), 
                    _user: User = Depends(require_admin_user)):
    return service.get_image_file(guid)