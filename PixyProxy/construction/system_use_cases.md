Based on the provided information, here are the use cases for the system:

1. **Use Case: Generate an Image**
    - **Actor**: User
    - **Preconditions**: User has a valid prompt.
    - **Postconditions**: An image and image detail are created and stored in the database.
    - **Normal Flow**: User sends a POST request to /image with a prompt. The system generates an image, creates image details, assigns a GUID, and stores all information in the database.

2. **Use Case: Get Image Details by GUID**
    - **Actor**: User
    - **Preconditions**: Image GUID is valid.
    - **Postconditions**: User receives image details.
    - **Normal Flow**: User sends a GET request to /image/{guid}. The system retrieves the image details associated with the provided GUID and returns them to the user.

3. **Use Case: Get Details for All Images**
    - **Actor**: User
    - **Preconditions**: None.
    - **Postconditions**: User receives details for all images.
    - **Normal Flow**: User sends a GET request to /image. The system retrieves the details for all images and returns them to the user.

4. **Use Case: Retrieve Image File by GUID**
    - **Actor**: User
    - **Preconditions**: Image GUID is valid.
    - **Postconditions**: User receives the image file.
    - **Normal Flow**: User sends a GET request to /image/{guid}/content. The system retrieves the image file associated with the provided GUID and returns it to the user.
