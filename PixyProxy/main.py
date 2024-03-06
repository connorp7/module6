import traceback

import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import PixyProxyException, EXCEPTION_STATUS_CODES
from web.middleware import LoggingMiddleware, RequestIdMiddleware
from web.routers import public_images, private_images

app = FastAPI()
print(sys.path)
# Register routers

# Include the router with a prefix
app.include_router(public_images.router, prefix="/public", tags=["Public Endpoints"])
app.include_router(private_images.router, prefix="/private", tags=["Private Per-user Endpoints"])

# Innermost first
app.add_middleware(LoggingMiddleware)  # type: ignore
app.add_middleware(RequestIdMiddleware)  # type: ignore


@app.exception_handler(PixyProxyException)
async def handle_image_exception(_request: Request, exc: PixyProxyException):
    # Get the status code from our mapping or default to 500 if not found
    status_code = EXCEPTION_STATUS_CODES.get(type(exc), 500)
    traceback_string = traceback.format_exc()
    return JSONResponse(status_code=status_code, content={"detail": str(exc), "traceback": traceback_string})


@app.exception_handler(Exception)
async def handle_generic_exception(_request: Request, exc: Exception):
    # Log the exception for debugging (optional)
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})
