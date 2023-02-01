from pydantic import (
    BaseModel,
)


class UserCreateRequest(BaseModel):
    """
    A class that defines the UserCreateRequest.
    Args:
        email: str
        password: str
    """

    email: str
    password: str


class UserUpdateRequest(BaseModel):
    """
    A class that defines the UserUpdateRequest.
    Args:
         first_name: str
        last_name: str
        phone_number: str
        user_role: str
        profile_picture: str
        gender: int
        age: int
    """

    first_name: str
    last_name: str
    phone_number: str
    user_role: str
    profile_picture: str
    gender: int
    age: int
