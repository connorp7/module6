
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

class ImageGenerator:
    def __init__(self, image_repo: ImageRepositoryInterface):
        self.image_repo = image_repo
        self.client = OpenAI()

    def generate_image(self, image: ImageDetailCreate) -> Optional[Image]:
        # Implementation of the create image use case
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=image.prompt,  # Assuming the ImageDetailCreate model has a 'prompt' field
            size="1024x1024",
            quality="standard",
            n=1,
            timeout=100
        )

        if response.data:
            image_url = response.data[0].url
            # Generate a unique filename for the new image
            filename = f"{image.prompt.replace(' ', '_')}.png"
            # Create a new Image object with the generated data
            new_image = Image(
                prompt=image.prompt,
                guid=image.prompt.replace(' ', '_'),
                filename=filename,
                id=None,  # This will be set by the database
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            # Save the new image to the database
            new_image_id = self.image_repo.create_image(new_image)
            new_image.id = new_image_id
            return new_image

        return None
