class PixyProxyException(Exception):
    pass

class DBConnectionError(PixyProxyException):
    def __init__(self):
        super().__init__("Error connecting to the database")
        

class RecordNotFoundError(PixyProxyException):
    def __init__(self):
        super().__init__(f"Record not found")

class ConstraintViolationError(PixyProxyException):
    def __init__(self):
        super().__init__(f"A database constraint was violated")