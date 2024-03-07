
import requests
from typing import Optional
from urllib.parse import urlparse
import os
import uuid
from core.models import ImageDetailCreate, Image

def save_image_from_url(self, image_url: str, filename: str):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(os.path.join('images', filename), 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def extract_filename_from_url(url):
    url_path = urlparse(url).path
    filename = os.path.basename(url_path)
    return filename        

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(base_url='http://aitools.cs.vt.edu:7860/openai/v1', api_key = 'aitools')

    def generate_image(self, image: ImageDetailCreate) -> str:
        # Implementation of the create image use case
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=image.prompt,  # Assuming the ImageDetailCreate model has a 'prompt' field
            style="natural",
            quality="standard",
            size="1024x1024",
            timeout=100
        )

        image_url = response.data[0].url

        response = requests.get(image_url)
        if response.status_code == 200:
            filename = extract_filename_from_url(image_url)
            file_path = os.path.join('images', filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return filename
        else:
            raise Exception(f"Failed to download image")