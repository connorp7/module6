from core import make_guid
from core.exceptions import DBConnectionError
from core.models import ImageDetail, ImageDetailCreate
from openai import OpenAI
from datetime import datetime
from typing import Optional

from .__init__ import get_current_db_context
from .generator import ImageGenerator


class ImageRepositoryInterface:

    def get_image_details_by_guid(self, guid):
        # Implementation of the get image by guid use case
        pass

    def get_all_images(self):
        # Implementation of the get all images use case
        pass

    def create_image(self, image: ImageDetailCreate):
        # Implementation of the create image use case
        pass

    def get_image_file(self, guid):
        # Implementation of the retrieve image file use case
        pass


class MySQLImageRepository(ImageRepositoryInterface):
    def __init__(self):
        self.image_generator = ImageGenerator()

    def create_image(self, image: ImageDetailCreate) -> dict:
        filename = self.image_generator.generate_image(image)
        guid = make_guid()
        db_context = get_current_db_context()
        if not db_context:
            raise DBConnectionError()
        try:
            db_context.cursor.execute(
                "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
                (guid, filename, image.prompt),
            )
            db_context.commit_transaction()
        except Exception as e:
            db_context.rollback_transaction()
            raise
        return {"guid": guid, "filename": filename, "prompt": image.prompt}

    def get_image_details_by_guid(self, guid: str) -> ImageDetail:
        db_context = get_current_db_context()
        if not db_context:
            raise DBConnectionError("No database connection found")
        try:
            db_context.cursor.execute("SELECT guid, filename, prompt FROM images WHERE guid = %s", guid)
            row = db_context.cursor.fetchone()  # fetch the result
        except Exception as e:
            db_context.rollback_transaction()
            raise  # re-raise the exception
        if row:
            return ImageDetail(guid=row[0], filename=row[1], prompt=row[2])

        
    def get_all_images(self) -> list[ImageDetail]:
        db_context = get_current_db_context()
        if not db_context:
            raise DBConnectionError()
        try:
            db_context.cursor.execute("SELECT * FROM images")
            rows = db_context.cursor.fetchall()  # fetch the results
        except Exception as e:
            db_context.rollback_transaction()
            raise  # re-raise the exception

        return [ImageDetail(guid=row[0], filename=row[1], prompt=row[2]) for row in rows]

    def get_image_file(self, guid):
        db_context = get_current_db_context()
        if not db_context:
            raise DBConnectionError()
        try:
            db_context.cursor.execute("SELECT filename FROM images WHERE guid = %s", guid)
            result = db_context.cursor.fetchone()  # fetch the result
        except Exception as e:
            db_context.rollback_transaction()
            raise  # re-raise the exception
        if result:
            return result[1]
        return None

