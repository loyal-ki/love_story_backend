from enum import IntEnum

from typing import (
    TypeVar,
    Generic,
    Optional
)

from pydantic import (
    BaseModel,
    Field
)

from fastapi import Query

from pydantic.dataclasses import dataclass
from pydantic.generics import GenericModel


# Request sort order
class SortOrder(IntEnum):
    ASC = 0
    DESC = 1


# ResultSetQuery pagination for on-demand option
@dataclass
class ResultSetQuery:
    """
    ResultSet using query for pagination (Request)
    """
    # select records, start on record.
    offset: Optional[int] = Query(
        default=None, description="start position", ge=0)

    # specify the number of records to return.
    limit: Optional[int] = Query(
        default=None, description="number of set", ge=0)


# ResultSet pagination
class ResultSet(BaseModel):
    """
    Result set for pagination (Response)
    """
    count: Optional[int]
    offset: Optional[int] = Field(..., description="start position")
    limit: Optional[int] = Field(..., description="number of set")
    total: Optional[int]


# Base success response
class BaseSuccessResponseModel(BaseModel):
    status_code: int = Field(..., example=200)
    message: str = Field(..., example="Successfully")


# Success response
class SuccessResponse(BaseModel):

    # meta (status_code, message) to return
    meta: BaseSuccessResponseModel = Field(..., example=BaseSuccessResponseModel(
        status_code=200, message="Successfully"))

    # data response
    data: dict = {}

    # default response to return
    @staticmethod
    def default():
        return SuccessResponse(meta=BaseSuccessResponseModel(status_code=200, message="Successfully")).dict()


# Base type data response to return
Data = TypeVar("Data")


# Generic success response can customize many types of data to return
class GenericSuccessResponse(GenericModel, Generic[Data]):

    # meta (status_code, message) to return
    meta: BaseSuccessResponseModel = Field(..., example=BaseSuccessResponseModel(
        status_code=200, message="Successfully"))

    # data response
    data: Data
