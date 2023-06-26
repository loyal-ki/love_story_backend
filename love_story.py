from fastapi import (
    FastAPI,
    Request,
    status
)
from fastapi.encoders import jsonable_encoder
from fastapi.requests import HTTPConnection
from fastapi.responses import JSONResponse


from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.routers import routers
from src.settings.settings import Settings
from src.settings import settings as settings_module
from src.constants import VERSION, APP_NAME
from src.config.config import ROOT_PATH
from src.errors import *


class RawContextMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        request = HTTPConnection(scope, receive)
        token = settings_module.settings_ctx.set(request.app.settings)
        try:
            await self.app(scope, receive, send)
        finally:
            settings_module.settings_ctx.reset(token)


# Initialize app
def get_app():

    # Get installation information
    settings = Settings()

    # Initialize FastAPI
    app = FastAPI(title=APP_NAME, version=VERSION,
                  docs_url="/", redoc_url="/redoc", root_path=ROOT_PATH)
    
    app.settings = settings

    # Add router
    app.include_router(routers)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )
    settings.init_logging()

    @app.get("/", tags=["root"])
    def root():
        return {"server": settings.api_title}

    @app.on_event("startup")
    async def startup():
        app.ctx_token = settings_module.settings_ctx.set(
            app.settings)  # for events context
        await settings.init()

    @app.on_event("shutdown")
    async def shutdown():
        await app.settings.shutdown()
        settings_module.settings_ctx.reset(app.ctx_token)

    # 401:NotSupported
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"meta": meta}),
        )

    # 403:NotSupported
    @app.exception_handler(OTPBlockedWithUserId)
    async def otp_blocked_error_handler(request: Request, exc: OTPBlockedWithUserId):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"meta": meta}),
        )

    # 403:NotSupported
    @app.exception_handler(OTPCodeHasExpired)
    async def otp_expired_error_handler(request: Request, exc: OTPCodeHasExpired):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"meta": meta}),
        )
        
      # 403:NotSupported
    @app.exception_handler(OTPCodeIsAlreadyUsed)
    async def otp_already_used_error_handler(request: Request, exc: OTPCodeIsAlreadyUsed):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"meta": meta}),
        )

    # 404:NotSupported
    @app.exception_handler(NotSupportedError)
    async def not_supported_error_handler(request: Request, exc: NotSupportedError):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder({"meta": meta}),
        )

    # 405:MethodNotAllowed
    @app.exception_handler(405)
    async def method_not_allowed_error_handler(request: Request, exc: StarletteHTTPException):
        meta = {
            "code": 405,
            "message": "Method Not Allowed",
            "description": f"method: {request.method}, url: {request.url.path}"
        }
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=jsonable_encoder({"meta": meta}),
        )

    # 409:DataConflict
    @app.exception_handler(DataConflictError)
    async def data_conflict_error_handler(request: Request, exc: DataConflictError):
        meta = {
            "code": exc.error_code,
            "message": exc.message
        }
        if getattr(exc, "description"):
            meta["description"] = exc.description

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder({"meta": meta}),
        )

    # 409:UserDataConflict
    @app.exception_handler(UserDataConflict)
    async def user_data_conflict_error_handler(request: Request, exc: UserDataConflict):
        meta = {
            "code": exc.error_code,
            "message": exc.message
        }
        if getattr(exc, "description"):
            meta["description"] = exc.description

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder({"meta": meta}),
        )

    # 500:InternalServerError
    @app.exception_handler(InternalServerError)
    async def internal_server_error_handler(request: Request, exc: InternalServerError):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
        }
        if getattr(exc, "description"):
            meta["description"] = exc.description

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"meta": meta}),
        )

    # 503:ServiceUnavailable
    @app.exception_handler(ServiceUnavailable)
    async def service_unavailable_error_handler(request: Request, exc: ServiceUnavailable):
        meta = {
            "code": exc.error_code,
            "message": exc.message,
            "description": exc.description
        }
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=jsonable_encoder({"meta": meta}),
        )

    app.add_middleware(RawContextMiddleware)
    return app


# Run app
app = get_app()
