from fastapi.openapi.utils import get_openapi
from functools import lru_cache
from pydantic import (
    BaseModel,
    create_model,
    Field
)
from typing import (
    Any,
    Type,
    Union,
    TypeVar
)

from src.errors.errors import AppError


class ErrorInfo(BaseModel):
    code: int = Field(...)
    message: str = Field(...)
    description: str | dict | None


class ErrorResponse(BaseModel):
    meta: ErrorInfo
    details: dict | None


class RequestValidationErrorDict(BaseModel):
    loc: list[str]
    msg: str
    type: str

    class Config:
        @staticmethod
        def schema_extra(schema: dict[str, Any], _) -> None:
            properties = schema["properties"]
            properties["loc"]["example"] = ["body", "contract_address"]
            properties["msg"]["example"] = "field required"
            properties["type"]["example"] = "value_error.missing"


class RequestValidationErrorInfo(ErrorInfo):
    code: int = Field(..., example=88)
    message: str = Field(..., example="Invalid Parameter")
    description: list[RequestValidationErrorDict]


class RequestValidationErrorResponse(BaseModel):
    meta: RequestValidationErrorInfo
    details: dict | None


AppErrorType = TypeVar("AppErrorType", bound=AppError)


@lru_cache(None)
def create_error_model(app_error: Type[AppError]):
    """
    This function creates Pydantic Model from AppError.
    * create_model() generates a different model each time when called,
      so cache is enabled.
    @param app_error: AppError defined in ibet-Wallet-API
    @return: pydantic Model created dynamically
    """

    metainfo_model = create_model(
        f"{app_error.error_type.strip()}Metainfo",
        code=(int, Field(..., example=app_error.error_code)),
        message=(str, Field(..., example=app_error.message))
    )
    error_model = create_model(
        f"{app_error.error_type.strip()}Response",
        meta=(metainfo_model, Field(...,)),
        details=(dict | None, Field(default=None, example=None)),
    )
    return error_model


def get_routers_responses(*args: Type[AppErrorType]):
    """
    This function returns responses dictionary to be used for openapi document.
    Supposed to be used in router decorator.
    @param args: tuple of AppError
    @return: responses dict
    """
    responses_per_status_code: dict[int, list[Type[AppError]]] = {}
    for arg in args:
        if not responses_per_status_code.get(arg.status_code):
            responses_per_status_code[arg.status_code] = [arg]
        else:
            responses_per_status_code[arg.status_code].append(arg)

    # NOTE: set RequestValidationError as default 400 error
    ret: dict[int, dict] = {400: {"model": RequestValidationErrorResponse}}
    for status_code, res in responses_per_status_code.items():
        error_models: list[Type[ErrorResponse]] = []
        for response in res:
            error_models.append(create_error_model(response))

        if len(error_models) > 0:
            if status_code == 400:
                ret[status_code] = {"model": tuple(
                    error_models) + (RequestValidationErrorResponse, )}
            else:
                ret[status_code] = {"model": tuple(error_models)}
    return ret
