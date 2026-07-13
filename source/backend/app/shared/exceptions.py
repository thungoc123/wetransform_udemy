from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.shared.response import StandardResponse

class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, errors: list = None):
        self.message = message
        self.status_code = status_code
        self.errors = errors

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            success=False,
            message=exc.message,
            errors=exc.errors
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"loc": ".".join(map(str, err.get("loc", []))), "msg": err.get("msg"), "type": err.get("type")} for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardResponse(
            success=False,
            message="Validation error",
            errors=errors
        ).model_dump()
    )

async def global_exception_handler(request: Request, exc: Exception):
    # Log exception here when logging framework is added
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=StandardResponse(
            success=False,
            message="Internal server error",
            errors=str(exc) if str(exc) else "An unexpected error occurred"
        ).model_dump()
    )
