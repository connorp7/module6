import os

import httpx
import mysql.connector
import pytest
from dotenv import load_dotenv

from core.models import ImageDetail

# Load environment variables from a .env file
load_dotenv()


# This fixture is used to clear the images from the database before running the tests.
# Its scope is 'module', meaning it will run once per module,
# and 'autouse=True' means it will automatically be used without having to be specified in each test function.
@pytest.fixture(scope='module', autouse=True)
def clear_images(db_connection):
    cursor = db_connection.cursor()
    # noinspection SqlWithoutWhere
    cursor.execute("DELETE FROM images")
    db_connection.commit()


# This fixture sets up a connection to the database. Its scope is 'module',
# so it will run once per module.  The 'yield' keyword is used to provide
# the database connection to the test functions. After the tests are done,
# the connection is closed.
@pytest.fixture(scope='module')
def db_connection():
    connection = mysql.connector.connect(
        host=f"{os.getenv('DB_HOST')}",
        user=f"{os.getenv('DB_USER')}",
        password=f"{os.getenv('DB_PASSWORD')}",
        database=f"{os.getenv('DB_NAME')}",
        port=f"{os.getenv('DB_PORT')}"
    )
    yield connection
    connection.close()


# This fixture sets up an HTTP client for making requests to the server.
# Its scope is 'module', so it will run once per module.
# The 'yield' keyword is used to provide the HTTP client to the test functions.
# After the tests are done, the client is closed.
@pytest.fixture(scope='module')
def http_client():
    with httpx.Client(base_url="http://localhost:8001", timeout=100) as client:
        yield client


# This fixture creates an image by making a POST request to the server.
# Its scope is 'module', so it will run once per module.
# The created image is then provided to the test functions.
@pytest.fixture(scope='module')
def created_image(http_client: httpx.Client):
    # Send POST request to create image
    response = http_client.post("/image/", json={"prompt": "a rubber duck on a sink"})
    assert response.status_code == 200
    return ImageDetail(**response.json())


# This test function checks if an image can be created successfully.
# It uses the 'http_client' and 'db_connection' fixtures to make a POST
# request to the server and then check if the image details are stored
# correctly in the database.
def test_create_image(http_client: httpx.Client, db_connection, created_image: ImageDetail):
    # Connect to MySQL and check image details
    cursor = db_connection.cursor()
    cursor.execute("SELECT guid, filename, prompt FROM images WHERE guid = %s", (created_image.guid,))
    result = cursor.fetchone()
    assert result == (created_image.guid, created_image.filename, created_image.prompt)


# This test function checks if an image can be retrieved by its GUID.
# It uses the 'http_client' fixture to make a GET request to the server
# and then checks if the retrieved image details match the created image.
def test_get_image_by_guid(http_client: httpx.Client, created_image: ImageDetail):
    # Send GET request to retrieve image by GUID
    response = http_client.get(f"/image/{created_image.guid}")
    assert response.status_code == 200
    retrieved_image_detail = ImageDetail(**response.json())
    assert retrieved_image_detail == created_image


# This test function checks if all images can be retrieved.
# It uses the 'http_client' fixture to make a GET request to the server
# and then checks if the retrieved images match the created image.
def test_get_all_images(http_client: httpx.Client, created_image: ImageDetail):
    # Send GET request to retrieve all images
    response = http_client.get("/image/")
    assert response.status_code == 200
    images = [ImageDetail(**image) for image in response.json()]
    assert len(images) == 1
    assert images[0] == created_image


# This test function checks if the content of an image can be retrieved.
# It uses the 'http_client' fixture to make a GET request to the server
# and then checks if the size of the retrieved image content is larger than 5KB.
def test_get_image_content(http_client: httpx.Client, created_image: ImageDetail):
    # Send GET request to retrieve image content
    response = http_client.get(f"/image/{created_image.guid}/content")

    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
    content_length = len(response.content)

    assert content_length > 5 * 1024  # Check that content is larger than 5KB