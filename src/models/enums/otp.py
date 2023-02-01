from enum import Enum


# OTP Type
class OTPTypeEnum(str, Enum):
    phone = "phone"
    email = "email"


# OTP Type
class OTPStatusEnum(str, Enum):
    not_used = "0"
    already_used = "1"
    blocked = "2"
