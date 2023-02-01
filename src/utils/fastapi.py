import decimal
import orjson
from typing import Any

from fastapi.responses import ORJSONResponse
from src.config.config import RESPONSE_VALIDATE_MODE
from src.settings import settings


# Custom ORJSON Response
class CustomORJSONResponse(ORJSONResponse):
    # media type response
    media_type = "application/json"

    # render serializes Python objects to JSON.
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY, default=decimal_default
        )


# check isInstance Decimal
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


# Validate and create Json response to return
def json_response(content: dict):
    RESPONSE_VALIDATION_MODE = RESPONSE_VALIDATE_MODE
    if RESPONSE_VALIDATION_MODE:
        return content
    else:
        return CustomORJSONResponse(content=content)
