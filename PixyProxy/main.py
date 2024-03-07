import traceback


from fastapi import FastAPI, Request
from web.routers import public_images

app = FastAPI()

# Register routers

# Include the router with a prefix
app.include_router(public_images.router, prefix="/image")

# Innermost first

