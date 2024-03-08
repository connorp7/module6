from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from core.models import ImageDetail, ImageDetailCreate
from service.image_service import ImageServiceInterface
from web.dependencies import get_image_service

router = APIRouter()


@router.post("/", response_model=ImageDetail, status_code=200)
async def add_image(image: ImageDetailCreate,
                    service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.create_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{guid}", response_model=ImageDetail, status_code=200)
def get_image_by_guid(guid: str,
                      service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image_by_guid(guid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[ImageDetail], status_code=200)
def get_all_images(service: ImageServiceInterface = Depends(get_image_service)):
    try:
        return service.get_all_images()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{guid}/content", status_code=200)
def get_image_file(guid: str, service: ImageServiceInterface = Depends(get_image_service)):
    try:
        image_file_path = "C:/Users/Connor/AIToolsForSWDelivery/module6/module6/PixyProxy/images/"
        image_file_path += service.get_image_file(guid)
        return FileResponse(image_file_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
