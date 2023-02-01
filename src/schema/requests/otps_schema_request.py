from pydantic import (
    BaseModel,
)


class CreateOTPsRequest(BaseModel):
    """
    A class that defines the CreateOTPsRequest.
    Args:
        user_id: str
    """

    user_id: int
    email: str


class VerifyOTPsRequest(BaseModel):
    """
    A class that defines the VerifyOTPsRequest.
    Args:
        user_id: str
        session_id: str
        otp_code: str

    """
    user_id: int
    session_id: str
    otp_code: str
