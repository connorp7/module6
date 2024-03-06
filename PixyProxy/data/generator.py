
import requests
from urllib.parse import urlparse
import os
import uuid
from data.image_repository import ImageRepositoryInterface 

def save_image_from_url(self, image_url: str, filename: str):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(os.path.join('images', filename), 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

class ImageGenerator:
    def __init__(self, image_repo: ImageRepositoryInterface):
        self.image_repo = image_repo
        self.client = OpenAI(base_url='http://aitools.cs.vt.edu:7860/openai/v1', api_key = 'aitools')

    def generate_image(self, image: ImageDetailCreate) -> Optional[Image]:
        # Implementation of the create image use case
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=image.prompt,  # Assuming the ImageDetailCreate model has a 'prompt' field
            style="natural",
            quality="standard",
            size="1024x1024",
            timeout=100
        )

        if response.data:
            image_url = response.data[0].url
            
            # Generate a unique filename for the new image
            filename = f"{uuid.uuid4()}.png"
            self.save_image_from_url(image_url)
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