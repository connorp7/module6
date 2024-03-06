class PixyProxyException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DBConnectionError(PixyProxyException):
    def __init__(self):
        super().__init__("Error connecting to the database")
        

class RecordNotFoundError(PixyProxyException):
    def __init__(self):
        super().__init__(f"Record not found")

class ConstraintViolationError(PixyProxyException):
    def __init__(self):
        super().__init__(f"A database constraint was violated")

EXCEPTION_STATUS_CODES = {
    ConstraintViolationError: 409,  # Conflict
    PixyProxyException: 500,           # Internal Server Error (Generic fallback)
    DBConnectionError: 500,         # Internal Server Error (Generic fallback)
    RecordNotFoundError: 404,       # Not Found
}