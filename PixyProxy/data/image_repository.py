
from core.models import ImageDetail, ImageDetailCreate, Image
from openai import OpenAI
from datetime import datetime
from typing import Optional




class ImageRepositoryInterface:

    def get_image_by_guid(self, guid):
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
        self.connection = create_connection()

    def get_image_by_guid(self, guid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM images WHERE guid = %s", (guid,))
        row = cursor.fetchone()
        if row:
            return ImageDetail(guid=row[1], filename=row[2], prompt=row[3])
        return None

    def get_all_images(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM images")
        rows = cursor.fetchall()
        return [ImageDetail(guid=row[1], filename=row[2], prompt=row[3]) for row in rows]

    def create_image(self, image: ImageDetailCreate):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
            (image.guid, image.filename, image.prompt),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_image_file(self, guid):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT filename FROM images WHERE guid = %s",
            (guid,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    @staticmethod
    def make_result_dict(result):
        result_dict = {
            "id": result[0],
            "guid": result[1],
            "filename": result[2],
            "prompt": result[3],
            "created_at": result[4],
            "updated_at": result[5],
        }
        return result_dict


