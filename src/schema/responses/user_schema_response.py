from typing import Optional
from pydantic import (
    BaseModel,
    Field,
)


class TokenSchemaResponse(BaseModel):
    """
    A class that defines the TokenSchemaResponse.
    Args:
        access_token: str
        refresh_token: str
        expires_in: int
        issued_at: int
        refresh_token_expires_in: int
        token_type: str
    """

    access_token: str = Field(...)
    refresh_token: str = Field(...)
    expires_in: int
    issued_at: int
    refresh_token_expires_in: int
    token_type: str = Field(...)


class UserInfoSchemaResponse(BaseModel):
    """
    A class that defines the UserInfoSchemaResponse.

    Args:
        email: str
        age: int
        first_name: str
        last_name: str
        phone_number: str
        gender: int
        profile_picture: str
    """

    email: str = Field(...)
    age: int
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    gender: int
    profile_picture: str = Field(...)


class UserSchemaResponse(BaseModel):
    """
    A class that defines the UserSchemaResponse.

    Args:
        user_info: UserInfoSchemaResponse
        user_token: TokenSchemaResponse
    """

    user_info: UserInfoSchemaResponse
    user_token: TokenSchemaResponse


class UserAccessToken(BaseModel):
    """
    A class that defines the UserSchemaResponse.

    Args:
        access_token: str
        refresh_token: str
        token_type: str
    """

    access_token: str
    refresh_token: str
    token_type: str
