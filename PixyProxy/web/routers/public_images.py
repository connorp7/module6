from fastapi import APIRouter, Depends, HTTPException
from core.exceptions import RecordNotFoundError
from core.models import ImageDetail, ImageDetailCreate
from service.image_service import ImageServiceInterface
from typing import List
from web.dependencies import get_image_service
from urllib.parse import unquote_plus

router = APIRouter()

@router.post("/", response_model=ImageDetail, status_code=200)
async def add_image(image: ImageDetailCreate,
                    service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.create_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/{guid}", status_code=200, summary="Get an image by GUID.")
def get_image_by_guid(guid: str,
                    service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image_by_guid(guid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", status_code=200, summary="Get all images.")
def get_all_images(service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.get_all_images()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{guid}/content", status_code=200, summary="Get image file by GUID.")
def get_image_file(guid: str, service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image_file(guid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))