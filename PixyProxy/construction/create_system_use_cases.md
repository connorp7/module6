You are an expert in writing FastAPI system use cases. Each use case should briefly describe the operation at hand.

The system we are building is a prompt management system and has a system description:

'''The system is a FastAPI-based REST API designed to manage images generated by the OpenAI API. The images are identified by GUIDs for public use and integer IDs for internal use. Each image also has a prompt used to generate it, a filename, and timestamps for creation and updates.

The API provides four endpoints:
1. POST /image: This endpoint generates an image (and image detail) from a prompt.
2. GET /image/{guid}: This endpoint retrieves the details of an image using the provided GUID.
3. GET /image: This endpoint retrieves the details of all images.
4. GET /image/{guid}/content: This endpoint retrieves the image file using the provided GUID.

The system uses a MySQL database to store image details. The database schema includes a table named 'images' with columns for id, guid, filename, prompt, created_at, and updated_at.

The system is structured into four layers:
1. The '/data' layer: This layer uses a repository pattern to interact with the MySQL database. It includes functionality to convert models to dictionaries and vice versa for efficiency. SQL commands use named parameters, and the initialization logic is in an init.py module.
2. The '/service' layer: This layer handles public and private prompt requests in separate modules. It uses pydantic for revalidation of incoming models from the web layer. All exceptions, whether originating from the database or service layer, use a general 'PixyProxyException' format.
3. The '/core' layer: This layer focuses on models and exceptions, all of which extend 'PixyProxyException'.
4. The '/web' layer: This layer manages resources for images. It uses a dependency pattern to ensure required authentication for private resource methods. It also includes a dependency for universal logging of all requests.

The system requires universal request logging in a specific format, with the request-id generated from host-datetime-threadid. All exceptions are handled by a single exception handler. This design ensures a clean separation of concerns, efficient data handling, and robust error management, making the system reliable and maintainable.'''

Write system use cases for the following system:

'''It seems like we would need the following use cases to make our API useful: Remember that guids are used to identify images.

Generate (Create) an image and image detail from a prompt.

Get image details for an image with the provided guid.

Get image details for all images.

Retrieve an image file using the provided guid.

All these operations can also be performed on private images after authentication has occurred. We will use HTTP basic authentication against a known set of users.'''