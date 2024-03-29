import os
from typing import List, Optional
from pydantic import BaseModel
from core.models import ImageDetail, ImageDetailCreate
from data.image_repository import ImageRepositoryInterface
from core.exceptions import PixyProxyException, RecordNotFoundError, ConstraintViolationError
from data.__init__ import DatabaseContext, get_current_db_context
import traceback
from data.generator import ImageGenerator


class ImageServiceInterface:
    def create_image(self, image: ImageDetailCreate) -> dict:
        """
        Creates a new image in the database.

        Args:
            image (ImageDetailCreate): The image to create.

        Returns:
            ImageDetail: The details of the created image.

        Raises:
            ConstraintViolationError: If the image data is invalid.
            PixyProxyException: If an unexpected error occurs.
            :param image:
        """
        pass

    def get_image_by_guid(self, guid: str) -> ImageDetail:
        """
        Retrieves an image from the database by its GUID.

        Args:
            guid (str): The GUID of the image to retrieve.

        Returns:
            Optional[ImageDetail]: The details of the retrieved image, or None if no image was found.

        Raises:
            RecordNotFoundError: If no image was found with the provided GUID.
            PixyProxyException: If an unexpected error occurs.
            :param guid:
        """
        pass

    def get_all_images(self) -> List[ImageDetail]:
        """
        Retrieves all images from the database.

        Returns:
            List[ImageDetail]: A list of all images in the database.

        Raises:
            PixyProxyException: If an unexpected error occurs.
        """
        pass

    def get_image_file(self, guid: str) -> str:
        """
        Retrieves the file of an image from the database by its GUID.

        Args:
            guid (str): The GUID of the image to retrieve.

        Returns:
            str: The filename of the retrieved image.

        Raises:
            RecordNotFoundError: If no image was found with the provided GUID.
            PixyProxyException: If an unexpected error occurs.
            :param guid:
        """
        pass


class ImageService(ImageServiceInterface):
    def __init__(self, image_repository: ImageRepositoryInterface, image_generator: ImageGenerator):
        self.image_repository = image_repository
        self.image_generator = image_generator

    def create_image(self, image: ImageDetailCreate) -> (dict):

        try:
            image = ImageDetailCreate(**image.dict())
        except Exception as e:
            raise ConstraintViolationError(str(e))
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image_dict = self.image_repository.create_image(image)
                db.commit_transaction()
                return image_dict
            except PixyProxyException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PixyProxyException("An unexpected error occurred while processing your request.") from e

    def get_image_by_guid(self, guid: str) -> ImageDetail:

        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image = self.image_repository.get_image_details_by_guid(guid)
                db.commit_transaction()

                if image is None:
                    raise RecordNotFoundError()
                return image
            except PixyProxyException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PixyProxyException("An unexpected error occurred while processing your request.") from e

    def get_all_images(self) -> List[ImageDetail]:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                images = self.image_repository.get_all_images()
                db.commit_transaction()
                return images
            except PixyProxyException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PixyProxyException("An unexpected error occurred while processing your request.") from e

    def get_image_file(self, guid: str) -> str:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image_file = self.image_repository.get_image_file(guid)
                db.commit_transaction()
                if image_file is None:
                    raise RecordNotFoundError()
                return image_file
            except PixyProxyException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PixyProxyException("An unexpected error occurred while processing your request.") from e
