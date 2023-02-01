from pydantic import (
    BaseModel,
)


class CreateOTPsResponse(BaseModel):
    """
    A class that defines the CreateOTPsRequest.
    Args:
        user_id: str
    """

    user_id: int
    session_id: str


class VerifyOTPsResponse(BaseModel):
    """
    A class that defines the VerifyOTPsRequest.
    Args:
        user_id: str
        session_id: str
        otp_code: str

    """

    user_id: str
    session_id: str
    otp_code: str


class OTPsStatusResponse(VerifyOTPsResponse):
    """
    A class that defines the CreateOTPsRequest.
    Args:
        user_id: str
        otp_failed_count: int
        status: str
    """

    otp_failed_count: int
    status: str
