It seems like we would need the following use cases to make our API useful: Remember that guids are used to identify images.

Generate (Create) an image and image detail from a prompt.

Get image details for an image with the provided guid.

Get image details for all images.

Retrieve an image file using the provided guid.

All these operations can also be performed on private images after authentication has occurred. We will use HTTP basic authentication against a known set of users.