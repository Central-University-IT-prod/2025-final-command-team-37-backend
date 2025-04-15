from fastapi import FastAPI, Response, Request, status
from fastapi.responses import JSONResponse


class UserUnauthorizedError(Exception):
    def __init__(self, detail="Not authenticate"):
        self.detail = detail
        super().__init__(self.detail)


class AccessDeniedError(Exception):
    def __init__(self, detail="Access denied"):
        self.detail = detail
        super().__init__(self.detail)


class EntityNotFoundError(Exception):
    def __init__(self, name="Entity"):
        self.detail = f"{name} not found"
        super().__init__(self.detail)


def validation_exception_handler(_: Request, exc: ValueError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


def user_unauthorized_exception_handler(_: Request, exc: UserUnauthorizedError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
    )


def access_denied_exception_handler(_: Request, exc: AccessDeniedError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail},
    )


def entity_not_found_exception_handler(_: Request, exc: EntityNotFoundError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(ValueError, validation_exception_handler)
    app.add_exception_handler(UserUnauthorizedError, user_unauthorized_exception_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_exception_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_exception_handler)
